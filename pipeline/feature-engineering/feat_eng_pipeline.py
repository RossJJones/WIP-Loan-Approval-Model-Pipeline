from metaflow import FlowSpec, step
from loguru import logger
import os
import polars as pl
from minio import Minio
from io import BytesIO

DATA_VERSION = os.getenv("DATA_VERSION")
FEATURE_STORE = os.getenv("FEATURE_STORE")
INPUT_BUCKET = os.getenv("INPUT_BUCKET")
INPUT_FILE = os.getenv("INPUT_FILE")
OUTPUT_FILE = os.getenv("OUTPUT_FILE")

minio_client = Minio(
    endpoint=os.getenv("METAFLOW_S3_ENDPOINT_URL").replace("http://", ""),
    access_key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    secure=False
)


class TestFlow(FlowSpec):

    @step
    def start(self):
        response = minio_client.get_object(
            bucket_name=INPUT_BUCKET,
            object_name=INPUT_FILE,
            version_id=DATA_VERSION
        )
        data = BytesIO(response.read())
        self.loan_dataframe = pl.read_csv(data)
        self.next(self.find_best_features)
    
    @step
    def find_best_features(self):
        
    
    @step
    def end(self):
        print(self.loan_dataframe.describe())
    

if __name__ == '__main__':
    TestFlow()