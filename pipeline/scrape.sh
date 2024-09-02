#!/bin/bash

set -euo pipefail

# Set the directory paths
spider_dir="./freya/spiders"
output_dir="./output"
merged_file="$output_dir/merged.csv"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Empty the merged.csv file or create a new empty file
> "$merged_file"
echo "Emptied or created merged.csv file."

# Initialize the merged file with the header
echo "job_title,job_location,job_department,job_url,first_seen,base_salary,job_type,job_level,job_apply_end_date,last_seen,is_active,company,company_url,job_board,job_board_url,job_age" > "$merged_file"

# Array of spiders to skip (manually filled)
# Exclude goto because it's not a real spider   
skip_spiders=("goto" "jobstreet" "dealls" "kalibrr")

# Process spider files
found_files=false
for spider_file in "$spider_dir"/*.py; do
    filename=$(basename "$spider_file" .py)

    # Skip __init__.py file
    if [[ "$filename" == "__init__" ]]; then
        continue
    fi

    # Check if the spider should be skipped
    if [[ " ${skip_spiders[@]} " =~ " ${filename} " ]]; then
        echo "Skipping $filename..."
        continue
    fi

    if [[ -f "$spider_file" ]]; then
        output_file="$output_dir/${filename}.csv"

        echo "Processing $filename..."
        scrapy crawl "$filename" -o "$output_file" -t csv

        if [[ -f "$output_file" ]]; then
            tail -n +2 "$output_file" >> "$merged_file"
            found_files=true
        fi
    fi
done

if $found_files; then
    echo "Merged CSV file updated: $merged_file"
else
    echo "No output files found to merge."
fi