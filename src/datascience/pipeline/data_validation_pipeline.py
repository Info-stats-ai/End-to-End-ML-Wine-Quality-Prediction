from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.data_validation import DataValiadtion
from src.datascience import logger

STAGE_NAME = "Data Validation stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_validation(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValiadtion(config=data_validation_config)
        data_validation.validate_all_columns()
#this is the pipeline for data validation
# what it does is it validates all the columns in the data with the schema.yml file
# if the columns are not in the schema.yml file, it will raise an error
# if the columns are in the schema.yml file, it will return True
# it will also return the status of the validation
# it will also return the status of the validation in the status.txt file
# it will also return the status of the validation in the status.txt file

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataValidationTrainingPipeline()
        obj.initiate_data_validation()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e