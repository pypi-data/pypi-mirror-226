from seaplane.api.paths.stream_stream_name.get import ApiForget
from seaplane.api.paths.stream_stream_name.put import ApiForput
from seaplane.api.paths.stream_stream_name.delete import ApiFordelete


class StreamStreamName(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
