from pprint import pformat

import uvicorn
from fastapi import FastAPI

from app.core.config import app_settings
from app.core.logs import logger

app = FastAPI(
    title=app_settings.APP_TITLE,
    description=app_settings.APP_DESCRIPTION,
    version='1.0.0',
    debug=app_settings.DEBUG,
    docs_url='/',
)

if __name__ == '__main__':
    logger.info("Start with configuration: \n%s", pformat(app_settings.model_dump()))
    uvicorn.run(app, host='localhost', port=10000)
