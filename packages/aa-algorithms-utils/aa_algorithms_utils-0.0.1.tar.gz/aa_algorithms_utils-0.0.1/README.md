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

- ``s3_client`` contains the class ``S3Client``, that is initialized using boto3.client and boto3.resource and the environment variable RESULT_BUCKET. 

    The function ``upload_files`` uploads the DataFrame returned by the algorithm (``output_df``) to the given path (``output_path``) in AWS, for the chosen variant (``variant`` – typically ``production`` or the name of the experiment, if testing new features).

-----------

To use these modules in the experiments do the following: