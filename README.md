# Nike-store-product-page-parser
Product information parser on Nike website using Selenium. Works as web app.

## Usage quick-guide
1. Make sure that you have got Firefox browser and gecko driver installed.
2. Download this repository.
3. Install requirements using following command:
```sh
pip install -r requirements.txt
```
4. Set environment variables:
```sh
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=0
```
5. In app.py configure host and port:
```python
if __name__ == '__main__':
    # paste here your host and port instead of 127.0.0.1 and 5000
    serve(app, host="127.0.0.1", port=5000)
```
6. Run parser web app:
```sh
flask run #or python3 app.py
```
