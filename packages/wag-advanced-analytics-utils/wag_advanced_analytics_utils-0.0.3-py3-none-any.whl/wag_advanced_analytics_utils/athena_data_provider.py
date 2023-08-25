import pandas as pd
from pyathena import connect as athena_connect
from wag_advanced_analytics_utils.logger import Logger

class AthenaDataProvider:
    """
    Athena Data Provider class for establishing connection to query data from AWS via Athena.

    Attributes
    ----------
    aws_access_key_id : str
        Key ID
    aws_secret_access_key : str
        family name of the person
    s3_staging_dir : str
        S3 staging directory
    region_name : str
        Region name for the AWS connection.

    Methods
    -------
    __init__(self, aws_access_key_id, aws_secret_access_key, s3_staging_dir, region_name):
    __repr__(self):
    __collect_aws_data(self, query):
    """

    def __init__(self, aws_access_key_id, aws_secret_access_key, s3_staging_dir, region_name):
        """
        Constructs all the necessary attributes for the AWS Data Provider object.
        """
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.s3_staging_dir = s3_staging_dir
        self.region_name = region_name

    def __repr__(self):
        """
        Gives information about the instances S3 staging directory and region name.

        Returns
        -------
        : str
            S3 staging directory and region name.
        """
        return f"s3_staging_dir: {self.s3_staging_dir}, region_name: {self.region_name}"
    
    def read_query(self, query):
        """
        Given a query, read it and return it as a DataFrame.
        """
        Logger.info("Loading data from AWS")
        try:
            data = self.__collect_aws_data(query)
        except Exception as error:
            Logger.error(
                "Failed to collect data from AWS", {"message": str(error)}
            )
            raise

        return data

    def __collect_aws_data(self, query):
        """
        Connect to AWS and execute query via Athena

        Parameters
        ----------
        query : str
            SQL query to run in Athena to fetch data

        Returns
        -------
        data : pandas.DataFrame
            Dataframe queried from Athena
        """

        athena_connection = athena_connect(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            s3_staging_dir=self.s3_staging_dir,
            region_name=self.region_name,
        )

        data = pd.read_sql_query(query, athena_connection)

        if data.empty:
            raise RuntimeError("No data was collected from AWS")

        return data
    
