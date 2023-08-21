from collections import defaultdict
import copy
import json
import re
from typing import Any, Callable, Dict, Optional, Self, Union, List, Tuple
from click import Parameter, Path

import openapi_spec_validator
import requests
import yaml

from openapi_schema_pydantic import (
    Components,
    Operation,
    Parameter,
    PathItem,
    Paths,
    Reference,
    RequestBody,
    Schema,
)
from openapi_schema_pydantic import OpenAPI, Operation, Reference, RequestBody, Schema
import logging

logger = logging.getLogger(__name__)

DUMMY_KEY = "dummyKey"

"""
Credit: https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/utilities/openapi.py
"""
class OpenAPISpec(OpenAPI):
    """OpenAPI Model that removes mis-formatted parts of the spec."""

    @property
    def _paths_strict(self) -> Paths:
        if not self.paths:
            raise ValueError("No paths found in spec")
        return self.paths

    def _get_path_strict(self, path: str) -> PathItem:
        path_item = self._paths_strict.get(path)
        if not path_item:
            raise ValueError(f"No path found for {path}")
        return path_item

    @property
    def _components_strict(self) -> Components:
        """Get components or err."""
        if self.components is None:
            raise ValueError("No components found in spec. ")
        return self.components

    @property
    def _parameters_strict(self) -> Dict[str, Union[Parameter, Reference]]:
        """Get parameters or err."""
        parameters = self._components_strict.parameters
        if parameters is None:
            raise ValueError("No parameters found in spec. ")
        return parameters

    @property
    def _schemas_strict(self) -> Dict[str, Schema]:
        """Get the dictionary of schemas or err."""
        schemas = self._components_strict.schemas
        if schemas is None:
            raise ValueError("No schemas found in spec. ")
        return schemas

    @property
    def _request_bodies_strict(self) -> Dict[str, Union[RequestBody, Reference]]:
        """Get the request body or err."""
        request_bodies = self._components_strict.requestBodies
        if request_bodies is None:
            raise ValueError("No request body found in spec. ")
        return request_bodies

    def _get_referenced_parameter(
        self, ref: Reference
    ) -> Union[Parameter, Reference]:
        """Get a parameter (or nested reference) or err."""
        ref_name = ref.ref.split("/")[-1]
        parameters = self._parameters_strict
        if ref_name not in parameters:
            raise ValueError(f"No parameter found for {ref_name}")
        return parameters[ref_name]

    def _get_root_referenced_parameter(self, ref: Reference) -> Parameter:
        """Get the root reference or err."""
        from openapi_schema_pydantic import Reference

        parameter = self._get_referenced_parameter(ref)
        while isinstance(parameter, Reference):
            parameter = self._get_referenced_parameter(parameter)
        return parameter

    def get_referenced_schema(self, ref: Reference) -> Schema:
        """Get a schema (or nested reference) or err."""
        ref_name = ref.ref.split("/")[-1]
        schemas = self._schemas_strict
        if ref_name not in schemas:
            raise ValueError(f"No schema found for {ref_name}")
        return schemas[ref_name]

    def get_schema(self, schema: Union[Reference, Schema]) -> Schema:
        from openapi_schema_pydantic import Reference

        if isinstance(schema, Reference):
            return self.get_referenced_schema(schema)
        return schema

    def _get_root_referenced_schema(self, ref: Reference) -> Schema:
        """Get the root reference or err."""
        from openapi_schema_pydantic import Reference

        schema = self.get_referenced_schema(ref)
        while isinstance(schema, Reference):
            schema = self.get_referenced_schema(schema)
        return schema

    def _get_referenced_request_body(
        self, ref: Reference
    ) -> Optional[Union[Reference, RequestBody]]:
        """Get a request body (or nested reference) or err."""
        ref_name = ref.ref.split("/")[-1]
        request_bodies = self._request_bodies_strict
        if ref_name not in request_bodies:
            raise ValueError(f"No request body found for {ref_name}")
        return request_bodies[ref_name]

    def _get_root_referenced_request_body(
        self, ref: Reference
    ) -> Optional[RequestBody]:
        """Get the root request Body or err."""
        from openapi_schema_pydantic import Reference

        request_body = self._get_referenced_request_body(ref)
        while isinstance(request_body, Reference):
            request_body = self._get_referenced_request_body(request_body)
        return request_body

    @staticmethod
    def _alert_unsupported_spec(obj: dict) -> None:
        """Alert if the spec is not supported."""
        warning_message = (
            " This may result in degraded performance."
            + " Convert your OpenAPI spec to 3.1.* spec"
            + " for better support."
        )
        swagger_version = obj.get("swagger")
        openapi_version = obj.get("openapi")
        if isinstance(openapi_version, str):
            if openapi_version != "3.1.0":
                logger.warning(
                    f"Attempting to load an OpenAPI {openapi_version}"
                    f" spec. {warning_message}"
                )
            else:
                pass
        elif isinstance(swagger_version, str):
            logger.warning(
                f"Attempting to load a Swagger {swagger_version}"
                f" spec. {warning_message}"
            )
        else:
            raise ValueError(
                "Attempting to load an unsupported spec:"
                f"\n\n{obj}\n{warning_message}"
            )

    @classmethod
    def parse_obj(cls, obj: dict) -> Self:
        try:
            cls._alert_unsupported_spec(obj)
            return super().parse_obj(obj)
        except Exception as e:
            # We are handling possibly misconfigured specs and
            # want to do a best-effort job to get a reasonable interface out of it.
            new_obj = copy.deepcopy(obj)
            for error in e.errors():
                keys = error["loc"]
                item = new_obj
                for key in keys[:-1]:
                    item = item[key]
                item.pop(keys[-1], None)
            return cls.parse_obj(new_obj)

    @classmethod
    def from_spec_dict(cls, spec_dict: dict) -> Self:
        """Get an OpenAPI spec from a dict."""
        return cls.parse_obj(spec_dict)

    @classmethod
    def from_text(cls, text: str) -> Self:
        """Get an OpenAPI spec from a text."""
        try:
            spec_dict = json.loads(text)
        except json.JSONDecodeError:
            spec_dict = yaml.safe_load(text)
        return cls.from_spec_dict(spec_dict)

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> Self:
        """Get an OpenAPI spec from a file path."""
        path_ = path if isinstance(path, Path) else Path(path)
        if not path_.exists():
            raise FileNotFoundError(f"{path} does not exist")
        with path_.open("r") as f:
            return cls.from_text(f.read())

    @classmethod
    def from_url(cls, url: str) -> openapi_spec_validator:
        """Get an OpenAPI spec from a URL."""
        response = requests.get(url)
        return cls.from_text(response.text)

    @property
    def base_url(self) -> str:
        """Get the base url."""
        return self.servers[0].url

    def get_methods_for_path(self, path: str) -> List[str]:
        """Return a list of valid methods for the specified path."""
        from openapi_schema_pydantic import Operation

        path_item = self._get_path_strict(path)
        results = []
        for method in ["get", "put", "post", "delete"]:
            operation = getattr(path_item, method, None)
            if isinstance(operation, Operation):
                results.append(method)
        return results

    def get_parameters_for_path(self, path: str) -> List[Parameter]:
        from openapi_schema_pydantic import Reference

        path_item = self._get_path_strict(path)
        parameters = []
        if not path_item.parameters:
            return []
        for parameter in path_item.parameters:
            if isinstance(parameter, Reference):
                parameter = self._get_root_referenced_parameter(parameter)
            parameters.append(parameter)
        return parameters

    def get_operation(self, path: str, method: str) -> Operation:
        """Get the operation object for a given path and HTTP method."""
        from openapi_schema_pydantic import Operation

        path_item = self._get_path_strict(path)
        operation_obj = getattr(path_item, method, None)
        if not isinstance(operation_obj, Operation):
            raise ValueError(f"No {method} method found for {path}")
        return operation_obj

    def get_parameters_for_operation(self, operation: Operation) -> List[Parameter]:
        """Get the components for a given operation."""
        from openapi_schema_pydantic import Reference

        parameters = []
        if operation.parameters:
            for parameter in operation.parameters:
                if isinstance(parameter, Reference):
                    parameter = self._get_root_referenced_parameter(parameter)
                parameters.append(parameter)
        return parameters

    def get_request_body_for_operation(
        self, operation: Operation
    ) -> Optional[RequestBody]:
        """Get the request body for a given operation."""
        from openapi_schema_pydantic import Reference

        request_body = operation.requestBody
        if isinstance(request_body, Reference):
            request_body = self._get_root_referenced_request_body(request_body)
        return request_body

    @staticmethod
    def get_cleaned_operation_id(
        operation: Operation, path: str, method: str
    ) -> str:
        """Get a cleaned operation id from an operation id."""
        operation_id = operation.operationId
        if operation_id is None:
            # Replace all punctuation of any kind with underscore
            path = re.sub(r"[^a-zA-Z0-9]", "_", path.lstrip("/"))
            operation_id = f"{path}_{method}"
        return operation_id.replace("-", "_").replace(".", "_").replace("/", "_")


