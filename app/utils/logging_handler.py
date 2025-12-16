from .constants_retriever import ConstantsRetriever
import logging 
import os 



class CustomLogger:

    @staticmethod
    def get_logger(name: str) -> logging.Logger:



        logs_folder = os.path.join(os.getcwd(), ConstantsRetriever.get_constants('logging_config')['logging_folder'])
        os.makedirs(logs_folder, exist_ok=True)

        # name_format = datetime.now().strftime("%Y_%M_%d:%H_%m_%S")
        file_name = os.path.join(logs_folder, ConstantsRetriever.get_constants('logging_config')['log_file'])

        logging_format = "%(asctime)s: %(levelname)s: %(filename)s: %(funcName)s: %(message)s"
        logging.basicConfig(filemode='w', filename=file_name,
                             format=logging_format, 
                             level=ConstantsRetriever.get_constants('logging_config')['log_level'])

        
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        return logger



