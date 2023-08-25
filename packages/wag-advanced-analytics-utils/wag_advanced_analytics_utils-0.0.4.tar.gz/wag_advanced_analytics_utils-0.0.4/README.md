# README

This package contains all the common functions used to run the Advanced Analytics algorithms. We provide a brief explanation of each of the modules and the corresponding functions:

- ``athena_data_provider`` contains the class ``AthenaDataProvider``, which is initialized by giving the parameters
    - aws_access_key_id
    - aws_secret_access_key
    - s3_staging_dir
    - region_name.

    The function ``read_query`` returns a DataFrame with the information requested by the query passed as argument.

- ``logger`` contains the class ``Logger``, which logs important messages and prints them to the terminal or CloudWatch in AWS.

- ``metrics`` contains the class ``Metrics``, which creates the metrics and pushes them to Datadog.

- ``s3_client`` contains the class ``S3Client``, that is initialized using boto3.client and boto3.resource and the environment variable ```RESULT_BUCKET```. 

    The function ``upload_files`` uploads the DataFrame returned by the algorithm (``output_df``) to the given path (``output_path``) in AWS, for the chosen variant (``variant`` – typically ``production`` or the name of the experiment, if testing new features).

-----------

If changes are made to this package, it has to be updated in PyPI by doing:

1. Update the version number in the file ```pyproject.toml``` under the field ```version```.
2. In the terminal, run the command ```python3 -m build```. This will create two new files in the directory ```dist```.
3. Upload the package by typing ```twine upload dist/*``` in the terminal. Since the account is protected by a two-factor authentication we have to use a token, meaning that you must
    - set your username to \_\_token\_\_ and
    - set your password to the token value, including the pypi- prefix.
4. Check that the package has been correcly updated in https://pypi.org/project/wag-advanced-analytics-utils/.

-----------

To use these modules in a Python script do the following:

- start by installing the package by running
    ```
    pip install wag_advanced_analytics_utils
    ``````
    or
    ```
    pipenv install wag_advanced_analytics_utils
    ```
- import the desired class by typing
    ```
    from wag_advanced_analytics_utils.{module_name} import class_name
    ```
    where ```{module_name}``` is one of the modules of the package and ```class_name``` is (one of) the class contained in the module.
