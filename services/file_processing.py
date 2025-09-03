import io
import logging
import os
import uuid
from typing import Any, Dict

import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# In-memory storage for demo purposes - use Redis/Database in production
file_storage: Dict[str, pd.DataFrame] = {}


class FileProcessingService:
    """Service for handling file uploads and processing"""

    ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json"}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

    @staticmethod
    def validate_file(filename: str, file_size: int) -> tuple[bool, str]:
        """Validate file extension and size"""
        if not filename:
            return False, "Filename is required"

        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in FileProcessingService.ALLOWED_EXTENSIONS:
            return (
                False,
                f"File type {file_ext} not supported. Allowed: {', '.join(FileProcessingService.ALLOWED_EXTENSIONS)}",
            )

        if file_size > FileProcessingService.MAX_FILE_SIZE:
            return (
                False,
                f"File size exceeds maximum allowed size of {FileProcessingService.MAX_FILE_SIZE // (1024 * 1024)}MB",
            )

        return True, "Valid file"

    @staticmethod
    async def process_file(
        file_content: bytes, filename: str
    ) -> tuple[str, pd.DataFrame, Dict[str, Any]]:
        """Process uploaded file and return DataFrame with metadata"""
        try:
            file_ext = os.path.splitext(filename)[1].lower()

            # Read file based on extension
            if file_ext == ".csv":
                df = pd.read_csv(io.BytesIO(file_content))
            elif file_ext in [".xlsx", ".xls"]:
                df = pd.read_excel(io.BytesIO(file_content))
            elif file_ext == ".json":
                df = pd.read_json(io.BytesIO(file_content))
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")

            # Generate unique file ID
            file_id = str(uuid.uuid4())

            # Store DataFrame
            file_storage[file_id] = df

            # Generate metadata
            metadata = FileProcessingService._generate_metadata(df, filename)

            logger.info(f"Successfully processed file {filename} with ID {file_id}")
            return file_id, df, metadata

        except Exception as e:
            logger.error(f"Error processing file {filename}: {str(e)}")
            raise ValueError(f"Error processing file: {str(e)}")

    @staticmethod
    def _generate_metadata(df: pd.DataFrame, filename: str) -> Dict[str, Any]:
        """Generate comprehensive metadata for the DataFrame"""
        try:
            # Basic info
            metadata = {
                "filename": filename,
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "data_types": df.dtypes.astype(str).to_dict(),
            }

            # Categorize columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
            datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

            metadata.update(
                {
                    "numeric_columns": numeric_cols,
                    "categorical_columns": categorical_cols,
                    "datetime_columns": datetime_cols,
                    "missing_values": df.isnull().sum().to_dict(),
                    "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB",
                }
            )

            # Statistical summary for numeric columns
            if numeric_cols:
                metadata["summary_stats"] = df[numeric_cols].describe().to_dict()

            # Sample data (first 5 rows)
            metadata["sample_data"] = df.head().to_dict("records")

            return metadata

        except Exception as e:
            logger.error(f"Error generating metadata: {str(e)}")
            return {"error": f"Error generating metadata: {str(e)}"}

