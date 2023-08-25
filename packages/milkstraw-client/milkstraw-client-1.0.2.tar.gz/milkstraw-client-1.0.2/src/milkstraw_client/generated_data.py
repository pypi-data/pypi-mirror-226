from __future__ import annotations

from typing import Optional

import milkstraw_client
from milkstraw_client import APIClient


class GeneratedData:
    """Handles interactions with generated data backend APIs.

    This class provides methods to generate, retrieve, and list generated data,
    as well as download generated data and associated reports.

    Attributes:
        id (str): The unique identifier of the generated data.
        model (str): The ID of the model used to generate the data.
        status (str): The status of the generated data.
    """

    def __init__(self, id: str, model: str, status: str):
        """Initializes a GeneratedData instance.

        Args:
            id (str): The unique identifier of the generated data.
            model (str): The ID of the model used to generate the data.
            status (str): The status of the generated data.
        """
        self.id = id
        self.model = model
        self.status = status

    def __repr__(self) -> str:
        """Return a string representation of the GeneratedData object."""
        attributes = ", ".join(f"{key}='{value}'" for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attributes})"

    @staticmethod
    def generate(model: str, records_num: int, condition: Optional[dict] = None) -> GeneratedData:
        """Generate synthetic data using a trained model.

        Args:
            model (str): The ID of the model used for data generation.
            records_num (int): The number of records to generate.
            condition (dict, optional): A dictionary specifying the generation condition. Defaults to None.

        Returns:
            GeneratedData: An instance of the GeneratedData class representing the generated data.
        """
        url = f"{milkstraw_client.edge_service_url}/generated-data/"
        json = {"modelId": model, "recordsNum": records_num}
        if condition is not None:
            json["condition"] = condition
        response = APIClient.request("post", url, json=json)
        return GeneratedData(**response)

    @staticmethod
    def get(id: str) -> GeneratedData:
        """Retrieve generated data by its unique identifier.

        Args:
            id (str): The unique identifier of the generated data.

        Returns:
            GeneratedData: An instance of the GeneratedData class representing the retrieved generated data.
        """
        url = f"{milkstraw_client.edge_service_url}/generated-data/{id}"
        response = APIClient.request("get", url)
        return GeneratedData(**response)

    @staticmethod
    def list() -> list[GeneratedData]:
        """List all available generated data.

        Returns:
            list[GeneratedData]: A list of GeneratedData instances representing the available generated data.
        """
        url = f"{milkstraw_client.edge_service_url}/generated-data"
        response = APIClient.request("get", url)
        data = [GeneratedData(**data_dict) for data_dict in response]
        return data

    @staticmethod
    def download(id: str, file_path: str) -> str:
        """Download the content of generated data by its unique identifier.

        Args:
            id (str): The unique identifier of the generated data.
            file_path (str): The path to save the downloaded file.

        Returns:
            str: The path to the downloaded file.
        """
        url = f"{milkstraw_client.edge_service_url}/generated-data/download/{id}"
        return APIClient.download_file(file_path, url)

    @staticmethod
    def download_report(id: str, file_path: str) -> str:
        """Download the report associated with generated data.

        Args:
            id (str): The unique identifier of the generated data.
            file_path (str): The path to save the downloaded report file.

        Returns:
            str: The path to the downloaded report file.
        """
        url = f"{milkstraw_client.edge_service_url}/generated-data/download/report/{id}"
        return APIClient.download_file(file_path, url)
