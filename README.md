# Network Security
This is my End to End Network Security Project with MLOPS and ETL pipelines. The aim of project is to detect phishing data.
I use modular coding

## Project structure 

<!-- ![project structure](image.png) -->
Data Ingestion Component ->  Data Validation Component -> Data Transformation Component -> Model Training Component ->  Model Evaluation Component -> Model Pusher Component

I will use MongoDB Database for this project. 

### ETL pipeline (Extract, Transform, Load)

My data source is a CSV file

Transformation
* basic preprocessing
* cleaning raw data
* converting to json

Then the Json file is stored in MongoDB Atlas




Conda
```
conda init
conda create --prefix ./venv python=3.12
conda activate venv/
```


## The order of creating files/directories

Create the project structure

Fill in requirements.txt

Create logging and exception handling

Create MongoDB Atlas cluster, create a user and test connection


