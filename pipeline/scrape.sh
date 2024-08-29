#!/bin/bash

set -euo pipefail

# Load configuration
source ./config.sh

# Array of spiders to exclude
EXCLUDE_SPIDERS=("goto")

# Function for logging
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Function to run a spider
run_spider() {
    spider=$1
    output_file="$OUTPUT_DIR/${spider}.csv"
    log "Processing $spider..."
    if ! scrapy crawl "$spider" -o "$output_file" -t csv; then
        log "Error: Failed to process $spider"
        return 1
    fi
    return 0
}

# Main execution
main() {
    mkdir -p "$OUTPUT_DIR"
    > "$MERGED_FILE"
    log "Emptied or created merged.csv file."

    echo "$HEADER" > "$MERGED_FILE"

    found_files=false
    for spider_file in "$SPIDER_DIR"/*.py; do
        filename=$(basename "$spider_file" .py)
        [[ "$filename" == "__init__" ]] && continue

        # Check if the spider is in the exclusion list
        if [[ " ${EXCLUDE_SPIDERS[@]} " =~ " ${filename} " ]]; then
            log "Skipping excluded spider: $filename"
            continue
        fi

        if [[ -f "$spider_file" ]]; then
            if run_spider "$filename"; then
                tail -n +2 "$OUTPUT_DIR/${filename}.csv" >> "$MERGED_FILE"
                found_files=true
            fi
        fi
    done

    if $found_files; then
        log "Merged CSV file updated: $MERGED_FILE"
    else
        log "No output files found to merge."
    fi

    # Cleanup
    rm -f "$OUTPUT_DIR"/*.csv
}

main "$@"