import logging
import os
from from_root import from_root
from source.constants import LOGS_DIR, LOGS_FILE_NAME

logs_path = os.path.join(from_root(), LOGS_DIR)

os.makedirs(logs_path, exist_ok=True)

logs_file_name = os.path.join(logs_path, LOGS_FILE_NAME)

logging.basicConfig(filename=logs_file_name,
                    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
                    level=logging.DEBUG)
