import os
from typing import Dict

import requests
import dotenv


# Load environment variables
dotenv.load_dotenv(".env", override=True)
required_environment_variables = [
    "TWINLAB_SERVER",
    "TWINLAB_KEY",
    "TWINLAB_USER",  # TODO: Remove eventually
]
for environment_variable in required_environment_variables:
    if not os.getenv(environment_variable):
        raise ValueError(f"{environment_variable} not set in .env")
TWINLAB_SERVER: str = os.getenv("TWINLAB_SERVER")

### Helper functions ###


def _create_headers(verbose=False) -> Dict[str, str]:
    headers = {
        # TODO: Remove when authentication is working
        "X-User": os.getenv("TWINLAB_USER"),
        "X-API_Key": os.getenv("TWINLAB_KEY"),
        "X-Language": "python",
    }
    verbose_str = "true" if verbose else "false"
    headers["X-Verbose"] = verbose_str
    return headers


def get_response_body(response: requests.Response) -> dict | str:
    # TODO: Use attribute of response to check if json/text
    try:
        return response.json()
    except:
        return response.text

###  ###

### API ###


def get_user(verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/user"
    headers = _create_headers(verbose=verbose)
    response = requests.get(url, headers=headers)
    body = get_response_body(response)
    return body


def get_versions(verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/versions"
    headers = _create_headers(verbose=verbose)
    response = requests.get(url, headers=headers)
    body = get_response_body(response)
    return body


def generate_upload_url(dataset_id: str, verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/upload_url/{dataset_id}"
    headers = _create_headers(verbose=verbose)
    response = requests.get(url, headers=headers)
    body = get_response_body(response)
    return body


def process_uploaded_dataset(dataset_id: str, verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/datasets/{dataset_id}"
    headers = _create_headers(verbose=verbose)
    response = requests.post(url, headers=headers)
    body = get_response_body(response)
    return body


def upload_dataset(dataset_id: str, data_csv: str, verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/datasets/{dataset_id}"
    headers = _create_headers(verbose=verbose)
    request_body = {"dataset": data_csv}
    response = requests.put(url, headers=headers, json=request_body)
    body = get_response_body(response)
    return body


def list_datasets(verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/datasets"
    headers = _create_headers(verbose=verbose)
    response = requests.get(url, headers=headers)
    body = get_response_body(response)
    return body


def view_dataset(dataset_id: str, verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/datasets/{dataset_id}"
    headers = _create_headers(verbose=verbose)
    response = requests.get(url, headers=headers)
    body = get_response_body(response)
    return body


def summarise_dataset(dataset_id: str, verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/datasets/{dataset_id}/summarise"
    headers = _create_headers(verbose=verbose)
    response = requests.get(url, headers=headers)
    body = get_response_body(response)
    return body


def delete_dataset(dataset_id: str, verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/datasets/{dataset_id}"
    headers = _create_headers(verbose=verbose)
    response = requests.delete(url, headers=headers)
    body = get_response_body(response)
    return body


def train_model(model_id: str, parameters_json: str, processor: str, verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/models/{model_id}"
    headers = _create_headers(verbose=verbose)
    headers["X-Processor"] = processor
    request_body = {
        # TODO: Add dataset_id and dataset_std_id as keys?
        # TODO: Split this into model_params/train_params as in twinLab?
        "parameters": parameters_json,
    }
    response = requests.put(url, headers=headers, json=request_body)
    body = get_response_body(response)
    return body


def list_models(verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/models"
    headers = _create_headers(verbose=verbose)
    response = requests.get(url, headers=headers)
    body = get_response_body(response)
    return body


def get_status_model(model_id: str, verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/models/{model_id}"
    headers = _create_headers(verbose=verbose)
    response = requests.get(url, headers=headers)
    body = get_response_body(response)
    return body


def view_model(model_id: str, verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/models/{model_id}/view"
    headers = _create_headers(verbose=verbose)
    response = requests.get(url, headers=headers)
    body = get_response_body(response)
    return body


def summarise_model(model_id: str, verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/models/{model_id}/summarise"
    headers = _create_headers(verbose=verbose)
    response = requests.get(url, headers=headers)
    body = get_response_body(response)
    return body


def use_model(model_id: str, eval_csv: str, method: str, processor: str, verbose=False, **kwargs) -> dict:
    url = f"{TWINLAB_SERVER}/models/{model_id}/{method}"
    headers = _create_headers(verbose=verbose)
    headers["X-Processor"] = processor
    request_body = {
        "dataset": eval_csv,  #  TODO: Should this be a dataset_id from an upload?
        "parameters": kwargs,  # To be passed to the method of campaign
    }
    response = requests.post(url, headers=headers, json=request_body)
    body = get_response_body(response)
    return body


def delete_model(model_id: str, verbose=False) -> dict:
    url = f"{TWINLAB_SERVER}/models/{model_id}"
    headers = _create_headers(verbose=verbose)
    response = requests.delete(url, headers=headers)
    body = get_response_body(response)
    return body

### ###
