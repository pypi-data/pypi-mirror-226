from __future__ import absolute_import

import uuid
from pydantic.fields import Dict, List

from uplink import *

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from depot_service.models.metadata_version_response import MetadataVersionResponse
from depot_service.models.dataset_response import DatasetResponse
from depot_service.models.dataset_request import DatasetRequest
from depot_service.models.field_rename_request import FieldRenameRequest
from depot_service.models.field_request import FieldRequest
from depot_service.models.field_update_request import FieldUpdateRequest
from depot_service.models.iceberg_partition_spec_request import IcebergPartitionSpecRequest
from depot_service.models.iceberg_stats import IcebergStats
from depot_service.models.snapshot_response import SnapshotResponse


class DatasetApi(DataOSBaseConsumer):
    @json
    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @patch("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/fields")
    def add_field(self, depot: str, collection: str, dataset: str, payload: Body(type=FieldRequest),
                  correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to add a new field to a dataset in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.
            payload (Body): The payload containing the field request data.
                - type (FieldRequest): The type of the field request.
                    Payload Attributes:
                        name (str): The name of the new field.
                            This attribute is essential and represents the name of the field that needs to be added to a dataset.

                        type (str): The type of the new field.
                            This attribute indicates the data type of the new field, such as string, integer, float, etc.

                        precision (Optional[int]): The precision of the new field (optional).
                            Precision is relevant when the field is of numeric type (e.g., float or decimal),
                            and it represents the total number of significant digits in the number.

                        scale (Optional[int]): The scale of the new field (optional).
                            Scale is also relevant for numeric types and represents the number of digits to the right of the decimal point.

                        keyType (Optional[str]): The key type of the new field (optional).
                            This attribute might be used when the field represents a key or identifier with a specific type,
                            such as "primary key" or "foreign key."

                        valueType (Optional[str]): The value type of the new field (optional).
                            This attribute could be used to specify the type of values that the field will hold,
                            like "text," "number," "date," etc.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @delete("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/fields/{field}")
    def drop_field(self, depot: str, collection: str, dataset: str, field: str,
                   correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to drop a field from a dataset in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.
            field (str): The name of the field to be dropped.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @get("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}")
    def fetch_dataset(self, depot: str, collection: str, dataset: str,
                      correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> DatasetResponse:
        """
        Method to fetch a dataset from the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to fetch.

        Returns:
            DatasetResponse: An instance of the DatasetResponse class representing the fetched dataset.
        """
        pass

    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @json
    @post("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}")
    def create_dataset(self, depot: str, collection: str, dataset: str, payload: Body(type=DatasetRequest),
                       correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to create a new dataset in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the new dataset to be created.
            payload (Body): The payload containing the dataset request data.
                - type (DatasetRequest): The type of the dataset request.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @delete("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}")
    def drop_dataset(self, depot: str, collection: str, dataset: str, purge: Query('purge') = False,
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to drop (delete) a dataset from the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to drop.
            purge (Query): An optional query parameter to indicate whether to purge the dataset completely.
                - Default: False

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @headers({"Content-Type": "application/json"})
    @patch("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/partitions")
    def update_partition(self, depot: str, collection: str, dataset: str,
                         payload: Body(type=List[IcebergPartitionSpecRequest]),
                         correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
         Method to update partitions for a dataset in the specified collection of a depot.

         Parameters:
             depot (str): The name of the depot.
             collection (str): The name of the collection within the depot.
             dataset (str): The name of the dataset to update partitions.
             payload (Body): The payload containing the partition specification request data.
                 - type (List[IcebergPartitionSpecRequest]): The list of partition specification requests.
                    Attributes:
                        index (int): The index of the partition specification.
                        type (str): The type of partitioning, e.g., "hash", "range", etc.
                        column (str): The name of the column to use for partitioning.
                        name (Optional[str]): The optional name of the partition.
                        num_buckets (Optional[int]): The optional number of buckets for "hash" partitioning.
         Returns:
             None: This method does not return anything.
         """
        pass

    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @get("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/schema")
    def fetch_schema(self, depot: str, collection: str, dataset: str,
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> str:
        """
        Method to fetch the schema of a dataset in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to fetch the schema.

        Returns:
            str: A JSON string representing the schema of the dataset.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/depots/{depot}/collections/{collection}/datasets")
    def list_dataset(self, depot: str, collection: str,
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[str]:
        """
        Method to list datasets in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.

        Returns:
            List[str]: A list of dataset names available in the specified collection.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/stats")
    def show_stats(self, depot: str, collection: str, dataset: str,
                   correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> IcebergStats:
        """
        Method to retrieve statistics for a dataset in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to retrieve statistics.

        Returns:
            IcebergStats: An instance of the IcebergStats data model representing the dataset statistics.
                Attributes:
                    stats (Dict[str, str]): A dictionary containing general statistics for the dataset.
                    timeline (Dict[str, Dict[str, str]]): A dictionary representing the timeline of statistics.
                    properties (Dict[str, str]): A dictionary containing additional properties related to statistics.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/properties")
    def list_properties(self, depot: str, collection: str, dataset: str,
                        correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Dict[str, str]:
        """
        Method to list properties of a dataset in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to list properties.

        Returns:
            Dict[str, str]: A dictionary representing the properties of the dataset.
        """
        pass

    @raise_for_status_code
    @json
    @delete("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/properties")
    def remove_properties(self, depot: str, collection: str, dataset: str, payload: Body(List[str]),
                          correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to remove properties from a dataset in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset from which properties should be removed.
            payload (Body): The payload containing a list of property names to be removed.
                - type (List[str]): The list of property names to remove.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @patch("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/properties")
    def add_properties(self, depot: str, collection: str, dataset: str, payload: Body(Dict[str, str]),
                       correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to add properties to a dataset in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to which properties should be added.
            payload (Body): The payload containing a dictionary of property names and values to add.
                - type (Dict[str, str]): A dictionary of property names and their corresponding values.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/metadata")
    def list_metadata(self, depot: str, collection: str, dataset: str,
                      correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[MetadataVersionResponse]:
        """
        Method to list metadata versions for a dataset in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to list metadata versions.

        Returns:
            List[MetadataVersionResponse]: A list of MetadataVersionResponse objects representing metadata versions.
                Attributes:
                version (str): The version string representing the metadata version.
                timestamp (int): The timestamp associated with the metadata version.
        """
        pass

    @raise_for_status_code
    @json
    @patch("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/metadata/{version}")
    def set_metadata(self, depot: str, collection: str, dataset: str, version: str,
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to set metadata for a specific version of a dataset in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset for which metadata should be set.
            version (str): The version of the metadata file to be set.
                Valid options: "latest" for the latest version,
                               "v2.metadata.json" for a specific version,
                               "v2.gz.metadata.json" for a specific version (compressed).

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @patch("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/fields/{field}/nullable/{nullable}")
    def update_nullability(self, depot: str, collection: str, dataset: str, field: str, nullable: bool,
                           correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to update the nullability of a field in the specified dataset of a collection within a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset containing the field.
            field (str): The name of the field for which the nullability should be updated.
            nullable (bool): The new nullability status of the field. Set to True to make the field nullable,
                             or False to make it non-nullable.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/snapshots")
    def list_snapshots(self, depot: str, collection: str, dataset: str,
                       correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[SnapshotResponse]:
        """
        Method to list snapshots for a dataset in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to list snapshots.

        Returns:
            List[SnapshotResponse]: A list of SnapshotResponse objects representing the snapshots.
        """
        pass

    @raise_for_status_code
    @patch("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/snapshots/{id}")
    def set_snapshot(self, depot: str, collection: str, dataset: str, id: int,
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to set a specific snapshot for a dataset in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset for which the snapshot should be set.
            id (int): The ID of the snapshot to be set.
                eg: 566136990417338097

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @patch("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/fields/{field}/rename")
    def rename_field(self, depot: str, collection: str, dataset: str, field: str,
                     payload: Body(type=FieldRenameRequest),
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to rename a field in the specified dataset of a collection within a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset containing the field to be renamed.
            field (str): The name of the field to be renamed.
            payload (Body): The payload containing the new name of the field.
                - type (FieldRenameRequest): The request body with the new field name.
                  It should have the following attribute:
                  - new_name (str): The new name for the field.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @patch("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/fields/{field}/update")
    def update_field(self, depot: str, collection: str, dataset: str, field: str,
                     payload: Body(type=FieldUpdateRequest),
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to update properties of a field in the specified dataset of a collection within a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset containing the field to be updated.
            field (str): The name of the field to be updated.
            payload (Body): The payload containing the updated properties of the field.
                - type (FieldUpdateRequest): The request body with the updated properties of the field.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @post("api/v2/depots/{depot}/collections/{collection}")
    def create_namespace(self, depot: str, collection: str,
                         correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to create a new namespace (collection) within a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the new collection (namespace) to create.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/depots/{depot}/collections/{collection}/datasets/{dataset}/schemas")
    def fetch_schemas(self, depot: str, collection: str, dataset: str,
                      correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> str:
        """
        Method to fetch schemas for a dataset in the specified collection of a depot.

        Parameters:
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to fetch schemas.

        Returns:
            str: The schemas for the specified dataset in JSON format.
        """
        pass
