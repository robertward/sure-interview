import boto3

def list_objects(bucket_name):
    ## Remove when not using localstack
    # Specify LocalStack endpoint URL
    localstack_endpoint_url = 'http://localhost:4566'

    # Create an S3 client with LocalStack configuration
    s3 = boto3.client('s3', endpoint_url=localstack_endpoint_url,
                             aws_access_key_id='dummy', aws_secret_access_key='dummy')
    ##

    ## Use this for AWS
    # Create an S3 client
    # s3_client = boto3.client('s3')

    # List objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Check if there are any objects in the bucket
    if 'Contents' in response:
        # Print the key (object name) for each object in the bucket
        for obj in response['Contents']:
            print(obj['Key'])
    else:
        print("No objects found in the bucket.")

# The name of your S3 bucket
bucket_name = 'deployments'

# Call the function with the bucket name
list_objects(bucket_name)
