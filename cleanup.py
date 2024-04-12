import argparse
import boto3

def initialize_s3_client():
    ### Use this for localstack
    ## Specify LocalStack endpoint URL
    #localstack_endpoint_url = 'http://localhost:4566'
    ## Create an S3 client with LocalStack configuration
    #s3 = boto3.client('s3', endpoint_url=localstack_endpoint_url, aws_access_key_id='dummy', aws_secret_access_key='dummy')
    
    ## Use this for AWS
    #Create an S3 client
    s3 = boto3.client('s3')

    return s3

def list_parent_objects_with_date_modified(bucket_name):
    s3 = initialize_s3_client()

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
        print("No deployments found in the bucket.")
    
    return parent_objects_with_last_modified

def sort_parent_objects(parent_objects):

    # Sort the list of parent objects by last modified date.  Set reverse to False for oldest first
    parent_objects.sort(key=lambda x: x[1], reverse=True)

    return parent_objects


def print_parent_objects(sorted_parent_objects, num_deployments):

    # Check if the number of parent objects is greater than the specified number of prefixes
    if len(sorted_parent_objects) > num_deployments:
        # Print only the parent objects starting from the index specified by num_deployments
        for parent_object_key, last_modified in sorted_parent_objects[num_deployments:]:
            print(f"Parent Object: {parent_object_key.rstrip('/')}, Last Modified: {last_modified} will be DELETED")
    else:
        print("The number of deployments in the bucket is less than or equal to the specified number to keep.")


def delete_objects_under_prefix(bucket_name, prefix):
    s3 = initialize_s3_client()

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' in response:
        for obj in response['Contents']:
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
    else:
        print(f"No objects found under prefix: {prefix}")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="List the parent objects in an S3 bucket with their last modified dates.")
    parser.add_argument("bucket_name", help="Name of the S3 bucket")
    parser.add_argument("-n", "--num_deployments", type=int, default=5, help="Number of deployments to keep (default: 5)")
    parser.add_argument("-d", "--dry-run", action='store_true', help="Dry run - Nothing will be deleted")
    args = parser.parse_args()

    # Call the function with the provided arguments
    parent_objects = list_parent_objects_with_date_modified(args.bucket_name)
    sorted_parent_objects = sort_parent_objects(parent_objects)
    print_parent_objects(sorted_parent_objects, num_deployments=args.num_deployments)

    # Check if dry-run flag is set
    if not args.dry_run:
        # Delete objects under each parent object
        for parent_object_key, _ in sorted_parent_objects[args.num_deployments:]:
            delete_objects_under_prefix(args.bucket_name, parent_object_key)
    else:
        print("---- DRY RUN ----")