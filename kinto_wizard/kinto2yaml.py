from kinto_http import exceptions as kinto_exceptions
from .logger import logger


def _sorted_principals(permissions):
    return {perm: sorted(principals) for perm, principals in permissions.items()}


def introspect_server(client, full=False):
    logger.info("Fetch buckets list.")
    buckets = client.get_buckets()
    return {
        bucket['id']: introspect_bucket(client, bucket['id'], full=full)
        for bucket in buckets
    }


def introspect_bucket(client, bid, full=False):
    logger.info("Fetch information of bucket {!r}".format(bid))
    try:
        bucket = client.get_bucket(bucket=bid)
    except kinto_exceptions.BucketNotFound:
        logger.error("Could not read bucket {!r}".format(bid))
        return None

    permissions = bucket.get('permissions', {})
    if len(permissions) == 0:
        error_msg = 'Could not read permissions of bucket {!r}'.format(bid)
        raise kinto_exceptions.KintoException(error_msg)

    collections = client.get_collections(bucket=bid)
    groups = client.get_groups(bucket=bid)
    result = {
        'permissions': _sorted_principals(permissions),
        'collections': {
            collection['id']: introspect_collection(client, bid, collection['id'], full=full)
            for collection in collections
        },
        'groups': {
            group['id']: introspect_group(client, bid, group['id'], full=full)
            for group in groups
        }
    }
    if full:
        result['data'] = bucket['data']
    return result


def introspect_collection(client, bid, cid, full=False):
    logger.info("Fetch information of collection {!r}/{!r}".format(bid, cid))
    collection = client.get_collection(bucket=bid, collection=cid)
    result = {
        'permissions': _sorted_principals(collection['permissions']),
    }
    if full:
        result['data'] = collection['data']
    return result


def introspect_group(client, bid, gid, full=False):
    logger.info("Fetch information of group {!r}/{!r}".format(bid, gid))
    group = client.get_group(bucket=bid, group=gid)
    result = {
        'permissions': _sorted_principals(group['permissions'])
    }
    data = group['data'] if full else {}
    data['members'] = sorted(group['data']['members'])
    result['data'] = data
    return result
