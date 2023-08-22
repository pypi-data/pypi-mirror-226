import unittest
from unittest.mock import MagicMock, Mock

from postgrest.exceptions import APIError
from tensorage.backend.database import DatabaseContext
import numpy as np


class TestDatabaseContext(unittest.TestCase):
    def setUp(self):
        # create a mock backend
        self.mock_backend = MagicMock()

        # now mock all the stuff in the backend
        self.mock_backend.client.table.return_value.select.return_value.limit.return_value.execute = Mock(return_value=True)

        # add a dataset response
        mock_dataset_response = MagicMock()
        mock_dataset_response.data = [{'id': 1, 'key': 'test', 'shape': [1, 2, 3], 'ndim': 3, 'is_shared': False, 'type': 'float32'}]
        tensor_mock = MagicMock()
        tensor_mock.data = [{'tensor': np.random.random((1, 2, 3)).astype(np.float32)}]

        # mock insert and select method
        self.mock_backend.client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_dataset_response
        self.mock_backend.client.table.return_value.insert.return_value.execute.return_value = mock_dataset_response
        self.mock_backend.client.table.return_value.delete.return_value.eq.return_value.execute.return_value = None
        self.mock_backend.client.rpc.return_value.execute.return_value = tensor_mock

        # create a DatabaseContext instance
        self.db_context = DatabaseContext(self.mock_backend)

    def test_check_schema_installed(self):
        # create a mock APIError that will be raised when the table is not found
        def raise_api_error():
            raise APIError({'message': 'Table not found', 'code': '42P01'})
        
        # here we need an extra backend to mock the APIError
        mock_backend = MagicMock()
        mock_backend.client.table.return_value.select.return_value.limit.return_value.execute.side_effect = raise_api_error

        # create a DatabaseContext instance and call the check_schema_installed method
        db_context = DatabaseContext(mock_backend)
        result = db_context.check_schema_installed()

        # assert that the result is False (since the table is not found)
        self.assertFalse(result)

    def test_insert_dataset(self):
        # call the insert_dataset method
        dataset = self.db_context.insert_dataset(key='test', shape=[1, 2, 3], dim=3)

        # assert that the dataset object has the correct attributes
        self.assertEqual(dataset.id, 1)
        self.assertEqual(dataset.key, 'test')
        self.assertEqual(dataset.shape, [1, 2, 3])
        self.assertEqual(dataset.ndim, 3)
        self.assertEqual(dataset.is_shared, False)
        self.assertEqual(dataset.type, 'float32')

    def test_get_dataset(self):
        # call the get_dataset method
        dataset = self.db_context.get_dataset(key='test')

        # assert that the dataset object has the correct attributes
        self.assertEqual(dataset.id, 1)
        self.assertEqual(dataset.key, 'test')
        self.assertEqual(dataset.shape, [1, 2, 3])
        self.assertEqual(dataset.ndim, 3)

    def test_remove_dataset(self):
        # call the remove_dataset method
        return_val = self.db_context.remove_dataset(key='test')

        # assert that no error was raised
        self.assertTrue(return_val)
    
    def test_insert_tensor(self):
        # call the insert tensor method
        return_val = self.db_context.insert_tensor(data_id=42, data=np.random.random((1, 2, 3)).astype(np.float32))

        self.assertTrue(return_val)

    def test_insert_tensor_exception(self):
        # create a mock APIError that will be raised when the insert does not work
        def raise_api_error():
            raise APIError({'message': 'Uniqueness violation', 'code': '32505'})

        # here we need an extra backend to mock the APIError
        mock_backend = MagicMock()
        mock_backend.client.table.return_value.insert.return_value.execute.side_effect = raise_api_error

        # create a DatabaseContext instance and call the insert_tensor method
        db_context = DatabaseContext(mock_backend)
        
        with self.assertRaises(APIError) as e:
            db_context.insert_tensor(data_id=42, data=np.random.random((1, 2, 3)).astype(np.float32))

            self.assertEqual(e.message, 'Uniqueness violation')
    
    def test_get_tensor(self):
        # call the get tensor method
        response = self.db_context.get_tensor(key='test', index_low=1, index_up=1, slice_low=[0,0], slice_up=[2,3])

        # assert it is an array
        self.assertTrue(isinstance(response, np.ndarray))
        self.assertEqual(response.shape, (1, 2, 3))

if __name__ == '__main__':
    unittest.main()