"""
The following methods were heavily stolen from https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/chains/openai_functions/openapi.py
"""
def _format_url(url: str, path_params: dict) -> str:
    expected_path_param = re.findall(r"{(.*?)}", url)
    new_params = {}
    for param in expected_path_param:
        clean_param = param.lstrip(".;").rstrip("*")
        val = path_params[clean_param]
        if isinstance(val, list):
            if param[0] == ".":
                sep = "." if param[-1] == "*" else ","
                new_val = "." + sep.join(val)
            elif param[0] == ";":
                sep = f"{clean_param}=" if param[-1] == "*" else ","
                new_val = f"{clean_param}=" + sep.join(val)
            else:
                new_val = ",".join(val)
        elif isinstance(val, dict):
            kv_sep = "=" if param[-1] == "*" else ","
            kv_strs = [kv_sep.join((k, v)) for k, v in val.items()]
            if param[0] == ".":
                sep = "."
                new_val = "."
            elif param[0] == ";":
                sep = ";"
                new_val = ";"
            else:
                sep = ","
                new_val = ""
            new_val += sep.join(kv_strs)
        else:
            if param[0] == ".":
                new_val = f".{val}"
            elif param[0] == ";":
                new_val = f";{clean_param}={val}"
            else:
                new_val = val
        new_params[param] = new_val
    return url.format(**new_params)

