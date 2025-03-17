from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig, ModelTrainingConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainingArtifact
from networksecurity.components.data_ingestion import DataIgestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_training import ModelTraining

import sys

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            logging.info("Initiate the data ingestion")
            data_ingestion = DataIgestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Finished data ingestion with artifact {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        
    
    def data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            logging.info("Initiate the data validation")
            data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Finished the data validation with artifact {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        
    def data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            logging.info("Initiate the data transformation")
            data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Finished the data transformation with artifact {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def model_training(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info("Initiate Model training")
            model_training_config = ModelTrainingConfig(self.training_pipeline_config)
            model_training = ModelTraining(model_trainer_config=model_training_config, 
                                        data_transformation_artifact=data_transformation_artifact)
            model_training_artifact = model_training.initiate_model_training()

            logging.info("Finished Model training")
            return model_training_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.data_ingestion()
            data_validation_artifact = self.data_validation(data_ingestion_artifact)
            data_trasformation_artifact = self.data_transformation(data_validation_artifact)
            model_training_artifact = self.model_training(data_trasformation_artifact)
            return model_training_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) 