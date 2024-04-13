
# Self-deploy Airflow using **Astro**

For the sake of *learning* and *grasping* the whole concept of pipeline (infrastructure included), I tried to set up everything from the dust. Here's everything I did :

## Infrastructure
I installed almalinux **-RHEL9 based-** with virtualbox.
- First step is create a venv python and set autoload in bashrc
- Install docker engine  
    [docker-engine](https://docs.docker.com/engine/install/rhel/)  
    [post-install](https://docs.docker.com/engine/install/linux-postinstall/)

    ```bash
    #add user
    sudo groupadd docker
    sudo usermod -aG docker $USER

    #logout and test
    docker run hello-world

    #set auto start
    sudo systemctl enable docker.service
    sudo systemctl enable containerd.service
    ```
- I use [astro cli](https://docs.astronomer.io/astro/cli/install-cli?tab=linux#install-the-astro-cli) to run airflow and don't forget to set things up like port number and exposing a port
    ```bash
    curl -sSL install.astronomer.io | sudo bash -s

    astro config set -g webserver.port 8081
    astro config set -g airflow.expose_port true
    ```
- Don't forget [java](https://www.linuxtechi.com/how-to-install-java-on-rhel-9/) to run spark! I used **java-1.8.0-openjdk**
- And the [spark](https://www.machinelearningplus.com/pyspark/install-pyspark-on-linux/) itself, here I used **spark-3.5.1**

## Astro 
Astro is airflow and dbt combined, so basically it's ease your life. 
```bash 
astro dev init
```
Edit the dockerfile and or the package dependencies.
Here's my old dockerfile config from work, I don't know if its still relevant to current astro version
```bash
#DOCKERFILE
FROM quay.io/astronomer/astro-runtime:9.4.0

WORKDIR "/usr/local/airflow"
COPY dbt-requirements.txt ./

USER root
RUN apt-get update

#INSTALL UNIXODBC UNTUK DBT
RUN sudo apt-get install -y unixodbc unixodbc-dev
RUN sudo apt-get install -y nano

#INSTALL ODBC 18 DRIVER SQL SERVER
RUN sudo apt-get install -y gnupg && \  
    sudo gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EB3E94ADBE1229CF && \
    curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc && \
    sudo curl https://packages.microsoft.com/config/debian/11/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list && \
    #untuk pasang keyserver
    sudo apt-get update && \
    sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18

#CREATE VENV
RUN python -m virtualenv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir -r dbt-requirements.txt && deactivate
```

## DBT
Basically I need dbt **inside** the container and **outside**.  
The inside is so the airflow/astro can run dbt, the outside part is so we can run or test the models independently. 
```bash
#dbtcore
pip install dbt-core
#addon
pip install dbt-postgres
```

## Spark
After downloaded spark, set up **$SPARK_HOME** in bashrc and also I need py spark so 
```bash
#install pyspark
pip install pyspark
```
*Just a note, so in total I add these 3 lines*
 ```bash  
export SPARK_HOME=/opt/spark
export PATH=$SPARK_HOME/bin:$PATH

source ~/venv/bin/activate
```

Create a file *$SPARK_HOME/conf/spark-defaults.conf* **AND** *~/venv/lib/python3.9/site-packages/pyspark/conf/spark-defaults.conf*
```bash 
spark.driver.memory             16g
spark.executor.memory           16g
spark.master                    local[*]
spark.memory.offHeap.size       8g
spark.memory.offHeap.enabled    true
```

## Databases
I use mongodb for noSQL representative and postgreSQL for RDBMS.  
- Postgre
I just use the built-in from astro *(the one comes with airflow's log, I know I'm not supposed to do this but it's just a test anyway)*.  
- For mongodb I use docker compose with these lines in **docker-compose.yml** and run it.
    ```yaml
    services:
    mongo:
        container_name: mongo
        image: mongo:4.2
        ports:
        - 27017:27017
        command: mongod
        restart: always
    ```
    ```bash 
    docker compose up -d
    ```