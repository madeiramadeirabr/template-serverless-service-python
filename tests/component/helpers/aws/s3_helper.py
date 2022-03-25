"""
S3 Helper module for test resources
Version: 1.0.0
"""
import os

from flambda_app.aws.s3 import S3


class S3Helper:
    _s3 = None

    @classmethod
    def download_file(cls, bucket_name, object_name, file_name):
        # keep one instance only
        if cls._s3 is None:
            cls._s3 = S3()
        return cls._s3.download_file(file_name, bucket_name, object_name)

    @classmethod
    def upload_file(cls, file_name, bucket_name, object_name=None):
        # keep one instance only
        if cls._s3 is None:
            cls._s3 = S3()
        return cls._s3.upload_file(file_name, bucket_name, object_name)

    @classmethod
    def event_to_dict(cls, event):
        pass

    @classmethod
    def delete_bucket(cls, bucket_url):
        # keep one instance only
        if cls._s3 is None:
            cls._s3 = S3()
        bucket_name = cls.get_bucket(bucket_url)
        return cls._s3.delete_bucket(bucket_name)

    @classmethod
    def create_bucket(cls, bucket_name, attributes=None):
        # keep one instance only
        if cls._s3 is None:
            cls._s3 = S3()
        return cls._s3.create_bucket(bucket_name)

    @classmethod
    def get_bucket(cls, bucket_name):
        # keep one instance only
        if cls._s3 is None:
            cls._s3 = S3()
        return cls._s3.get_bucket(bucket_name)
