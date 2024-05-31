# End-to-End Streaming Big Data Pipeline using Confluent Kafka and MongoDB

This repo helps us to know how to publish and consume data to and from kafka confluent in json format for real time streaming sensor readings generated from edge/IOT devices.

## Initial setup:

Step 1: Clone the GitHub repo
```
git clone https://github.com/seemanshu-shukla/sensor-fault-detection-big-data-pipeline.git
```

Step 2: Activate the base conda environment
```
conda activate base  #to activate base
source activate #to activate base if above not works
conda --version
```

Step 3: Create the virtual environment
```
conda create -p venv python==3.8 -y
```

Step 4: Activating the virtual environment
```
conda activate venv/
```
Step 5: Installing the pyhtonic dependencies for this project
```
pip install -r requirements.txt
```

## Refer to the below documentation that would help you in getting the required credentials and setting up this entire project:
https://github.com/seemanshu-shukla/Profile-Building/blob/main/End-to-End_Streaming_Big_Data_Pipeline_Using_Kafka_and_MongoDB/Big_Data_Pipeline_Using_Confluent_Kafka_And_MongoDB.pdf

## Cluster Environment Variable
```
API_KEY
API_SECRET_KEY
BOOTSTRAP_SERVER
```


## Schema related Environment Variable
```
SCHEMA_REGISTRY_API_KEY
SCHEMA_REGISTRY_API_SECRET
ENDPOINT_SCHEMA_URL
```
## Data base related Environment Variable
```
MONGO_DB_URL
```

## Update the credential in .env file and run below command to run your application in docker container

Step 1: Create .env file in root dir of your project if it is not available
paste the below content and update the credentials
```
API_KEY="<your credentials>"
API_SECRET_KEY="<your credentials>"
BOOTSTRAP_SERVER="<your credentials>"
SCHEMA_REGISTRY_API_KEY="<your credentials>"
SCHEMA_REGISTRY_API_SECRET="<your credentials>"
ENDPOINT_SCHEMA_URL="<your credentials>"
MONGO_DB_URL="<your credentials>"
```

Step 2: Build docker image
```
docker build -t data-pipeline:lts .
```

Step 3: Run the docker image
For linux or mac
```
docker run -it -v $(pwd)/logs:/logs  --env-file=$(pwd)/.env data-pipeline:lts
```

For windowns user (Please feel free to change the host and container ports based on the ones available in your system)
```
docker run -p 8080:8080 data-pipeline:lts
```