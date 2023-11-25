from flask import Flask, request
from web_parser import WebParser
import os
import sys
import json
from waitress import serve

app = Flask(__name__)


@app.route('/get-data', methods=['GET', 'POST'])
def get_data():
    if request.method == 'GET' or request.method == 'POST':
        url = request.args.get('url')
        parser = WebParser()
        result = parser.run(url)
        working_dir = os.path.dirname(
            os.path.abspath(sys.argv[0])).replace('\\', '/')
        with open(f"{working_dir}/{result['title']}.json", "w") as file:
            json.dump(result, file)
        return result
    else:
        return 'Error. User GET or POST method for request'


if __name__ == '__main__':
    # serve(app, host="194.67.111.22", port=8080)
    # example = http://127.0.0.1:5000/get-data?url=your_link_to_product_page
    serve(app, host="95.163.235.215", port=8080)