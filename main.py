import os
import time
from config import read_config, create_default_config
from utils.network_utils import run_auto_network

def main():
    config_file_path = "config.ini"
    if not os.path.exists(config_file_path):
        create_default_config(config_file_path)
    config = read_config(config_file_path)
    while True:
        run_auto_network(config)
        time.sleep(config.interval)

if __name__ == "__main__":
    main()
