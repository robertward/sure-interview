provider "aws" {
  region                  = "us-east-1"
  access_key              = "mock_access_key"
  secret_key              = "mock_secret_key"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  s3_force_path_style         = true
  endpoints {
    s3 = "http://localhost:4566"
  }
}

resource "aws_s3_bucket" "deployments_bucket" {
  bucket = "deployments"
  force_destroy = true
}

resource "null_resource" "upload_files" {
  depends_on = [aws_s3_bucket.deployments_bucket]

  provisioner "local-exec" {
    command = <<-EOT
      # Run the shell script
      ./create_mock_files.sh &&
      
      for file in $(ls ${path.module}/mocks); do
        awslocal s3 cp "${path.module}/mocks/$file" s3://deployments/$file --recursive
        sleep 10  # Adjust the sleep duration as needed
      done &&
      
      # Run the script after copying files
      rm -rf mocks
    EOT
  }
}