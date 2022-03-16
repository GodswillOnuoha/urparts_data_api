import logging

from fastapi import FastAPI
import uvicorn

from web_api.api import machine_parts_api
from web_api.settings import log_level, log_filemode


api = FastAPI()


def configure():
    logging.basicConfig(level=log_level)
    configure_routing()


def configure_routing():
    api.include_router(machine_parts_api.router)


if __name__ == "__main__":
    configure()
    uvicorn.run(api, host="0.0.0.0", port=8000)
else:
    configure()
