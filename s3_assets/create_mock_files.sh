#!/bin/bash

# Define the number of mock directories to create
num_directories=5

# Loop to create multiple mock directories
for ((i=1; i<=$num_directories; i++))
do
    # Create main directory
    mkdir -p "mocks/deployment_$i"

    # Create subdirectories
    mkdir -p "mocks/deployment_$i/subdir1"
    mkdir -p "mocks/deployment_$i/subdir2"

    # Generate random filenames
    file1_name=$(uuidgen | tr -d '-')
    file2_name=$(uuidgen | tr -d '-')
    file3_name=$(uuidgen | tr -d '-')

    # Create files with random filenames
    touch "mocks/deployment_$i/$file1_name.txt"
    touch "mocks/deployment_$i/subdir1/$file2_name.txt"
    touch "mocks/deployment_$i/subdir2/$file3_name.txt"

    # Display the directory structure
    echo "Created mock directory $i:"
    tree "mocks/deployment_$i"
    echo ""
done
