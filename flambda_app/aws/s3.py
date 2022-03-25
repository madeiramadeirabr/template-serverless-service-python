"""
AWS S3 Module
Version: 1.0.1
"""
import os

import boto3

from flambda_app import helper
from flambda_app.aws import change_endpoint
from flambda_app.config import get_config
from flambda_app.logging import get_logger

_RETRY_COUNT = 0
_MAX_RETRY_ATTEMPTS = 3


class S3:
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Bucket.upload_file
    """

    def __init__(self, logger=None, config=None, profile=None, session=None):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # last_exception
        self.exception = None
        # profile
        self.profile = profile if profile is not None else \
            os.environ['AWS_PROFILE'] if 'AWS_PROFILE' in os.environ else None
        # session
        self.session = session if session is not None else \
            boto3.session.Session(profile_name=self.profile)

        self.connection = None

    def connect(self, retry=False):
        global _RETRY_COUNT, _MAX_RETRY_ATTEMPTS
        connection = self.connection
        if connection is None:
            try:
                endpoint_url = self.config.get('LOCALSTACK_ENDPOINT', None)
                region_name = self.config.get('REGION_NAME', 'us-east-2')
                bucket_name = self.config.get('APP_BUCKET', None)

                self.logger.debug('S3 - profile: {}'.format(self.profile))
                self.logger.debug('S3 - endpoint_url: {}'.format(endpoint_url))
                self.logger.debug('S3 - bucket_name: {}'.format(bucket_name))
                self.logger.debug('S3 - region_name: {}'.format(region_name))

                if self.profile:
                    session = self.session
                    connection = session.resource(
                        's3',
                        endpoint_url=endpoint_url,
                        region_name=self.config.REGION_NAME
                    )
                else:
                    connection = boto3.resource(
                        's3',
                        endpoint_url=endpoint_url,
                        region_name=self.config.REGION_NAME
                    )

                try:
                    bucket = connection.Bucket(bucket_name)
                    connection.meta.client.list_buckets()

                    if bucket is None:
                        raise Exception("Unable to read bucket")
                except Exception as err:
                    if helper.has_attr(err, "response") and err.response['Error']:
                        self.logger.debug('S3 - Connected')
                        self.logger.error(err)
                    else:
                        connection = None
                        raise err

                _RETRY_COUNT = 0
                self.connection = connection

            except Exception as err:
                if _RETRY_COUNT == _MAX_RETRY_ATTEMPTS:
                    _RETRY_COUNT = 0
                    self.logger.error(err)
                    connection = None
                    self.connection = connection
                else:
                    self.logger.error(err)
                    self.logger.info('Trying to reconnect... {}'.format(_RETRY_COUNT))
                    # retry
                    if not retry:
                        _RETRY_COUNT += 1
                        change_endpoint(self)
                        connection = self.connect(retry=True)
                        self.connection = connection
        return connection

    def upload_filedata(self, bucket_name, data, object_name):
        if self.connection is None:
            self.connect()
        s3 = self.connection
        if object_name is None:
            raise Exception('Object name must be informed')

        try:
            bucket = s3.Bucket(bucket_name)
            bucket.upload_fileobj(data, object_name)
            response = s3.ObjectSummary(bucket_name, object_name)
        except Exception as err:
            self.logger.error(err)
            self.exception = err
            response = None

        return response

    def upload_file(self, file_name, bucket_name, object_name=None):
        if self.connection is None:
            self.connect()
        s3 = self.connection
        if file_name is None:
            raise Exception('File must be informed')
        if not os.path.isfile(file_name):
            raise Exception('File not found')

        if object_name is None:
            object_name = os.path.basename(file_name)

        try:
            bucket = s3.Bucket(bucket_name)
            bucket.upload_file(file_name, object_name)
            response = s3.ObjectSummary(bucket_name, object_name)
        except Exception as err:
            self.logger.error(err)
            self.exception = err
            response = None

        return response

    def download_file(self, bucket_name, object_name, file_name):
        if file_name is None:
            raise Exception('File must be informed')

        if object_name is None:
            object_name = os.path.basename(file_name)

        try:
            bucket = self.get_bucket(bucket_name)
            # Get the file
            bucket.download_file(object_name, file_name)
            # test if file was created
            response = os.path.isfile(file_name)

        except Exception as err:
            self.logger.error(err)
            self.exception = err
            response = None

            response = None

        return response

    def create_bucket(self, bucket_name):
        if self.connection is None:
            self.connect()
        s3 = self.connection
        if bucket_name is None:
            raise Exception('Bucket must be informed')

        try:
            # Get the file
            response = s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': self.config.REGION_NAME
                },
            )

        except Exception as err:
            self.logger.error(err)
            self.exception = err
            response = None

        return response

    def delete_bucket(self, bucket_name, account_id=None):
        if account_id is None:
            # todo tratar
            account_id = "000000000000"
        if bucket_name is None:
            raise Exception('Bucket must be informed')

        try:
            # try to get the bucket_name
            bucket = self.get_bucket(bucket_name)
            # Get the file
            response = bucket.delete(ExpectedBucketOwner=account_id)

        except Exception as err:
            self.logger.error(err)
            self.exception = err
            response = None

        return response

    def list_objects(self, bucket_name, max_keys=1000):
        if self.connection is None:
            self.connect()
        s3 = self.connection
        if bucket_name is None:
            raise Exception('Bucket must be informed')
        try:
            response = s3.meta.client.list_objects(
                Bucket=bucket_name,
                # Delimiter='string',
                # EncodingType='url',
                # Marker='string',
                MaxKeys=max_keys,
                # Prefix='string',
                # RequestPayer='requester',
                # ExpectedBucketOwner='string'
            )
        except Exception as err:
            self.logger.error(err)
            self.exception = err
            response = None

        return response

    def get_bucket(self, bucket_name):
        bucket = None
        if self.connection is None:
            self.connect()
        s3 = self.connection
        try:
            # try to get the bucket_name
            bucket = s3.Bucket(bucket_name)
        except Exception as err:
            self.logger.error(err)
            self.exception = err
        return bucket

