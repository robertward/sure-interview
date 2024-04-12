import boto3

def list_parent_objects_with_date_modified(bucket_name):
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
    response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/')

    # Check if there are any objects in the bucket
    if 'CommonPrefixes' in response:
        # Print the key and date modified for each parent object (CommonPrefixes)
        for obj in response['CommonPrefixes']:
            parent_object_key = obj['Prefix']
            # Because there is no LastModified key for prefixes we need to grab the objects in each prefix
            parent_object_response = s3.list_objects_v2(Bucket=bucket_name, Prefix=parent_object_key)
            # Compare LastModified dates on all the objects to find the max LastModified and use that for the prefix
            last_modified_dates = [content['LastModified'] for content in parent_object_response.get('Contents', [])]
            if last_modified_dates:
                parent_last_modified = max(last_modified_dates)
                print(f"Parent Object: {parent_object_key.rstrip('/')}, Last Modified: {parent_last_modified}")
            else:
                print(f"Parent Object: {parent_object_key.rstrip('/')}, Last Modified: N/A (No objects inside)")
    else:
        print("No parent objects found in the bucket.")

# The name of your S3 bucket
bucket_name = 'deployments'

# Call the function with the bucket name
list_parent_objects_with_date_modified(bucket_name)
