from __future__ import absolute_import

import uuid

from pydantic.fields import Dict, Any, List
from uplink import *

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from depot_service.models.depot_flag_request import DepotFlagRequest
from depot_service.models.depot_request import DepotRequest
from depot_service.models.depot_response import DepotResponse


class DepotApi(DataOSBaseConsumer):

    @raise_for_status_code
    @returns.json
    @json
    @patch("api/v2/depots/{depot}/archived")
    def archive(self, depot: str, payload: Body(type=DepotFlagRequest),
                correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> DepotResponse:
        """
        Archive a specific depot.

        This method makes an API call to archive the specified depot.

        Args:
            depot (str): The ID or name of the depot to archive.
            payload (dict):
                Attributes:
                    isArchived (bool): A flag indicating whether the depot should be archived (True) or unarchived (False).
                    archivalMessage (Optional[str]): An optional message explaining the reason for archiving the depot.
                                     This message will only be present if the `isArchived` attribute is True.
        Returns:
            DepotResponse: An object containing the response data from the API call.
                           The structure of the DepotResponse object may vary based on the API response.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/depots/{depot}")
    def get_depot(self, depot: str,
                  correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> DepotResponse:
        """
        Get information about a specific depot.

        This method makes an API call to retrieve detailed information about the specified depot.

        Args:
            depot (str): The ID or name of the depot to retrieve information for.

        Returns:
            DepotResponse: An object containing the response data from the API call.
        """
        pass

    @raise_for_status_code
    @returns.json
    @json
    @put("api/v2/depots/{depot}")
    def create_or_update(self, depot: str, payload: Body(type=DepotRequest),
                         correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> DepotResponse:
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/depots/{depot}/meta")
    def get_meta(self, depot: str,
                 correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Dict[str, Any]:
        """
        Get metadata for a specific depot.

        Args:
            depot (str): The ID or name of the depot to retrieve metadata for.

        Returns:
            dict: A dictionary containing the metadata for the specified depot.

        Raises:
            Exception: If the API request fails or returns an error status code.

        """
        pass

    @raise_for_status_code
    @delete("api/v2/depots/{depot}/meta")
    def delete_meta(self, depot: str, key: Query("key"),
                    correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Delete a meta entry for a given depot.

        This function deletes a meta entry with a specific key for a given depot.

        Parameters:
            depot (str): The name of the depot where the meta entry will be deleted.
            key (str): The key of the meta entry to be deleted.

        Returns:
            None: This function doesn't return anything explicitly.
        """
        pass

    @raise_for_status_code
    @json
    @patch("api/v2/depots/{depot}/meta")
    def update_meta(self, depot: str, payload: Body(type=dict),
                    correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> DepotResponse:
        """
        Update a meta entry for a given depot.

        This function sends a PATCH request to update a meta entry for a given depot
        using the provided payload.

        Parameters:
            depot (str): The name of the depot where the meta entry will be updated.
            payload (dict): A dictionary containing the data to be updated in the meta entry.

        Returns:
            DepotResponse: An object representing the response from the API call.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/depots/{depot}/owners")
    def get_owners(self, depot: str,
                   correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[str]:
        """
        Get the owners of a specific depot.

        This method makes an API call to retrieve the owners associated with the specified depot.

        Args:
            depot (str): The ID or name of the depot to retrieve owners for.

        Returns:
            List[str]: A list containing the names of owners of the specified depot.
        """
        pass

    @raise_for_status_code
    @returns.json
    @put("api/v2/depots/{depot}/owners/{owner}")
    def add_owner(self, depot: str, owner: str,
                  correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> DepotResponse:
        """
            Add a new owner to a given depot.

            This function sends a PUT request to add a new owner to a specified depot.

            Parameters:
                depot (str): The name of the depot to which the new owner will be added.
                owner (str): The name of the new owner to be added to the depot.

            Returns:
                DepotResponse: An object representing the response from the API call.
        """
        pass

    @raise_for_status_code
    @delete("api/v2/depots/{depot}/owners/{owner}")
    def delete_owner(self, depot: str, owner: str,
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Delete an owner from a given depot.

        This function sends a DELETE request to remove an owner from a specified depot.

        Parameters:
            depot (str): The name of the depot from which the owner will be deleted.
            owner (str): The name of the owner to be removed from the depot.

        Returns:
            None: This function doesn't return anything explicitly. The owner will be deleted from the depot on a successful API call.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/depots/{depot}/collections")
    def get_collections(self, depot: str,
                        correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[str]:
        """
        Retrieve a list of collections from a given depot.

        This function sends a GET request to fetch the list of collections available in a specified depot.

        Parameters:
            depot (str): The name of the depot from which to retrieve the list of collections.
                Possible values for 'depot': GCS, S3, ABFSS, WASBS, FILE, PULSAR

        Returns:
            List[str]: A list of strings representing the names of collections available in the specified depot.
                If no collections are found or an error occurs, an empty list will be returned.

        Raises:
            ValueError: If the 'depot' parameter is not one of the valid options (GCS, S3, ABFSS, WASBS, FILE, PULSAR).
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/depots")
    def get_depots(self,
                   correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> dict:
        """
        Retrieve a dictionary of available depots.

        This function sends a GET request to fetch a dictionary containing information about available depots.

        Parameters:
            No parameter

        Returns:
            dict: A dictionary where the keys represent the depot names and the values are additional information about each depot.
        """
        pass

    # @raise_for_status_code
    # @returns.json
    # @get("api/v2/depots/{depot}/secrets")
    # def get_secrets(self) -> dict:
    #     """
    #     Retrieve a dictionary of available depots.
    #
    #     This function sends a GET request to fetch a dictionary containing information about available depots.
    #
    #     Parameters:
    #         No parameter
    #
    #     Returns:
    #         dict: A dictionary where the keys represent the depot names and the values are additional information about each depot.
    #     """
    #     pass