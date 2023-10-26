# Nike-store-product-page-parser
Product information parser on Nike website using Selenium. Works as web app.

## Usage quick-guide
1. Download this repository.
2. Install requirements using following command:
```sh
pip install -r requirements.txt
```
3. Set environment variables:
```sh
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=0
```
4. In app.py configure host and port:
```python
if __name__ == '__main__':
    # paste here your host and port instead of 127.0.0.1 and 5000
    http_server = WSGIServer(('127.0.0.1', 5000), app) 
    http_server.serve_forever()
```
4. Run parser web app:
```sh
flask run #or python3 app.py
```
