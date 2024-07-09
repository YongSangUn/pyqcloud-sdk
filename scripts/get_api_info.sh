#!/bin/bash

# Define global variables
SEARCH_DIR="/opt/git/0star/tencentcloud-sdk-python/tencentcloud"
api_version=$(grep -oP "(?<=version__ = ')[^']*(?=')" $SEARCH_DIR/__init__.py)
OUTPUT_FILE="api_info_$api_version.json"
declare -A API_MAP

# Function to extract and sanitize api information
extract_api_info() {
    local file=$1
    local api_version endpoint service
    api_version=$(grep -Po "(?<=_apiVersion = ')[^']*(?=')" "$file")
    endpoint=$(grep -Po "(?<=_endpoint = ')[^']*(?=')" "$file")
    service=$(grep -Po "(?<=_service = ')[^']*(?=')" "$file")

    if [[ -n $api_version && -n $endpoint && -n $service ]]; then
        if [[ -z ${API_MAP[$service]} ]]; then
            API_MAP["$service"]="{\"api_versions\": [\"$api_version\"], \"endpoint\": \"$endpoint\", \"service\": \"$service\"}"
        else
            API_MAP["$service"]=$(echo "${API_MAP[$service]}" | sed "s/\"apiVersion\": \[/\"apiVersion\": \[\"$api_version\",/")
        fi
    fi
}

# Function to process each client file
process_files() {
    local files
    files=$(grep -Pl '_apiVersion|_endpoint|_service' "$SEARCH_DIR"/*/v*/*_client.py)
    while IFS= read -r file; do
        extract_api_info "$file"
    done <<< "$files"
}

# Function to convert map to JSON
convert_to_json() {
    printf "{\n" > "$OUTPUT_FILE"
    for service in "${!API_MAP[@]}"; do
        printf "  \"%s\": %s,\n" "$service" "${API_MAP[$service]}" >> "$OUTPUT_FILE"
    done
    sed -i '$ s/,$//' "$OUTPUT_FILE"
    printf "}\n" >> "$OUTPUT_FILE"
}

# Main function to orchestrate script
main() {
    process_files
    convert_to_json
    printf "API information saved to %s\n" "$OUTPUT_FILE"
}

# Execute the main function
main
