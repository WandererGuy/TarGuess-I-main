from fastapi import FastAPI, HTTPException, Form
import os 
import uvicorn
import logging
import configparser
import subprocess
import re
from fastapi.staticfiles import StaticFiles

import os, sys
sys.path.insert(0, os.path.abspath(".."))

from routers import targuess_services as tar

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='fastapi.log', filemode='w')
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('config/config.ini')
host_ip = config['DEFAULT']['host'] 
port_num = config['DEFAULT']['port'] 

app = FastAPI()
app.include_router(tar.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
# Endpoint to receive an image and start the processing pipeline
@app.get("/")
async def root():
    return {"message": "Hello World"}


def main():
    print('INITIALIZING FASTAPI SERVER')
    uvicorn.run("server_api:app", host=host_ip, port=int(port_num), reload=True)

if __name__ == "__main__":
    main()
