import argparse
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

        # Create a list to store parent objects along with their last modified dates
        parent_objects_with_last_modified = []


        # Print the key and date modified for each parent object (CommonPrefixes)
        for obj in response['CommonPrefixes']:
            parent_object_key = obj['Prefix']
            # Because there is no LastModified key for prefixes we need to grab the objects in each prefix
            parent_object_response = s3.list_objects_v2(Bucket=bucket_name, Prefix=parent_object_key)
            # Compare LastModified dates on all the objects to find the max LastModified and use that for the prefix
            last_modified_dates = [content['LastModified'] for content in parent_object_response.get('Contents', [])]
            if last_modified_dates:
                parent_last_modified = max(last_modified_dates)
                # Store parent object key and its last modified date in the list
                parent_objects_with_last_modified.append((parent_object_key, parent_last_modified))
            else:
                # If there are no objects inside the prefix, store "N/A" for the last modified date
                parent_objects_with_last_modified.append((parent_object_key, "N/A (No objects inside)"))
    else:
        print("No parent objects found in the bucket.")
    
    return parent_objects_with_last_modified

def sort_parent_objects(parent_objects):

    # Sort the list of parent objects by last modified date.  Set reverse to True for newest first
    parent_objects.sort(key=lambda x: x[1], reverse=False)

    return parent_objects


def print_parent_objects(sorted_parent_objects, num_prefixes):

    # Check if the number of parent objects is greater than the specified number of prefixes
    if len(sorted_parent_objects) > num_prefixes:
        # Print only the parent objects starting from the index specified by num_prefixes
        for parent_object_key, last_modified in sorted_parent_objects[num_prefixes:]:
            print(f"Parent Object: {parent_object_key.rstrip('/')}, Last Modified: {last_modified}")
    else:
        print("The number of parent objects is less than or equal to the specified number of prefixes.")


# The name of your S3 bucket
bucket_name = 'deployments'

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="List the parent objects in an S3 bucket with their last modified dates.")
    parser.add_argument("bucket_name", help="Name of the S3 bucket")
    parser.add_argument("-n", "--num_prefixes", type=int, default=5, help="Number of prefixes to display (default: 5)")
    args = parser.parse_args()

    # Call the function with the provided arguments
    parent_objects = list_parent_objects_with_date_modified(args.bucket_name)
    sorted_parent_objects = sort_parent_objects(parent_objects)
    print_parent_objects(sorted_parent_objects, num_prefixes=args.num_prefixes)