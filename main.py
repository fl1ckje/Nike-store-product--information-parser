import json
from fastapi import FastAPI
import uvicorn
from src.config import HOST, PORT, NIKE_DATA_PATH
from src.parsing import parse_nike_product_page, parse_nike_product_list

app = FastAPI()


# http://127.0.0.1:5000/get-product/?url=https://google.com


@app.get("/get-product/")
async def get_product(url: str = None):
    if url is None:
        return json.dumps(
            {
                "status": "ERR",
                "result": f"Error: no product URL found. Example: http://{HOST}:{PORT}/get-product/?url=PRODUCT_URL"
            }
        )
    else:
        result = parse_nike_product_page(url)
        return json.dumps(
            {
                "status": "OK",
                "result": result
            }
        )


@app.get("/get-product-list/")
async def get_product_list():
    result = parse_nike_product_list(NIKE_DATA_PATH)
    return json.dumps(
        {
            "status": "OK",
            "result": result
        }
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, log_level="info")
