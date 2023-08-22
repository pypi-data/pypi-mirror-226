#from mlflow.exceptions import MlflowException  # This only works on an ML cluster



# Load a Model from a particular Stage of the Model Registry
def load_model_from_registry_stage(model_name, model_stage, mlflow, lib):
    # Return a Model from the appropriate Stage of the Model Registry

    # Parameters:
    # model_name - Name of the Model
    # model_stage - Stage the Model is loaded at in the Model Registry
    # mlflow - MLFlow object
    # lib - pyfunc/spark/sklearn

    # Models should theoretically be in at least one of two Stages - 'Staging' and 'Production'.
    # 'Staging' represents Dev and Test and 'Production' represents Prod.
    # There is another Stage 'None' but developers are encouraged to promote their models to 'Staging' prior to system testing.
    # If we have asked for a Model from Stage 'None' and it does not exist here, elevate our search into Stage 'Staging':
    #   - If it does not exist here either, elevate our search to Stage 'Production'
    #   - If it does not exist here either, raise an error
    # If we have asked for a Model from Stage 'Staging' and it does not exist here, elevate our search into Stage 'Production':
    #   - If it does not exist here either, raise an error
    try:
        # Load the Model from the specified Stage in the MLFlow Registry
        modelUri = f"models:/{model_name}/{model_stage}"

        #match lib.lower():
        #    case "spark":
        #        model = mlflow.spark.load_model(modelUri)
        #    case "sklearn":
        #        model = mlflow.sklearn.load_model(modelUri)
        #    case other:
        #        model = mlflow.pyfunc.load_model(modelUri)

        if lib.lower() == "spark":
            model = mlflow.spark.load_model(modelUri)            
        elif lib.lower() == "sklearn":
            model = mlflow.sklearn.load_model(modelUri)
        else:
            model = mlflow.pyfunc.load_model(modelUri)

        print(f"Model '{model_name}' found at Stage '{model_stage}'.")
    except: # MlflowException:
        # If we are at Stage 'Production' and haven't found the Model, raise an error.
        if model_stage == "Production":
            raise
        else:
            # Elevate the Stage to the next logical level. 'None' moves to 'Staging', 'Staging' moves to 'Production'.
            model_stage = "Staging" if model_stage == "None" else "Production"
            return load_model_from_registry_stage(model_name, model_stage, mlflow, lib)
    else:
        return model


# Load a Model from the Model Registry

def load_model_from_registry(model_name, model_stage, mlflow, lib="python", registry_uri = None):
    """
    Return a Model from the appropriate Stage of the Model Registry

    Parameters:
    model_name - Name of the Model
    model_stage - Stage the Model is loaded at in the Model Registry
    mlflow - MLFlow object
    lib - pyfunc/spark/sklearn.  Default pyfunc.
    registry_uri - uri of the registry that you want to connect to. Default 
    """

    # Prepare to access the MLflow Databricks Workspace (shared Model Registry)
    if registry_uri is None:
        scope = "AzureKeyVaultSecrets"
        prefix = "MLflowWorkspace"
        registry_uri = f"databricks://{scope}:{prefix}"
    mlflow.set_registry_uri(registry_uri)

    return load_model_from_registry_stage(model_name, model_stage, mlflow, lib)

