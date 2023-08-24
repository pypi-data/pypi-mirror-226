from pathlib import PurePath

from botocore.exceptions import ClientError
from cloudstorageio.exceptions.exceptions import CredentialsExpiredError
from cloudstorageio.file.file import File


class S3File(File):
    def __init__(self, s3_object):
        self.object = s3_object

    def read(self):
        try:
            result = self.object.get()['Body'].read()
        except ClientError:
            raise CredentialsExpiredError
        return result

    def path(self):
        return (f's3://'
                f'{str(self.object.bucket_name / PurePath(self.object.key))}')

    def __repr__(self):
        return f'S3File at {self.object.key}'
