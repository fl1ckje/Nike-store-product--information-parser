from pathlib import Path


HOST = '127.0.0.1'
PORT = 9222

# "/usr/local/bin/geckodriver"

GECKO_DRIVER_PATH = "/snap/bin/firefox.geckodriver"
"""
Get gecko driver here: https://github.com/mozilla/geckodriver/releases
"""

HEADLESS = False
SAVE_PRODUCT_TO_FILE = True

CWD_PATH = Path.cwd()
DOWNLOADS_PATH = CWD_PATH / 'downloads'
DATA_PATH = CWD_PATH / 'data'

NIKE_DATA_PATH = DATA_PATH / 'nike.txt'
SCROLL_PAUSE_TIME = 0.3
