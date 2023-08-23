import typing_extensions

from seaplane.api.apis.tags import TagValues
from seaplane.api.apis.tags.stream_api import StreamApi
from seaplane.api.apis.tags.flow_api import FlowApi
from seaplane.api.apis.tags.object_api import ObjectApi
from seaplane.api.apis.tags.endpoint_api import EndpointApi

TagToApi = typing_extensions.TypedDict(
    "TagToApi",
    {
        TagValues.STREAM: StreamApi,
        TagValues.FLOW: FlowApi,
        TagValues.OBJECT: ObjectApi,
        TagValues.ENDPOINT: EndpointApi,
    },
)

tag_to_api = TagToApi(
    {
        TagValues.STREAM: StreamApi,
        TagValues.FLOW: FlowApi,
        TagValues.OBJECT: ObjectApi,
        TagValues.ENDPOINT: EndpointApi,
    }
)
