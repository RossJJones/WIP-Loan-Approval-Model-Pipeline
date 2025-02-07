import os
import time
from loguru import logger
from minio import Minio

minio_client = Minio(
    endpoint=os.getenv("METAFLOW_S3_ENDPOINT_URL").replace("http://", ""),
    access_key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    secure=False
)

current_version = ""

if __name__ == "__main__":
    while True:
        try:
            result = minio_client.stat_object(
                bucket_name=os.getenv("INPUT_BUCKET"),
                object_name=os.getenv("INPUT_FILE"),
            )

            if result.version_id != current_version:
                current_version = result.version_id
                logger.info("New data version detected, starting feature engineering pipeline...")
                os.system(f"DATA_VERSION={current_version} python /app/feat_eng_pipeline.py run")
                logger.info("Feature engineering pipeline finished")
                

        except Exception as e:
            logger.error(e)

        time.sleep(60)


