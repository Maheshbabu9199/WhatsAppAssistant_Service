from .constants_retriever import ConstantsRetriever
import logging 
import os 



class CustomLogger:

    @staticmethod
    def get_logger(name: str) -> logging.Logger:



        

        logger = logging.getLogger(name)

        # Prevent duplicate handlers
        if logger.handlers:
            return logger

        logging_config = ConstantsRetriever.getConstants("logging_config")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        logs_folder = os.path.join(base_dir, logging_config["logging_folder"])
        os.makedirs(logs_folder, exist_ok=True)

        file_name = os.path.join(logs_folder, logging_config["log_file"])

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | "
            "%(filename)s:%(lineno)d | %(message)s"
        )

        handler = logging.FileHandler(file_name, mode="a")
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)

        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(formatter)
        logger.addHandler(streamhandler)
        logger.setLevel(logging.DEBUG)

        logger.propagate = False 

        return logger



