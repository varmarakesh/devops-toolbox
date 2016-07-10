__author__ = 'rakesh.varma'
import boto.s3
from boto.s3.connection import S3Connection
import time

class s3_operations:

    s3 = None

    def __init__(self, access_key_id, secret_access_key):
        self.s3 = boto.connect_s3(
                        aws_access_key_id = access_key_id,
                        aws_secret_access_key = secret_access_key
        )

    def __str__(self):
        result = ""
        if self.s3:
            result = '\n'.join(bucket.name for bucket in self.s3.get_all_buckets())
            return result

