# sure-interview
# Infrastructure Scripting Challenge

This Python script provides functionality to manage deployments in an Amazon S3 bucket. It allows you to list deployments with their last modified dates, sort them based on modification dates, and optionally delete objects based on specified criteria.

## Features

- **List deployments**: Retrieve a list of deployments (common prefixes) in an S3 bucket along with their last modified dates.
- **Sort by Last Modified Date**: Sort the list of deployments based on their last modified dates.
- **Delete Objects**: Optionally delete objects under specific deployments based on a specified number of deployments to keep.
- **Dry Run Mode**: Perform a dry run to preview deletions without actually deleting any objects.

## Usage

### Prerequisites

- Python 3.x installed
- `pip` installed
- Install dependencies using pip:
    ```
    pip install -r requirements.txt
    ```

### Command Line Arguments

```
usage: cleanup.py [-h] [-n NUM_DEPLOYMENTS] [-d] bucket_name

List the deployments in an S3 bucket with their last modified dates.

positional arguments:
  bucket_name           Name of the S3 bucket

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_DEPLOYMENTS, --num_deployments NUM_DEPLOYMENTS
                        Number of deployments to keep (default: 5)
  -d, --dry-run         Dry run - Nothing will be deleted
```

## Assumptions

1. AWS credentials are stored in either environment variables or in a shared credentials file
2. This script assumes the bucket you are working against is in the same AWS account as the credentials and you have the required access
3. It's assumed that sorting by date is the best way to find the latest deployment
4. Deployment folders aren't reused


## Testing

I've included the s3_assets directory that I used to set up my test environment, the README.md has instructions on how to use it.