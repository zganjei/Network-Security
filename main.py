from networksecurity.components.data_ingestion import DataIgestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig, ModelTrainingConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_training import ModelTraining

import sys

if __name__=="__main__":
    try:
        # Training pipeline
        training_pipeline_config = TrainingPipelineConfig()

        # data ingestion
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIgestion(data_ingestion_config)
        logging.info("Initiate the data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info("Finished data ingestion")

        # data validation
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_config,data_validation_config)
        logging.info("Initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Finished the data validation")

        # data transformation
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
        logging.info("Initiate the data transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_validation_artifact)
        logging.info("Finished the data transformation")

        logging.info("Initiate Model training")
        model_training_config = ModelTrainingConfig(training_pipeline_config)
        model_training = ModelTraining(model_trainer_config=model_training_config, 
                                       data_transformation_artifact=data_transformation_artifact)
        model_training_artifact = model_training.initiate_model_training()

        logging.info("Finished Model training")


    except Exception as e:
        raise NetworkSecurityException(e,sys)