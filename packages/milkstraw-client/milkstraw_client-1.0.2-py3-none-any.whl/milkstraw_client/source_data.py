from __future__ import annotations

from typing import Optional

import milkstraw_client
from milkstraw_client import APIClient


class SourceData:
    """Handles interactions with the source data backend APIs.

    This class provides methods to upload, retrieve, list, and download source data.

    Attributes:
        id (str): The unique identifier of the source data.
        name (str): The name of the source data.
        status (str): The status of the source data.
    """

    def __init__(self, id: str, name: str, status: str):
        """Initializes a SourceData instance.

        Args:
            id (str): The unique identifier of the source data.
            name (str): The name of the source data.
            status (str): The status of the source data.
        """
        self.id = id
        self.name = name
        self.status = status

    def __repr__(self) -> str:
        """Return a string representation of the SourceData object."""
        attributes = ", ".join(f"{key}='{value}'" for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attributes})"

    @staticmethod
    def upload(
        name: str,
        file_path: str,
        auto_primary_key: Optional[bool] = None,
        primary_key_column: Optional[str] = None,
    ) -> SourceData:
        """Upload source data to the backend.

        Args:
            name (str): The name of the source data.
            file_path (str): The path to the source data file.
            auto_primary_key (bool, optional): Whether to automatically generate a primary key. Defaults to None.
            primary_key_column (str, optional): The name of the primary key column. Defaults to None.

        Returns:
            SourceData: An instance of the SourceData class representing the uploaded source data.
        """
        url = f"{milkstraw_client.edge_service_url}/source-data/"
        params = {"name": name}
        if auto_primary_key is not None:
            params["auto_primary_key"] = auto_primary_key
        if primary_key_column is not None:
            params["primary_key_column"] = primary_key_column
        file_paths = {"file": file_path}
        response = APIClient.request("post", url, params=params, file_paths=file_paths)
        return SourceData(**response)

    @staticmethod
    def get(id: str) -> SourceData:
        """Retrieve source data by its unique identifier.

        Args:
            id (str): The unique identifier of the source data.

        Returns:
            SourceData: An instance of the SourceData class representing the retrieved source data.
        """
        url = f"{milkstraw_client.edge_service_url}/source-data/{id}"
        response = APIClient.request("get", url)
        return SourceData(**response)

    @staticmethod
    def list() -> list[SourceData]:
        """List all available source data.

        Returns:
            list[SourceData]: A list of SourceData instances representing the available source data.
        """
        url = f"{milkstraw_client.edge_service_url}/source-data"
        response = APIClient.request("get", url)
        data = [SourceData(**data_dict) for data_dict in response]
        return data

    @staticmethod
    def download(id: str, file_path: str) -> str:
        """Download the content of source data by its unique identifier.

        Args:
            id (str): The unique identifier of the source data.
            file_path (str): The path to save the downloaded file.

        Returns:
            str: The path to the downloaded file.
        """
        url = f"{milkstraw_client.edge_service_url}/source-data/download/{id}"
        return APIClient.download_file(file_path, url)
