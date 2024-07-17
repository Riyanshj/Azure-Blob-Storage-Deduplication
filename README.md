# Azure Blob Storage Deduplication Script

This script helps deduplicate blobs in an Azure Blob Storage container by comparing their SHA-256 hashes.

## Features

- Computes SHA-256 hash of blobs to identify duplicates.
- Prompts user to delete duplicate blobs found.
- Prints "No duplication found" if no duplicates are detected.

## Requirements

- Python 3.6+
- `azure-storage-blob` library (install via `pip install azure-storage-blob`)

## Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
