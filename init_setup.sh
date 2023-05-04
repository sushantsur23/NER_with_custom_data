echo [$(date)] : "STARTING INITIAL SETUP"
export _VERSION_=3.8

echo [$(date)] : "PROJECT DIRECTORY NAME"
read project_name_
export project_name_=$project_name_
echo [$(date)] : "CREATING PROJECT STRUCTURE"

echo [$(date)] : "CREATING DATA INGESTION"
mkdir -p ${project_name_}/components
touch ${project_name_}/__init__.py
touch ${project_name_}/components/__init__.py ${project_name_}/components/data_ingestion.py

echo [$(date)] : "CREATING DATA VALIDATION"
# mkdir -p ${project_name_}/data_validation
touch ${project_name_}/components/__init__.py ${project_name_}/components/data_validation.py

echo [$(date)] : "CREATING DATA TRANSFORMATION"
# mkdir -p ${project_name_}/data_transformation
touch ${project_name_}/components/__init__.py ${project_name_}/components/data_transformation.py

echo [$(date)] : "CREATING MODEL TRAINING"
# mkdir -p ${project_name_}/model_training
touch ${project_name_}/components/__init__.py ${project_name_}/components/model_training.py

echo [$(date)] : "CREATING MODEL EVALUATION/ANALYSIS"
mkdir -p ${project_name_}/model_analysis
touch ${project_name_}/model_analysis/__init__.py ${project_name_}/model_analysis/model_evaluation.py

echo [$(date)] : "CREATING CONFIGURATION COMPONENT"
mkdir -p ${project_name_}/configuration
touch ${project_name_}/configuration/__init__.py ${project_name_}/configuration/configuration_component.py

echo [$(date)] : "CREATING LOGGING LAYER"
mkdir -p ${project_name_}/logging
touch ${project_name_}/logging/__init__.py ${project_name_}/logging/logging.py ${project_name_}/logging/logs.txt

echo [$(date)] : "CREATING UTILITY LAYER"
mkdir -p ${project_name_}/utils
touch ${project_name_}/utils/__init__.py ${project_name_}/utils/main_utils.py

echo [$(date)] : "CREATING EXCEPTION LAYER"
mkdir -p ${project_name_}/exception
touch ${project_name_}/exception/__init__.py ${project_name_}/exception/exception_handler.py

echo [$(date)] : "CREATING ENTITY LAYER"
mkdir -p ${project_name_}/entity
touch ${project_name_}/entity/__init__.py ${project_name_}/entity/artifact_entity.py 
touch ${project_name_}/entity/config_entity.py


echo [$(date)] : "CREATING CONSTANT LAYER"
mkdir -p ${project_name_}/constant
mkdir -p ${project_name_}/constant/constant_names
touch ${project_name_}/constant/constant_names/__init__.py
touch ${project_name_}/constant/__init__.py ${project_name_}/constant/database.py
touch ${project_name_}/constant/__init__.py ${project_name_}/constant/application.py
touch ${project_name_}/constant/__init__.py ${project_name_}/constant/env_variable.py
touch ${project_name_}/constant/__init__.py ${project_name_}/constant/bucket_name.py


echo [$(date)] : "CREATING DATA ACCESS LAYER"
mkdir -p ${project_name_}/data_access
touch ${project_name_}/data_access/__init__.py
touch ${project_name_}/data_access/data.py


echo [$(date)] : "CREATING PIPELINE LAYER"
mkdir -p ${project_name_}/pipeline
touch ${project_name_}/pipeline/__init__.py
touch ${project_name_}/pipeline/training_pipeline.py


echo [$(date)] : "CREATING ARTIFACTS"
mkdir -p ${project_name_}/artifacts
touch ${project_name_}/artifacts/__init__.py
mkdir -p ${project_name_}/artifacts/models
mkdir -p ${project_name_}/artifacts/datasets
mkdir -p ${project_name_}/artifacts/polts
mkdir -p ${project_name_}/artifacts/serialized_objects


echo [$(date)] : "CREATING NOTEBOOK FOLDER"
mkdir -p ${project_name_}/Notebooks
touch ${project_name_}/Notebooks/test1.ipynb
touch ${project_name_}/Notebooks/test2.ipynb
touch ${project_name_}/Notebooks/test3.ipynb

echo [$(date)] : "CREATING API ENDPOINT !"
touch main.py

echo [$(date)] : "CREATING CONDA ENVIRONMENT"
conda create --prefix ./sentimentp python=${_VERSION_} -y
source activate ./sentimentp

echo [$(date)] : "CREATE REQUIREMENTS TEXT FILE"
touch requirements.txt
pip_requirements() {
if test "$#" -eq 0
then 
  echo $'\nProvide at least one Python package name\n' 
else 
  for package in "$@"
  do
    pip install $package
    pip freeze | grep -i $package >> requirements.txt
  done
fi
}
pip_requirements numpy pandas seaborn sklearn pymongo fastapi nltk notebook matplotlib ipykernel PyYAML notebook ipykernel dill uvicorn


echo [$(date)]: "CREATING DOCKER FILE"
touch Dockerfile
touch .dockerignore

echo [$(date)]: "CREATING ADDITIONAL FILES"
touch config.yaml

echo [$(date)] : "END"