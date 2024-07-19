import unittest

import unittest.test
from app import app, collection
from flask import json
from bson.objectid import ObjectId

class FlaskMongoCRUDTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # This method is run once for each class before any tests are run.
        cls.client = app.test_client()
        cls.client_testing = True
    
    def setUp(self):
        # This method is run before each individual test.
        # Clear the collection before each test
        collection.delete_many({})
    
    def test_create_item(self):
        response = self.client.post('/items', json={'name': 'Test Item', 'description': 'This is a test item'})
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('_id', response_data)
        
    def test_get_items(self):
        # Insert a test item
        item_id = collection.insert_one({'name': 'Test Item', 'description': 'This is a test item'}).inserted_id
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['_id'], str(item_id))
        
    def test_get_item(self):
        # Insert a test item
        item_id = collection.insert_one({'name': 'Test Item', 'description': 'This is a test item'}).inserted_id
        response = self.client.get(f'/item/{item_id}')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['_id'], str(item_id))
        
    def test_update_item(self):
        # Insert a test item
        item_id = collection.insert_one({'name': 'Test Item Update', 'description': 'This is a test item'}).inserted_id
        response = self.client.put(f'/item/{item_id}', json={'name': 'Updated Item', 'description': 'Updated description'})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Item updated successfully')
        
        # Verify the update
        updated_item = collection.find_one({'_id': ObjectId(item_id)})
        self.assertEqual(updated_item['name'], 'Updated Item')
        self.assertEqual(updated_item['description'], 'Updated description')
        
    def test_delete_item(self):
        # Insert a test item
        item_id = collection.insert_one({'name': 'Test Item', 'description': 'This is a test item'}).inserted_id
        response = self.client.delete(f'/item/{item_id}')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Item deleted successfully')

        # Verify the deletion
        deleted_item = collection.find_one({'_id': ObjectId(item_id)})
        self.assertIsNone(deleted_item)

if __name__ == '__main__':
    unittest.main()