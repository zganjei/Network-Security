from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainingArtifact
from networksecurity.entity.config_entity import ModelTrainingConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.logging.logger import logging
from networksecurity.utils.utils import load_numpy_array_data, save_object, load_object, get_classification_score, evaluate_models
from networksecurity.utils.utils import NetworkModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
import mlflow

import os,sys
import pandas as pd

import dagshub
dagshub.init(repo_owner='zzganjei', repo_name='Network-Security', mlflow=True)

# with mlflow.start_run():
#   mlflow.log_param('parameter name', 'value')
#   mlflow.log_metric('metric name', 1)


class ModelTraining:
    def __init__(self, model_trainer_config: ModelTrainingConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_training_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        
    def track_mlflow(self, best_model, classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            recall_score = classification_metric.recall_score
            precision_score = classification_metric.precision_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model, "model")
    
    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree":  DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier()
            }
            params = {
                "Decision Tree":  {
                    'criterion': ['gini', 'entropy', 'log_loss'],
                    # 'splitter': ['best', 'random'],
                    # 'max_features': ['sqrt', 'log2']
                },
                "Random Forest": {
                    'n_estimators': [8,16,32,64,128,256],
                    # 'criterion': ['gini', 'entropy', 'log_loss'],
                    # 'max_features': ['sqrt', 'log2', None]
                },
                "Gradient Boosting": {
                    #'loss': ['log_loss', 'exponential'],
                    'learning_rate': [.1, .01, .05, .001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    'n_estimators': [8,16,32,64,128,256],
                    # 'criterion': ['squared_error', 'friedman_mse'],
                    # 'max_features': ['auto', 'sqrt', log2],
                },
                "Logistic Regression": {},
                "AdaBoost": {
                    'learning_rate': [.1, .01, .05, .001],
                    'n_estimators': [8,16,32,64,128,256],
                }
            }
            model_report: dict = evaluate_models(X_train=X_train, y_train=y_train,X_test=X_test,y_test=y_test,
                                                 models=models, params=params)
            best_model_score = max(model_report.values())
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]
            y_train_pred = best_model.predict(X_train)
            
            classification_train_metric = get_classification_score(y_true=y_train,y_pred=y_train_pred)

            y_test_pred = best_model.predict(X_test)
            classification_test_metric = get_classification_score(y_true=y_test,y_pred=y_test_pred)

            
            # Track the experiments with mlflow
            self.track_mlflow(best_model,classification_train_metric)
            self.track_mlflow(best_model,classification_test_metric)

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_training_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
            save_object(self.model_training_config.trained_model_file_path,network_model)
            save_object("final_model/model.pkl",best_model)

            # Model Training Artifact
            model_training_artifact = ModelTrainingArtifact(
                                    trained_model_file_path=self.model_training_config.trained_model_file_path,
                                    train_metric_artifact=classification_train_metric,
                                    test_metric_artifact=classification_test_metric)
            
            logging.info(f"Model training artifact {model_training_artifact}")
            return model_training_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys) 

    def initiate_model_training(self) -> ModelTrainingArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # load training and test arrays
            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_array[:, :-1], # all columns except for target column
                train_array[:, -1], # target column
                test_array[:, :-1], # all columns except for target column
                test_array[:, -1] # target column
            )

            model_training_artifact = self.train_model(x_train,y_train,x_test,y_test)
            return model_training_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys) 