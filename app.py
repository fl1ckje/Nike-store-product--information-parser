from flask import Flask, request
from web_parser import WebParser
import os, sys, json
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route('/get-data', methods=['GET', 'POST'])
def get_data():
    if request.method == 'GET' or request.method == 'POST':
        

        #получаем url из аргумента запроса
        url = request.args.get('url')

        #создаём экземпляр объекта парсера
        parser = WebParser()

        #получаем результат
        result = parser.run(url)

        #закрываем веб драйвер парсера
        parser.driver.quit()

        #сохраняем результат в json файл рядом со скриптом
        working_dir = os.path.dirname(os.path.abspath(sys.argv[0])).replace('\\', '/')
        with open(f"{working_dir}/{result['title']}.json", "w") as file: 
            json.dump(result, file)

        #возвращаем результат клиенту        
        return result
    else:
        return 'Error. User GET or POST method for request'



if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
    # example = http://127.0.0.1:5000/get-data?url=your_link_to_product_page