from ner_custom.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
# /,DataValidationConfig,DataTransformationConfig
from ner_custom.entity.artifact_entity import DataIngestionArtifact
# /, DataValidationArtifact,DataTransformationArtifact
# from ner_custom.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact,ModelTrainerArtifact
# from ner_custom.entity.config_entity import ModelPusherConfig,ModelEvaluationConfig,ModelTrainerConfig
from ner_custom.exception import MyException
import sys,os
from ner_custom.logger import logging
from ner_custom.components.data_ingestion import DataIngestion
from ner_custom.components.data_validation import DataValidation
from ner_custom.components.data_transformation import DataTransformation
# from ner_custom.components.model_trainer import ModelTrainer
# from ner_custom.components.model_evaluation import ModelEvaluation
from ner_custom.components.model_pusher import ModelPusher
from ner_custom.cloud_storage.s3_sync import S3Sync
# from ner_custom.constant.s3_bucket import TRAINING_BUCKET_NAME
from ner_custom.constant.training_pipeline import SAVED_MODEL_DIR


class TrainPipeline:
    is_pipeline_running=False
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except  Exception as e:
            raise MyException(e,sys)


    def run_pipeline(self):
        try:
            
            TrainPipeline.is_pipeline_running=True

            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact=self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            model_eval_artifact = self.start_model_evaluation(data_validation_artifact, model_trainer_artifact)
            if not model_eval_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")
            model_pusher_artifact = self.start_model_pusher(model_eval_artifact)
            TrainPipeline.is_pipeline_running=False
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
        except  Exception as e:
            self.sync_artifact_dir_to_s3()
            TrainPipeline.is_pipeline_running=False
            raise MyException(e,sys)

