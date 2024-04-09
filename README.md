
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
- I use [astro cli](https://docs.astronomer.io/astro/cli/install-cli?tab=linux#install-the-astro-cli) to run airflow 
    ```bash
    curl -sSL install.astronomer.io | sudo bash -s

    astro config set -g webserver.port 8081
    astro config set -g airflow.expose_port true
    ```
    and set things up like port number and exposing a port

- Don't forget [java](https://www.linuxtechi.com/how-to-install-java-on-rhel-9/) to run spark! I used **java-1.8.0-openjdk**
- And the [spark](https://www.machinelearningplus.com/pyspark/install-pyspark-on-linux/) itself, here I used **spark-3.5.1**

## Astro 
Astro is airflow and dbt combined, so basically it's ease your life. 
```bash 
astro dev init
```
Edit the dockerfile and or the package dependencies.

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
spark.memory.executor   = 16g
spark.memory.driver     = 16g
```