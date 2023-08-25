import boto3
import os
from wag_advanced_analytics_utils.logger import Logger

class S3Client:

    def __init__(self):
        """
        Constructs the necessary attributes for the S3 Client object.
        """
        self.s3 = boto3.client('s3')
        self.r3 = boto3.resource('s3')
        self.bucket = os.environ['RESULT_BUCKET']

    @classmethod
    def upload_files(self, output_path, output_df, variant):
        """
        Uploads the algorithm result (output_df) to the given path (output_path).
        """
        Bucket = self.r3.Bucket(self.bucket)
        try:
            csv_content = output_df.to_csv(index=True, header=True)

            Bucket.put_object(
                    Key=output_path,
                    ACL="public-read",
                    Body=csv_content,
                    ContentType="text/csv",
                )

            Logger.info("Result uploaded successfully!", {"variant": variant})
        except Exception as error:
            raise error
            
        return