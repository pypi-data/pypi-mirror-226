import typing_extensions

from seaplane.api.paths import PathValues
from seaplane.api.apis.paths.stream import Stream
from seaplane.api.apis.paths.stream_stream_name import StreamStreamName
from seaplane.api.apis.paths.flow import Flow
from seaplane.api.apis.paths.flow_flow_name import FlowFlowName
from seaplane.api.apis.paths.flow_flow_name_secrets import FlowFlowNameSecrets
from seaplane.api.apis.paths.flow_flow_name_secrets_secret_name import (
    FlowFlowNameSecretsSecretName,
)
from seaplane.api.apis.paths.object import Object
from seaplane.api.apis.paths.object_bucket_name import ObjectBucketName
from seaplane.api.apis.paths.object_bucket_name_list import ObjectBucketNameList
from seaplane.api.apis.paths.object_bucket_name_store import ObjectBucketNameStore
from seaplane.api.apis.paths.endpoints_endpoint_request import EndpointsEndpointRequest
from seaplane.api.apis.paths.endpoints_endpoint_response_request_id import (
    EndpointsEndpointResponseRequestId,
)

PathToApi = typing_extensions.TypedDict(
    "PathToApi",
    {
        PathValues.STREAM: Stream,
        PathValues.STREAM_STREAM_NAME: StreamStreamName,
        PathValues.FLOW: Flow,
        PathValues.FLOW_FLOW_NAME: FlowFlowName,
        PathValues.FLOW_FLOW_NAME_SECRETS: FlowFlowNameSecrets,
        PathValues.FLOW_FLOW_NAME_SECRETS_SECRET_NAME: FlowFlowNameSecretsSecretName,
        PathValues.OBJECT: Object,
        PathValues.OBJECT_BUCKET_NAME: ObjectBucketName,
        PathValues.OBJECT_BUCKET_NAME_LIST: ObjectBucketNameList,
        PathValues.OBJECT_BUCKET_NAME_STORE: ObjectBucketNameStore,
        PathValues.ENDPOINTS_ENDPOINT_REQUEST: EndpointsEndpointRequest,
        PathValues.ENDPOINTS_ENDPOINT_RESPONSE_REQUEST_ID: EndpointsEndpointResponseRequestId,
    },
)

path_to_api = PathToApi(
    {
        PathValues.STREAM: Stream,
        PathValues.STREAM_STREAM_NAME: StreamStreamName,
        PathValues.FLOW: Flow,
        PathValues.FLOW_FLOW_NAME: FlowFlowName,
        PathValues.FLOW_FLOW_NAME_SECRETS: FlowFlowNameSecrets,
        PathValues.FLOW_FLOW_NAME_SECRETS_SECRET_NAME: FlowFlowNameSecretsSecretName,
        PathValues.OBJECT: Object,
        PathValues.OBJECT_BUCKET_NAME: ObjectBucketName,
        PathValues.OBJECT_BUCKET_NAME_LIST: ObjectBucketNameList,
        PathValues.OBJECT_BUCKET_NAME_STORE: ObjectBucketNameStore,
        PathValues.ENDPOINTS_ENDPOINT_REQUEST: EndpointsEndpointRequest,
        PathValues.ENDPOINTS_ENDPOINT_RESPONSE_REQUEST_ID: EndpointsEndpointResponseRequestId,
    }
)
