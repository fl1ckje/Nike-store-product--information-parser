# Nike-store-product--information-parser
Product information parser on Nike website using Selenium.

## Usage quick-guide
1. Make sure that you have got Firefox browser and gecko driver installed.
2. Download this repository.
3. Install requirements using following command:
```sh
pip install -r requirements.txt
```
4. In `src/config.py` configure host and port:
```python
HOST = '127.0.0.1'
PORT = 9222
```
5. In `src/config.py` configure path to geckodriver:
```python
GECKO_DRIVER_PATH = "/snap/bin/firefox.geckodriver"
```
6. Run application:
```sh
python3 main.py
```
