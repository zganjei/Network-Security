# Network Security
This is my End to End Network Security Project with MLOps and ETL pipelines. The aim of project is to detect phishing.
I use modular coding and Object-Oriented Programming in Python.

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

Then the Json file is stored in MongoDB Atlas

## Data Ingestion Architecture

Data Ingestion Config -> Initiate Data Ingestion -> Export raw Data from MongoDB to Feature Store -> Drop unnecassary Columns  and do Feature Engineering -> Split data into train and test -> Data Ingestion Artifact(output) to Feature Store

## Data Validation Architecture

At this stage we need to ensure that our data has the same schema, and we don't have data drift (distribution, etc has not changed)

Data Validation Config -> Initiate Data Validation -> Read Data -> Validate number of Columns -> do numerical columns exist?


## Data Transformation Architecture

Prerocessing data to Replace NAN values, Scale input