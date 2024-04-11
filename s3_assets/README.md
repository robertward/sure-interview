# Terraform Script for Mock Deployment and S3 Bucket Creation

This Terraform script (`main.tf`) automates the creation of an S3 bucket and sets up a local bash script (`create_mock_files.sh`) to generate mock deployments, which are then uploaded to the S3 bucket. 

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) installed on your local machine.
- [LocalStack](https://github.com/localstack/localstack) installed on your local machine.

## Usage

1. **Initialize Terraform**: Run `terraform init` to initialize the working directory containing Terraform configuration files.
   ```bash
   terraform init
   ```

2. **Plan Infrastructure Changes**: Run `terraform plan` to create an execution plan. This step is optional but recommended to review changes before applying them.
   ```bash
   terraform plan
   ```

3. **Apply Changes**: Apply the Terraform configuration to create the S3 bucket and execute the local script.
   ```bash
   terraform apply
   ```

4. **Verify S3 Bucket Creation**: Once the script execution is complete, verify that the S3 bucket has been created with the specified configurations.

5. **Cleanup (Optional)**: If needed, you can destroy the infrastructure created by Terraform after testing.
   ```bash
   terraform destroy
   ```