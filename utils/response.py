from typing import Any

def get_response(message="", data={}, code=40000):
    return {
        "code": code,
        "message": message,
        "data": data,
    }


from rest_framework.response import Response
from rest_framework.serializers import Serializer


class APIResponse(Response):
    def __init__(
        self,
        data:dict[str, Any]={},
        code:int=None,
        msg:str=None,
        status:int=None,
        template_name=None,
        headers=None,
        exception:bool=False,
        content_type=None,
        **kwargs
    ):
        super().__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                "You passed a Serializer instance as data, but "
                "probably meant to pass serialized `.data` or "
                "`.error`. representation."
            )
            raise AssertionError(msg)
        self.data = {"code": code, "message": msg, "data": data}
        self.data.update(kwargs)
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value
