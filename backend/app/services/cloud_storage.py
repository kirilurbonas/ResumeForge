"""Cloud storage adapter for file storage."""

from abc import ABC, abstractmethod
from typing import Optional, BinaryIO
import os
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)


class CloudStorageAdapter(ABC):
    """Abstract base class for cloud storage adapters."""
    
    @abstractmethod
    def upload_file(self, file_content: bytes, file_path: str) -> str:
        """Upload a file and return its URL."""
        pass
    
    @abstractmethod
    def download_file(self, file_path: str) -> bytes:
        """Download a file."""
        pass
    
    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        """Delete a file."""
        pass
    
    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists."""
        pass


class S3StorageAdapter(CloudStorageAdapter):
    """AWS S3 storage adapter."""
    
    def __init__(self, bucket_name: str, region: str = "us-east-1"):
        """
        Initialize S3 storage adapter.
        
        Args:
            bucket_name: S3 bucket name
            region: AWS region
        """
        self.bucket_name = bucket_name
        self.region = region
        
        # Initialize S3 client
        self.s3_client = boto3.client(
            's3',
            region_name=region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
    
    def upload_file(self, file_content: bytes, file_path: str) -> str:
        """Upload file to S3."""
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_path,
                Body=file_content
            )
            # Return S3 URL
            return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{file_path}"
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {e}")
            raise
    
    def download_file(self, file_path: str) -> bytes:
        """Download file from S3."""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return response['Body'].read()
        except ClientError as e:
            logger.error(f"Error downloading file from S3: {e}")
            raise
    
    def delete_file(self, file_path: str) -> bool:
        """Delete file from S3."""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return True
        except ClientError as e:
            logger.error(f"Error deleting file from S3: {e}")
            return False
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists in S3."""
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return True
        except ClientError:
            return False


class LocalStorageAdapter(CloudStorageAdapter):
    """Local file system storage adapter (for development)."""
    
    def __init__(self, base_path: str = "./storage"):
        """
        Initialize local storage adapter.
        
        Args:
            base_path: Base directory for file storage
        """
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
    
    def upload_file(self, file_content: bytes, file_path: str) -> str:
        """Save file locally."""
        full_path = os.path.join(self.base_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'wb') as f:
            f.write(file_content)
        
        return f"file://{full_path}"
    
    def download_file(self, file_path: str) -> bytes:
        """Read file from local storage."""
        full_path = os.path.join(self.base_path, file_path)
        with open(full_path, 'rb') as f:
            return f.read()
    
    def delete_file(self, file_path: str) -> bool:
        """Delete file from local storage."""
        try:
            full_path = os.path.join(self.base_path, file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists locally."""
        full_path = os.path.join(self.base_path, file_path)
        return os.path.exists(full_path)


# Factory function to get storage adapter
def get_storage_adapter() -> CloudStorageAdapter:
    """Get the appropriate storage adapter based on environment."""
    storage_type = os.getenv("STORAGE_TYPE", "local").lower()
    
    if storage_type == "s3":
        bucket_name = os.getenv("S3_BUCKET_NAME")
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable is required for S3 storage")
        region = os.getenv("AWS_REGION", "us-east-1")
        return S3StorageAdapter(bucket_name=bucket_name, region=region)
    else:
        base_path = os.getenv("STORAGE_PATH", "./storage")
        return LocalStorageAdapter(base_path=base_path)
