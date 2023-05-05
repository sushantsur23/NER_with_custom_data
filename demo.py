from ner_custom.components.data_ingestion import DataIngestion
from ner_custom.entity.config_entity import DataIngestionConfig

DI = DataIngestion(DataIngestionConfig)
DI.initiate_data_ingestion()

