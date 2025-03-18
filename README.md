# Network Security
This is my End to End Network Security Project with MLOps and ETL pipelines. The aim of project is to detect phishing using Machine Learning.
I use modular coding and Object-Oriented Programming in Python. 
List of tools/libraries/frameworks used: Sklearn, Numpy, Pandas, MLFlow, AWS (S3, EC2, ECR), Github Actions CI/CD Pipeline, MongoDB, FAST API,  Docker

## Project structure 

<!-- ![project structure](image.png) -->
Data Ingestion Component ->  Data Validation Component -> Data Transformation Component -> Model Training Component ->  Model Evaluation Component -> Model Pusher Component

I will use MongoDB Database for this project. 


## The order of creating files/directories

Conda
```
conda init
conda create --prefix ./venv python=3.12
conda activate venv/
```

Create the project structure

Fill in requirements.txt

Create logging and exception handling

Create MongoDB Atlas cluster, create a user and test connection

Create ETL pipeline (push_data.py)


### ETL pipeline (Extract, Transform, Load)

My data source is a CSV file

Transformation
* basic preprocessing
* cleaning raw data
* converting to json

Then the Json file is stored in MongoDB Atlas.

Create training pipeline and add the following steps to that:

## Data Ingestion Architecture

Data Ingestion Config -> Initiate Data Ingestion -> Export raw Data from MongoDB to Feature Store -> Drop unnecassary Columns  and do Feature Engineering -> Split data into train and test -> Data Ingestion Artifact(output) to Feature Store

## Data Validation Architecture

At this stage we need to ensure that our data has the same schema, and we don't have data drift (distribution, etc has not changed)

Data Validation Config -> Initiate Data Validation -> Read Data -> Validate number of Columns -> do numerical columns exist?


## Data Transformation Architecture

Prerocessing data to Replace NAN values, Scale input

## Model Training and Evaluation Architecture

Model trainer config , Data Transformation Artifacts -> Initiate Model Training -> Load numpy array data -> Split train and test-> Model factory -> get best model -> Model sensor -> calculate metric -> Model Trainer Artifact (model.pkl file)

## MLflow
Add mlflow tracking to code and use DAGsHub to connect to this repository. In the repo at DagsHub, choose remote -> experiments and copy the code. Add the code to model training file. Then the local mlflow will not be created. Instead they will go to dagshub experiments.

add app.py file which is the frontand and will trigger the pipeline


```
uvicorn app:app --reload
```



![alt text](image-1.png)


## Cloudify: Step 1. Move artifacts to S3 bucket

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

```

Create IAM user on AWS with -> attach policies directly ->add  permission AdministratorAccess -> create user

users -> select the user -> access keys -> create Access Key -> command line interface -> Create Access key

in the terminal write
aws configure
then pass the newly generated aws access key

Create an S3 bucket


## Cloudify: Step 2. Store docker image in AWS ECR

Create ECR (Elastic Contrainer Registry) repository which is a fully-managed docker registry. Then copy the URI next to repository name and add it as a secret to github actions.

## Cloudify: Step 3. Deploying the docker image in AWS EC2