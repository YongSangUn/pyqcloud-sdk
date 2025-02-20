#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import os
import re
from pathlib import Path
from typing import Dict, List

# Regular expressions for extracting API information
VERSION_PATTERN = r"(?<=version__ = ')[^']*(?=')"
API_VERSION_PATTERN = r"(?<=_apiVersion = ')[^']*(?=')"
ENDPOINT_PATTERN = r"(?<=_endpoint = ')[^']*(?=')"
SERVICE_PATTERN = r"(?<=_service = ')[^']*(?=')"


def extract_api_info(file_path: str) -> Dict[str, str]:
    """Extract API information from a client file.

    Args:
        file_path (str): Path to the client file.

    Returns:
        Dict[str, str]: Dictionary containing API information.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    api_version = re.search(API_VERSION_PATTERN, content)
    endpoint = re.search(ENDPOINT_PATTERN, content)
    service = re.search(SERVICE_PATTERN, content)

    if all([api_version, endpoint, service]):
        return {"api_version": api_version.group(), "endpoint": endpoint.group(), "service": service.group()}
    return {}


def find_client_files(sdk_path: str) -> List[str]:
    """Find all client files in the SDK directory.

    Args:
        sdk_path (str): Path to the SDK directory.

    Returns:
        List[str]: List of client file paths.
    """
    client_files = []
    for root, _, files in os.walk(sdk_path):
        for file in files:
            if file.endswith("_client.py"):
                client_files.append(os.path.join(root, file))
    return client_files


def get_sdk_version(sdk_path: str) -> str:
    """Get the SDK version from __init__.py.

    Args:
        sdk_path (str): Path to the SDK directory.

    Returns:
        str: SDK version.
    """
    init_file = os.path.join(sdk_path, "__init__.py")
    with open(init_file, "r", encoding="utf-8") as f:
        content = f.read()
    version_match = re.search(VERSION_PATTERN, content)
    return version_match.group() if version_match else "unknown"


def process_api_info(client_files: List[str]) -> Dict[str, Dict]:
    """Process API information from client files.

    Args:
        client_files (List[str]): List of client file paths.

    Returns:
        Dict[str, Dict]: Dictionary containing processed API information.
    """
    api_map = {}
    for file in client_files:
        info = extract_api_info(file)
        if not info:
            continue

        service = info["service"]
        if service not in api_map:
            api_map[service] = {
                "api_versions": [info["api_version"]],
                "endpoint": info["endpoint"],
                "service": service,
            }
        elif info["api_version"] not in api_map[service]["api_versions"]:
            api_map[service]["api_versions"].append(info["api_version"])

    return api_map


def save_api_info(api_map: Dict[str, Dict], output_dir: str, version: str):
    """Save API information to a JSON file.

    Args:
        api_map (Dict[str, Dict]): API information to save.
        output_dir (str): Directory to save the JSON file.
        version (str): SDK version.
    """
    _ = version
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "endpoints.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(api_map, f, indent=2, ensure_ascii=False)


def save_sdk_version(output_dir: str, version: str):
    """Save SDK version to .sdk-version file.

    Args:
        output_dir (str): Directory to save the version file.
        version (str): SDK version.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    version_file = output_dir / ".sdk-version"

    with open(version_file, "w", encoding="utf-8") as f:
        f.write(version)


def main():
    """Main function to orchestrate the API information extraction process."""
    parser = argparse.ArgumentParser(description="Extract API information from Tencent Cloud SDK")
    parser.add_argument("sdk_path", help="Path to the SDK directory")
    parser.add_argument("output_dir", help="Directory to save the output JSON file")
    args = parser.parse_args()

    # Get SDK version
    version = get_sdk_version(args.sdk_path)

    # Find and process client files
    client_files = find_client_files(args.sdk_path)
    api_map = process_api_info(client_files)

    # Save API information and SDK version
    save_api_info(api_map, args.output_dir, version)
    save_sdk_version(args.output_dir, version)
    print(f"API information saved to {args.output_dir}/endpoints_{version}.json")
    print(f"SDK version saved to {args.output_dir}/.sdk-version")


if __name__ == "__main__":
    main()
