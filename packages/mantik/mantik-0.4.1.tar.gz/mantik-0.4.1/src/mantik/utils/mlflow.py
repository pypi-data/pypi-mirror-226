import mlflow.tracking as tracking
import mlflow.tracking._tracking_service.utils as mlflow_utils

import mantik.utils.env as env

TRACKING_URI_ENV_VAR = mlflow_utils._TRACKING_URI_ENV_VAR
TRACKING_TOKEN_ENV_VAR = mlflow_utils._TRACKING_TOKEN_ENV_VAR
TRACKING_USERNAME_ENV_VAR = mlflow_utils._TRACKING_USERNAME_ENV_VAR
TRACKING_PASSWORD_ENV_VAR = mlflow_utils._TRACKING_PASSWORD_ENV_VAR
EXPERIMENT_NAME_ENV_VAR = tracking._EXPERIMENT_NAME_ENV_VAR
EXPERIMENT_ID_ENV_VAR = tracking._EXPERIMENT_ID_ENV_VAR

CONFLICTING_ENV_VARS = (
    TRACKING_USERNAME_ENV_VAR,
    TRACKING_PASSWORD_ENV_VAR,
)


def unset_conflicting_env_vars() -> None:
    env.unset_env_vars(CONFLICTING_ENV_VARS)
