from ner_custom.components.data_ingestion import DataIngestion

from ner_custom.entity.config_entity import DataIngestionConfig

di = DataIngestion(DataIngestionConfig)

di_art = di.initiate_data_ingestion()