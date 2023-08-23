import os
import subprocess
import mlflow
import pandas as pd
from telemedbasics.io.parquet import read
import sys
sys.path.append(os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0], 'tc_uc4'))

from test_tc.utility.resources import get_configuration



# Models' name to test
models_name = [
    "Italia/Abruzzo", "Italia/Basilicata", "Italia/Bolzano", "Italia/Calabria", "Italia/Campania", "Italia/Emilia-Romagna", "Italia/Friuli-Venezia-Giulia",
    "Italia", "Italia/Lazio", "Italia/Liguria", "Italia/Lombardia", "Italia/Molise", "Italia/Piemonte", "Italia/Puglia", "Italia/Sardegna", "Italia/Sicilia",
    "Italia/Toscana", "Italia/Trento", "Italia/Umbria", "Italia/Valle D Aosta", "Italia/Veneto"
               ]


# Initial setting
experiment_name = "unittest"
python_cmd = 'python'
project_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
config_path = os.path.join(project_path, "tests/config")
path_configs = experiment_name + "_path.toml"
model_configs = experiment_name + "_prophet.toml"


# Configuration path configs
experiment_folder = get_configuration("data_paths", config_path, path_configs)["experiment_folder"]
experiment_folder = os.path.join(project_path, experiment_folder)
predict_save_folder = get_configuration("data_paths", config_path, path_configs)["predict_save_folder"]

# Configuration model configs
model_conf = get_configuration("model", config_path, model_configs)
preprocessing  = get_configuration("preprocessing", config_path, model_configs)
forecasting    = get_configuration("forecasting", config_path, model_configs)
model_name = get_configuration("model", config_path, model_configs)["model_name"]
# ----------
time_granularity = preprocessing["time_granularity"]
apply_reconciler = model_conf['apply_reconciler']
start_date = forecasting["start_date"]
num_forecast_periods = forecasting["num_forecast_periods"]



def test_run_exp_job():
    
    ## TEST EXPERIMENT ##
    subproc_path = os.path.join(project_path, "experiments", "execute_experiment.py")
    subproc_path_escaped = f'"{subproc_path}"'
    command = f'{python_cmd} {subproc_path_escaped} -E {experiment_name}'
    process = subprocess.Popen(command, shell=True)
    process.wait()

    mlflow.set_tracking_uri(experiment_folder)
    experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

    # Find best run
    run = mlflow.search_runs(experiment_ids=experiment_id).loc[0]
    # # Test if trained models are present in artifacts
    model_uri = f"runs:/{run['run_id']}/{model_name}.pkl"
    model = mlflow.sklearn.load_model(model_uri)

    # Test model names
    for id_pred, m in model.models_dict.items():
        assert id_pred in models_name
        
        # Test parameters in specified range
        if m is not None:
            assert m.weekly_seasonality in [True, False]
            assert m.yearly_seasonality in [True, False]

    
    best_reconciler_folder = 'best_reconciler'
    assert len(os.listdir(os.path.join(run.artifact_uri, best_reconciler_folder))) != 0


    ## TEST JOB ##
    subproc_path = os.path.join(project_path, "jobs", "execute_job.py")
    subproc_path_escaped = f'"{subproc_path}"'
    command = f'{python_cmd} {subproc_path_escaped} -E {experiment_name}'
    process = subprocess.Popen(command, shell=True)
    process.wait()
    
    read_path = os.path.join(project_path,predict_save_folder)
    predictions = read(datapath = os.path.join(read_path,"unittest.parquet"))
    hier_predictions = read(datapath = os.path.join(read_path,f"unittest_{apply_reconciler}.parquet"))
    assert type(predictions) == pd.DataFrame
    assert type(hier_predictions) == pd.DataFrame

