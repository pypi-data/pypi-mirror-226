import requests
import json

def create_completion(prompt: str, modelUuid: str, apiKey: str, stream: bool=False, n_samples: int=1):
    """
    向指定模型发送文本提示，获取生成的推理结果（Completion）。

    这个函数会向 FastModels API 发送一个 POST 请求，请求内容包含一个文本提示、模型的 UUID、
    授权API KEY、是否使用流式相应、返回结果的数量，然后返回 API 的响应。

    Args:
        prompt (str): 要发送给模型的文本提示。
        modelUuid (str): 要使用的模型的 UUID。
        apiKey (str): 授权的API KEY。
        stream (bool): 是否使用流式响应, 默认不使用。
        n_samples (int): 返回结果的数量, 默认为1。

    Returns:
        list[dict]: API 的 JSON 响应列表，包含生成的完成。

    Raises:
        requests.exceptions.RequestException: 如果请求失败。
    """
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {apiKey}'}
    data = json.dumps({'prompt': prompt, 'model_uuid': modelUuid, 'stream': stream, 'n_samples': n_samples})
    response = requests.post(
        'https://www.fastmodels.cn/api/v1/completions',
        headers=headers,
        data=data,
    )

    if stream:
        response_json_list = []
        for line in response.iter_lines():
            decoded_line = line.decode('utf-8')
            try:
                # remove the "data:" prefix if it exists
                json_start = decoded_line.find('{')
                if json_start > 0:
                    decoded_line = decoded_line[json_start:]

                # Parse the JSON line and add it to the result list
                json_line = json.loads(decoded_line)
                response_json_list.append(json_line)
            except json.JSONDecodeError:
                pass

        return response_json_list
    
    else:
        # If not streaming, just return the JSON response
        return [response.json()]
