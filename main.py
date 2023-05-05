from ner_custom.configuration.configuration_component import MongoDBClient
from ner_custom.exception import MyException
import os,sys
from ner_custom.logger import logging
from ner_custom.pipeline import training_pipeline
from ner_custom.pipeline.training_pipeline import TrainPipeline
import os
from ner_custom.utils.main_utils import read_yaml_file
from ner_custom.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI
from ner_custom.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
# from ner_custom.ml.model.estimator import ModelResolver,TargetValueMapping
from ner_custom.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
import os


env_file_path=os.path.join(os.getcwd(),"env.yaml")

def set_env_variable(env_file_path):

    if os.getenv('MONGO_DB_URL',None) is None:
        env_config = read_yaml_file(env_file_path)
        os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")






def main():
    try:
        set_env_variable(env_file_path)
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__=="__main__":
    #main()
    # set_env_variable(env_file_path)
    app_run(app, host=APP_HOST, port=APP_PORT)