def _openapi_params_to_json_schema(params: List[Parameter], spec: OpenAPISpec, with_param_desc=False) -> dict:
    properties = {}
    required = []
    for p in params:
        if p.param_schema:
            schema = spec.get_schema(p.param_schema)
        else:
            media_type_schema = list(p.content.values())[0].media_type_schema  # type: ignore  # noqa: E501
            schema = spec.get_schema(media_type_schema)
        if p.description and with_param_desc:
            schema.description = p.description
        properties[p.name] = json.loads(schema.json(exclude_none=True))
        if p.required:
            required.append(p.name)

    schema = {
        "type": schema.type or "string", 
        "required": required
    }

    if spec.enum:
        schema["enum"] = spec.enum
    if len(properties):
        schema["properties"] = properties

    return schema

def openapi_spec_to_openai_fn(
    spec: OpenAPISpec,
) -> Tuple[List[Dict[str, Any]], Callable]:
    """Convert a valid OpenAPI spec to the JSON Schema format expected for OpenAI
        functions.

    Args:
        spec: OpenAPI spec to convert.

    Returns:
        Tuple of the OpenAI functions JSON schema and a default function for executing
            a request based on the OpenAI function schema.
    """
    if not spec.paths:
        return [], lambda: None
    functions = []
    _name_to_call_map = {}
    for path in spec.paths:
        path_params = {
            (p.name, p.param_in): p for p in spec.get_parameters_for_path(path)
        }
        for method in spec.get_methods_for_path(path):
            request_args = {}
            op = spec.get_operation(path, method)
            op_params = path_params.copy()
            for param in spec.get_parameters_for_operation(op):
                op_params[(param.name, param.param_in)] = param
            params_by_type = defaultdict(list)
            for name_loc, p in op_params.items():
                params_by_type[name_loc[1]].append(p)
            param_loc_to_arg_name = {
                "query": "params",
                "header": "headers",
                "cookie": "cookies",
                "path": "path_params",
            }
            for param_loc, arg_name in param_loc_to_arg_name.items():
                if params_by_type[param_loc]:
                    request_args[arg_name] = _openapi_params_to_json_schema(
                        params_by_type[param_loc], spec
                    )
            request_body = spec.get_request_body_for_operation(op)
            # TODO: Support more MIME types.
            if request_body and request_body.content:
                media_types = {}
                
                for media_type, media_type_object in request_body.content.items():
                    if media_type_object.media_type_schema:
                        schema = spec.get_schema(media_type_object.media_type_schema)
                        media_types[media_type] = json.loads(
                            schema.json(exclude_none=True)
                        )
                if not media_types['application/json']:
                    logger.warn(f"Unable to use method: {op.operationId} because it doesn't take JSON")
                    continue

                request_args = media_types['application/json']

            fn = {
                "name": op.operationId,
                "description": op.description or op.summary,
            }
            if request_args:
                fn["parameters"] = request_args
                if request_args.get("required", None):
                    fn["required"] = request_args["required"]
            else:
                fn["parameters"] = { 
                    "type": "object", 
                    "properties": {
                        DUMMY_KEY: { 
                            "type": "null"
                        }
                    }
                }
            functions.append(fn)
            _name_to_call_map[fn["name"]] = {
                "method": method,
                "url": spec.base_url + path
            }

    def default_call_api(
        name: str,
        fn_args: dict,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs: Any,
    ) -> Any:
        method = _name_to_call_map[name]["method"]
        url = _name_to_call_map[name]["url"]
        path_params = fn_args.pop("path_params", {})
        url = _format_url(url, path_params)
        request_args = {}
        if DUMMY_KEY not in fn_args and isinstance(fn_args, dict):
            request_args["data"] = json.dumps(fn_args)
        
        _kwargs = {**request_args, **kwargs}
        if headers is not None:
            if "headers" in _kwargs:
                _kwargs["headers"].update(headers)
            else:
                _kwargs["headers"] = headers
        if params is not None:
            if "params" in _kwargs:
                _kwargs["params"].update(params)
            else:
                _kwargs["params"] = params
        result = requests.request(method.upper(), url, **_kwargs)
        if result.status_code != 200:
            return f"Error: {result.status_code} {result.reason}"
        return result.text


    return functions, default_call_api
