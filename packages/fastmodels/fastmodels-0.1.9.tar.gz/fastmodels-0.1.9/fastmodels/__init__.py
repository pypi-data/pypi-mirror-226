import os
from fastmodels.utils.modelclient import create_completion as _create_completion

def set_apikey(api_key: str):
    """
    Set the FASTMODELS_API_KEY environment variable.

    Args:
        api_key (str): The FastModels API key.
    """
    os.environ['FASTMODELS_API_KEY'] = api_key

def complete(prompt: str, model_uuid: str, stream: bool=False, n_samples: int=1):
    """
    Inference by sending a prompt to a specific model.

    Args:
        prompt (str): The prompt to send to model.
        model_uuid (str): The ID of the model to use.
        stream (bool): Whether to use streaming response. Default is False.
        n_samples (int): Number of results returned. Default is 1.

    Returns:
        list[dict]: The API's JSON response containing the completion.

    Raises:
        ValueError: FASTMODELS_API_KEY is not defined.
    """
    api_key = os.getenv('FASTMODELS_API_KEY')
    if api_key is None:
        raise ValueError("Please set the API key FASTMODELS_API_KEY using fastmodels.set_apikey.")
    response_json_list = _create_completion(prompt, model_uuid, api_key, stream, n_samples)
    return response_json_list

__all__ = ['set_apikey', 'complete']