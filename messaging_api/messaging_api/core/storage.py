import boto3
from botocore.exceptions import ClientError, SSLError
from messaging_api.config import BUCKET_NAME, BUCKET_ENDPOINT_URL
from messaging_api.exceptions import StorageException
import time

class S3Storage:
    def __init__(self, bucket_name:str, endpoint_url:str = None, load_retries:int = 5 ) -> None:
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.load_retries = load_retries
        
    def _connect_bucket(self):
        client = boto3.resource("s3", endpoint_url=self.endpoint_url)
        
        bucket = client.Bucket(self.bucket_name)
        if not bucket.creation_date:
            client.create_bucket(ACL="private", Bucket=self.bucket_name)
            bucket = client.Bucket(self.bucket_name)
        return client, bucket
    
    def store(self, path:str, data:bytes):
        _, bucket = self._connect_bucket()
        try:
            object = bucket.put_object(Key=path, Body=data)
            object.wait_until_exists()
        except ClientError as e:
            raise StorageException(
                path, e.response["Error"]["Code"], e.response["Error"]["Message"]
            )
    
    def load(self, path: str) -> bytes:
        _, bucket = self._connect_bucket()
        try_again = True
        try_count = 0

        while try_again:
            try_again = False
            try:
                object_ref = bucket.Object(path)
                obj = object_ref.get()
                buffer = obj["Body"].read()
            except ClientError as e:
                raise StorageException(
                    path, e.response["Error"]["Code"], e.response["Error"]["Message"]
                )
            except SSLError as e:
                if try_count < self.load_retries:
                    try_again = True
                    time.sleep(0.05)
                else:
                    raise StorageException(
                        path,
                        e.response["Error"]["Code"],
                        e.response["Error"]["Message"],
                    )

            try_count += 1

        return buffer
    
    
if __name__=="__main__":
    storage_manager = S3Storage(BUCKET_NAME, BUCKET_ENDPOINT_URL)
    ...