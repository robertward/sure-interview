import boto3

def list_objects_in_bucket(bucket_name):
    ## Remove when not using localstack
    # Specify LocalStack endpoint URL
    localstack_endpoint_url = 'http://localhost:4566'

    # Create an S3 client with LocalStack configuration
    s3_client = boto3.client('s3', endpoint_url=localstack_endpoint_url,
                             aws_access_key_id='dummy', aws_secret_access_key='dummy')
    ##

    ## Use this for AWS
    # Create an S3 client
    # s3_client = boto3.client('s3')

    # List objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    # Check if objects were found
    if 'Contents' in response:
        print("Objects in bucket '{}':".format(bucket_name))
        for obj in response['Contents']:
            print("- {}".format(obj['Key']))
    else:
        print("No objects found in bucket '{}'.".format(bucket_name))

# Replace 'your-bucket-name' with 'deployments'
bucket_name = 'deployments'
list_objects_in_bucket(bucket_name)
