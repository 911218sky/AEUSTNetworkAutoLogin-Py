import configparser
from typing import Optional

class Config:
    def __init__(self, ping: str, interval: int, username: str, password: str, login_log_path: str, error_log_path: str):
        self.ping = ping
        self.interval = interval
        self.username = username
        self.password = password
        self.login_log_path = login_log_path
        self.error_log_path = error_log_path


def read_config(config_file_path: str) -> Optional[Config]:
    cfg = configparser.ConfigParser()
    cfg.read(config_file_path)
    settings = cfg['Settings']
    ping = settings.get('PING')
    interval_str = settings.get('INTERVAL')
    interval = int(interval_str)
    username = settings.get('USERNAME')
    password = settings.get('PASSWORD')
    login_log_path = settings.get('LOGIN_LOGFILE_PATH')
    error_log_path = settings.get('ERROR_LOGFILE_PATH')
    return Config(ping, interval, username, password, login_log_path, error_log_path)


def createDefaultConfig(config_file_path: str) -> None:
    cfg = configparser.ConfigParser()
    username = input("Student ID: ")
    password = input("Password: ")
    cfg['Settings'] = {
        'PING': "8.8.8.8",
        'INTERVAL': '1',
        'USERNAME': username,
        'PASSWORD': password,
        'LOGIN_LOGFILE_PATH': 'login.log',
        'ERROR_LOGFILE_PATH': 'error.log'
    }
    with open(config_file_path, 'w') as configfile:
        cfg.write(configfile)
    print("Default configuration file created successfully.")
