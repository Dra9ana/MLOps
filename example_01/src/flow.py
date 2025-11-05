import mlflow
from sklearn.neighbors import KNeighborsClassifier
from src.core import config

mlflow.set_tracking_uri(config.mlflow.tracking_uri)

# If you have an experiment name in config, use it
experiment_name = config.mlflow.experiment_name or 'DefaultExperiment'
try:
    exp_id = mlflow.create_experiment(name=experiment_name)
    
except Exception as e:
    exp_id = mlflow.get_experiment_by_name(experiment_name).experiment_id