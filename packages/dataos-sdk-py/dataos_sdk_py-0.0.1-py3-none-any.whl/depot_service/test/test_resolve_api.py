import unittest
from unittest.mock import patch, MagicMock
from depot_service.depot_service_client import DepotServiceClientBuilder
from env import env
from depot_service.models.address_info import AddressInfo


class TestResolveApiWithDepotServiceClient(unittest.TestCase):

    def setUp(self):
        # Create an instance of ResolveApi with a mock DepotServiceClient
        builder = DepotServiceClientBuilder()
        builder.base_url = env["URL"]
        builder.apikey = env["KEY"]
        self.mock_client = builder.build()

    def test_resolve_address_with_depot_service_client(self):
        # Mock the response data from the DepotServiceClient
        mock_response_data = {'depot': 'icebase', 'type': 'abfss', 'collection': 'retail', 'dataset': 'customer',
                              'format': 'iceberg', 'external': True, 'source': 'icebase', 'connection': {}}

        # Set the mock response for the client's resolve method
        self.mock_client.resolve_api.resolve = MagicMock(return_value=AddressInfo(**mock_response_data))

        # Call the resolve method with a test address
        address = "dataos://test:retail/city"
        resolved_address = self.mock_client.resolve_api.resolve(address=address)
        print(resolved_address)
        # Assert that the client's resolve method was called with the correct data
        self.mock_client.resolve_api.resolve.assert_called_once_with(address=address)

        # Assert that the resolved_address object contains the expected data
        self.assertIsInstance(resolved_address, AddressInfo)
        # self.assertEqual(resolved_address.street_address, mock_response_data["street_address"])
        # self.assertEqual(resolved_address.city, mock_response_data["city"])
        # self.assertEqual(resolved_address.state, mock_response_data["state"])
        # self.assertEqual(resolved_address.postal_code, mock_response_data["postal_code"])
        # Add other assertions for other properties if needed


if __name__ == "__main__":
    unittest.main()
