from seaplane.api.paths.object_bucket_name_store.get import ApiForget
from seaplane.api.paths.object_bucket_name_store.put import ApiForput
from seaplane.api.paths.object_bucket_name_store.delete import ApiFordelete


class ObjectBucketNameStore(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
