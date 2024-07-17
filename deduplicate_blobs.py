import os
import hashlib
from azure.storage.blob import BlobServiceClient, ContainerClient
from io import BytesIO

def get_file_hash(file_path, chunk_size=8192):
    """Compute SHA-256 hash of the given file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_blob_hash(blob_client, chunk_size=8192):
    """Compute SHA-256 hash of the given blob data."""
    sha256 = hashlib.sha256()
    blob_data = BytesIO()
    blob_client.download_blob().readinto(blob_data)
    blob_data.seek(0)  # Reset stream position
    
    for chunk in iter(lambda: blob_data.read(chunk_size), b''):
        sha256.update(chunk)
    return sha256.hexdigest()

def prompt_delete_blob(blob_name):
    """Prompt the user to delete the duplicate blob."""
    prompt = f"Duplicate found: {blob_name}. Do you want to delete it? [y/N]: "
    response = input(prompt).strip().lower()
    return response == 'y'

def deduplicate_blobs(container_client):
    """Deduplicate blobs in the given container."""
    seen_hashes = {}
    blob_list = container_client.list_blobs()
    found_duplicate = False
    
    for blob in blob_list:
        blob_client = container_client.get_blob_client(blob.name)
        blob_hash = get_blob_hash(blob_client)
        
        if blob_hash not in seen_hashes:
            seen_hashes[blob_hash] = blob.name
        else:
            if prompt_delete_blob(blob.name):
                blob_client.delete_blob()
                print(f"Deleted: {blob.name}")
                found_duplicate = True
            else:
                print(f"Kept: {blob.name}")
    
    if not found_duplicate:
        print("No duplication found")


connection_string = "DefaultEndpointsProtocol=https;AccountName= #YourAccountName ;AccountKey=#YourAccountKey ;EndpointSuffix=core.windows.net"
container_name = "#YourContainerName"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

deduplicate_blobs(container_client)


"""Replace #YourAccountName with your storage account name"""
"""Replace #YourAccountKey with your acoount key"""
"""Replace #YourContainerName with your Azure blob Container"""
