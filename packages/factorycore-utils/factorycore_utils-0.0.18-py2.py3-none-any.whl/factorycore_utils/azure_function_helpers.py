from factorycore_utils.dbutils_helper import *

def call_factoryCORE_function(spark, method, function_name, query_string=None, body=None):
    # Call an factory.CORE Azure Function using either an Http Get or Post and return the Response object

    # Parameters:
    # spark - Spark context.
    # method - 'get' or 'post'
    # function_name - Name of the Azure Function
    # query_string - The query string to use with a 'get' method. Default None.
    # body - The body string to use with a 'post' method. Default None.
    
    import requests

    # Get secrets from Key Vault
    secret_scope = "AzureKeyVaultSecrets"
    dbutils = get_dbutils(spark)
    azure_function_url = dbutils.secrets.get(scope = secret_scope, key = "FactoryCoreFunctionUrl")
    azure_function_key = dbutils.secrets.get(scope = secret_scope, key = "FactoryCoreFunctionKey")

    # Construct the HTTP Header
    headers = { 
              'content-type': 'application/json', 
              'x-functions-key': f'{azure_function_key}' 
            }

    # Construct the URL
    url = f"{azure_function_url}/api/{function_name}" + (("?" + query_string) if query_string else "")

    if method == "get":
        response = requests.get(url, headers=headers)
    elif method == "post":
        response = requests.post(url, data=body, headers=headers)
    else:
        response = None

    return response


def send_email(spark, recipients, subject, message):
    # Send a custom email to a recipient list by calling an Azure Function

    # Parameters:
    # spark - Spark context.
    # recipients - Semi-colon separated list of recipients to send the email to
    # subject - Email subject
    # message - HTML-enabled email message

    body = f"""
    {{
        "NotificationType": "CustomEmail",
        "EmailRecipients": "{recipients}",
        "EmailSubject": "{subject}",
        "EmailMessage": "{message}"
    }}  
    """  

    resp = call_factoryCORE_function(spark, "post", "SendNotification", body=body)      
    resp.raise_for_status()


def record_notebook_run_url(spark, task_run_key, notebook_context, workspace_url, property_name):
    # Record the Notebook Run URL in the RunOrchestrationDetails column of the TaskRun record.

    # Parameters:
    # spark - Spark context.
    # task_run_key - The identifier of the TaskRun record.
    # notebook_context - The Context of the Notebook - we will lookup values within this context to derive the URL.
    # workspace_url - The URL of the Workspace.
    # property_name - The name of the Property to assign the Notebook Run URL to.

    notebook_run_url = f"https://{workspace_url}/?o={notebook_context['tags']['orgId']}#job/{notebook_context['tags']['jobId']}/run/{notebook_context['tags']['idInJob']}"

    body = f"""
    {{
        "TaskRunKey": {task_run_key},
        "PropertyKey": "{property_name}",
        "PropertyValue": "{notebook_run_url}"
    }}  
    """  

    resp = call_factoryCORE_function(spark, "post", "UpdateTaskRunOrchestration", body=body)
    resp.raise_for_status()


def set_task_run_result(spark, task_run_key, run_status_code, run_result):
    # Set the Result of the Task Run.

    # Parameters:
    # spark - Spark context.
    # task_run_key - The identifier of the TaskRun record.
    # run_status_code - The code for the Run Status.
    # run_result - The result of the Run.

    body = f"""
    {{
        "TaskRunKey": {task_run_key},
        "RunStatusCode": "{run_status_code}",
        "Result": "{run_result}"
    }}  
    """  

    resp = call_factoryCORE_function(spark, "post", "SetTaskRunResult", body=body)
    resp.raise_for_status()


def update_task_run_output(spark, task_run_key, property_key, property_value):
    # Add a JSON property to the Task Run Output.

    # Parameters:
    # spark - Spark context.
    # task_run_key - The identifier of the TaskRun record.
    # property_key - The key for the JSON Property to add to the Task Run Output.
    # property_value - The value of the JSON Property.

    body = f"""
    {{
        "TaskRunKey": {task_run_key},
        "PropertyKey": "{property_key}",
        "PropertyValue": "{property_value}"
    }}  
    """  

    resp = call_factoryCORE_function(spark, "post", "UpdateTaskRunOutput", body=body)
    resp.raise_for_status()


def update_state_config(spark, task_run_key, property_key, property_value):
    # Add/Update the JSON property in the StateConfig of the Task State.

    # Parameters:
    # spark - Spark context.
    # task_run_key - The identifier of the TaskRun record.
    # property_key - The key for the JSON Property to add to the StateConfig column.
    # property_value - The value of the JSON Property.

    body = f"""
    {{
        "TaskRunKey": {task_run_key},
        "PropertyKey": "{property_key}",
        "PropertyValue": "{property_value}"
    }}  
    """  

    resp = call_factoryCORE_function(spark, "post", "UpdateStateConfig", body=body)
    resp.raise_for_status()
