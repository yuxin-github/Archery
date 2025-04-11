# utils/obs_utils.py
import time

from obs import ObsClient
from django.conf import settings


def get_obs_client():
    """获取 OBS 客户端"""
    return ObsClient(
        access_key_id=settings.OBS_CONFIG['access_key_id'],
        secret_access_key=settings.OBS_CONFIG['secret_access_key'],
        server=settings.OBS_CONFIG['server']
    )


def upload_to_obs(file_path, object_name=None):
    """上传文件到 OBS"""
    client = get_obs_client()

    if not object_name:
        object_name = f"{time.time()}-{file_path.split('/')[-1]} "  # 默认使用时间戳-文件名

    resp = client.putFile(
        bucketName=settings.OBS_CONFIG['bucket_name'],
        objectKey=object_name,
        file_path=file_path
    )

    if resp.status >= 300:
        raise Exception(f"OBS Upload Failed: {resp.reason}")

    return resp.body.objectUrl
