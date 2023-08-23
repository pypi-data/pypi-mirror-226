from seaplane.api.paths.flow_flow_name.get import ApiForget
from seaplane.api.paths.flow_flow_name.put import ApiForput
from seaplane.api.paths.flow_flow_name.delete import ApiFordelete


class FlowFlowName(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
