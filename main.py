import fastapi
import uvicorn
from starlette.requests import Request
from routes import weather
from api.openweather import api_key 
import json
from pathlib import Path
app = fastapi.FastAPI()


def config():
    config_routes()
    config_apikeys()

def config_apikeys():
    file = Path('config.json').absolute()
    if not file.exists():
        print('Error : file is not exit')
        raise Exception('config file that contain secrets key does not exists')
    with open('config.json') as fin:
        config = json.load(fin)
        api_key = config.get('api_key')

def config_routes():
    app.include_router(weather.router)

@app.get('/')
def index():
    return 'Hello worssld'


if __name__ == '__main__':
    config()
    uvicorn.run(app,host="localhost",port=5000)
else: config()  #production