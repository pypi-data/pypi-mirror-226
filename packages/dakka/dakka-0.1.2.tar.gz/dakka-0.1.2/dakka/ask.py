import re
import requests
import json
from itertools import chain
from dakka.openapi_spec import OpenAPISpec, openapi_spec_to_openai_fn
from openapi_schema_pydantic import Parameter
from openai import ChatCompletion

from dakka.agent_logger import AGENT_LOGGER


def process_question(question, enabled_specs, config, verbose=True):
    """Determine the endpoint based on the question and the enabled specs."""

    fname_to_spec_func = {}
    ai_functions = []
    spec_func = {}
    for spec in enabled_specs[1:]:
        ai_func, func = openapi_spec_to_openai_fn(OpenAPISpec.from_spec_dict(spec))

        spec_name = spec['info']['title']
        spec_func[spec_name] = func
        for func_desc in ai_func:
            fname_to_spec_func[func_desc['name']] = (spec_name, func)
            ai_functions.append(func_desc)


    messages=[
        {
            "role": "system",
            "content": "You are a friendly AI. Your task is to help the user, using the tools available to you."
        },
        {
            "role": "user",
            "content": question,
        }
    ]

    while True:
        response = ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.1,
            function_call="auto",
            api_key=config["openai_key"],
            functions=ai_functions
        )

        choice = response['choices'][0]
        finish_reason = choice['finish_reason']
        
        message = choice['message']
        messages.append(message.to_dict())
        if verbose:
            AGENT_LOGGER.info(f"[GPT] message: {str(message)}")
        
        if finish_reason == 'function_call':
            function_call = message['function_call']
            f_name = function_call['name']
            arguments = json.loads(function_call['arguments'])
            (spec_name, func_to_call) = fname_to_spec_func[f_name]
            result = func_to_call(f_name, arguments, headers={"content-type": "application/json"})
            
            if verbose:
                AGENT_LOGGER.warn(f"[FUNC] ({spec_name}) {f_name} called with: {str(arguments)}")
            
            function_message = {
                "role": "function",
                "name": f_name,
                "content": result
            }
            if verbose:
                AGENT_LOGGER.warn(f"[FUNC] ({spec_name}) {f_name} returned: {str(function_message)}")
                
            messages.append(function_message)
        elif finish_reason == 'stop':
            return messages
        else:
            AGENT_LOGGER.critical(f"[GPT] Unknown finish_reason: {finish_reason}")
            return "Failed to complete"