from __future__ import annotations

from typing import Optional

import milkstraw_client
from milkstraw_client import APIClient


class Model:
    """Handles interactions with generative models backend APIs.

    This class provides methods to create, retrieve, and list models.

    Attributes:
        id (str): The unique identifier of the model.
        name (str): The name of the model.
        status (str): The status of the model.
        source_data (str): The ID of the source data used to train the model.
    """

    def __init__(self, id: str, name: str, status: str, source_data: str):
        """Initializes a Model instance.

        Args:
            id (str): The unique identifier of the model.
            name (str): The name of the model.
            status (str): The status of the model.
            source_data (str): The ID of the source data used to train the model.
        """
        self.id = id
        self.name = name
        self.status = status
        self.source_data = source_data

    def __repr__(self) -> str:
        """Return a string representation of the Model object."""
        attributes = ", ".join(f"{key}='{value}'" for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attributes})"

    @staticmethod
    def create(
        name: str,
        source_data: str,
        auto_anonymize_personal_info: Optional[bool] = None,
        anonymize_personal_info_columns: Optional[list[str]] = None,
    ) -> Model:
        """Create a new generative model.

        Args:
            name (str): The name of the model.
            source_data (str): The ID of the source data used to train the model.
            auto_anonymize_personal_info (bool, optional): Whether to automatically anonymize
                personal information in the source data. Defaults to None.
            anonymize_personal_info_columns (list of str, optional): A list of column names
                to be anonymized in the source data. Defaults to None.

        Returns:
            Model: An instance of the Model class representing the created model.
        """
        url = f"{milkstraw_client.edge_service_url}/models/"
        json = {"name": name, "sourceDataId": source_data}
        if auto_anonymize_personal_info is not None:
            json["auto_anonymize_personal_info"] = auto_anonymize_personal_info
        if anonymize_personal_info_columns is not None:
            json["anonymize_personal_info_columns"] = anonymize_personal_info_columns
        response = APIClient.request("post", url, json=json)
        return Model.__parse_dict(response)

    @staticmethod
    def get(id: str) -> Model:
        """Retrieve a generative model by its unique identifier.

        Args:
            id (str): The unique identifier of the model.

        Returns:
            Model: An instance of the Model class representing the retrieved model.
        """
        url = f"{milkstraw_client.edge_service_url}/models/{id}"
        response = APIClient.request("get", url)
        return Model.__parse_dict(response)

    @staticmethod
    def list() -> list[Model]:
        """List all available generative models.

        Returns:
            list[Model]: A list of Model instances representing the available models.
        """
        url = f"{milkstraw_client.edge_service_url}/models"
        response = APIClient.request("get", url)
        models = [Model.__parse_dict(model_dict) for model_dict in response]
        return models

    @staticmethod
    def __parse_dict(model_dict: dict[str, str]) -> Model:
        """Parse a dictionary to create a Model instance.

        Args:
            model_dict (dict[str, str]): A dictionary representing the model.

        Returns:
            Model: An instance of the Model class based on the dictionary.
        """
        return Model(
            id=model_dict["id"],
            name=model_dict["name"],
            status=model_dict["status"],
            source_data=model_dict["sourceData"],
        )
