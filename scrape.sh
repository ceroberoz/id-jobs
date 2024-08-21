#!/bin/bash

# Set the directory path
spider_dir="./freya/spiders"
output_dir="./output"

# Get current date in the format YYYY-MM-DD
current_date=$(date +"%Y-%m-%d")

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Initialize an array to store output file names
output_files=()

# Loop through all .py files in the spider directory
for spider_file in "$spider_dir"/*.py; do
    if [ -f "$spider_file" ]; then
        # Extract filename without extension
        filename=$(basename "$spider_file" .py)

        # Run scrapy command
        scrapy crawl "$filename" -o "$output_dir/${current_date}-${filename}.csv" -t csv

        # Add output file to the array
        output_files+=("$output_dir/${current_date}-${filename}.csv")
    fi
done

# Merge all output CSV files
output_merged="$output_dir/merged.csv"

# Check if there are any output files
if [ ${#output_files[@]} -gt 0 ]; then
    # Initialize the merged file with the header
    echo "job_title,job_location,job_department,job_url,first_seen,base_salary,job_type,job_level,job_apply_end_date,last_seen,is_active,company,company_url,job_board,job_board_url" > "$output_merged"

    # Append the content of all files (excluding headers) to the merged file
    for file in "${output_files[@]}"; do
        tail -n +2 "$file" >> "$output_merged"
    done

    echo "Merged CSV file created: $output_merged"
else
    echo "No output files found to merge."
fi
