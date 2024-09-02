#!/bin/bash

set -euo pipefail

# Set the directory paths
SPIDER_DIR="./freya/spiders"
OUTPUT_DIR="./output"
MERGED_FILE="$OUTPUT_DIR/merged.csv"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Function to initialize the merged file
initialize_merged_file() {
    > "$MERGED_FILE"
    echo "Emptied or created merged.csv file."
    echo "job_title,job_location,job_department,job_url,first_seen,base_salary,job_type,job_level,job_apply_end_date,last_seen,is_active,company,company_url,job_board,job_board_url,job_age" > "$MERGED_FILE"
}

# Function to process each spider file
process_spider_file() {
    local spider_file=$1
    local filename=$(basename "$spider_file" .py)
    local output_file="$OUTPUT_DIR/${filename}.csv"

    echo "Processing $filename..."
    if scrapy crawl "$filename" -o "$output_file" -t csv; then
        if [[ -f "$output_file" ]]; then
            tail -n +2 "$output_file" >> "$MERGED_FILE"
            found_files=true
        fi
    else
        echo "Error processing $filename"
    fi
}

# Initialize the merged file
initialize_merged_file

# Array of spiders to skip (manually filled)
# Exclude goto because it's not a real spider
skip_spiders=("goto")

# Process spider files
found_files=false
for spider_file in "$SPIDER_DIR"/*.py; do
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
        process_spider_file "$spider_file"
    fi
done

if $found_files; then
    echo "Merged CSV file updated: $MERGED_FILE"
else
    echo "No output files found to merge."
fi