import subprocess
import re
import requests
import datetime
from config import Config
from bs4 import BeautifulSoup


def ping_host(host: str) -> bool:
    ping_command = f"ping -c 1 -W 2 {host}"
    try:
        output = subprocess.check_output(
            ping_command, shell=True, universal_newlines=True)
        packets_received = re.search(r"(\d) packets received", output)
        if packets_received:
            return int(packets_received.group(1)) > 0
    except subprocess.CalledProcessError:
        pass
    return False


def get_formatted_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_error(error_log_path: str, error: str) -> None:
    log_entry = f"[{get_formatted_datetime()}] ERROR: {error}\n"
    with open(error_log_path, "a") as log_file:
        log_file.write(log_entry)


def log_success(login_log_path: str, message: str) -> None:
    log_entry = f"[{get_formatted_datetime()}] SUCCESS: {message}\n"
    with open(login_log_path, "a") as log_file:
        log_file.write(log_entry)


def run_auto_network(config: Config) -> None:
    try:
        ping_successful = ping_host(config.ping)
        if ping_successful:
            return

        resp = requests.get("http://www.gstatic.com/generate_204")
        resp.raise_for_status()

        body = resp.text

        if body == "":
            log_error(config.error_log_path, "Empty response from server")
            return

        regex = re.compile(r'window\.location\s*=\s*"([^"]+)";')
        match = regex.search(body)
        if not match or len(match.groups()) < 1:
            log_error(config.error_log_path, "Login URL not found")
            return
        login_url = match.group(1)

        resp = requests.get(login_url)
        body = resp.text

        soup = BeautifulSoup(body, 'html.parser')
        magic = soup.select_one('input[type=hidden]:nth-child(1)').get('value')

        if magic == "":
            log_error(config.error_log_path, "Magic value not found")
            return

        payload = {
            "magic": magic,
            "4Tredir": "http://edge-http.microsoft.com/captiveportal/generate_204",
            "username": config.username,
            "password": config.password
        }

        headers = {
            "Host": "fg.aeust.edu.tw:1442",
            "Origin": "https://fg.aeust.edu.tw:1442",
            "Referer": login_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        resp = requests.post("https://fg.aeust.edu.tw:1442/",
                             data=payload, headers=headers)

        resp.raise_for_status()

        if resp.status_code == 200:
            log_success(config.login_log_path,
                        "Login successful " + config["username"])

    except Exception as e:
        log_error(config.error_log_path, e)
