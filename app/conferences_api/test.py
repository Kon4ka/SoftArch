import unittest
import requests

BASE_URL = "http://127.0.0.1:8080"
conference_id: str = ""


class TestAPI(unittest.TestCase):
    def setUp(self):
        conference_data = {
            "name": "Test Conference",
            "reports": [],
            "date_of_conference": 20220410,
            "max_authors": 100
        }
        response = requests.post(
            f"{BASE_URL}/conferences/", json=conference_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.text)
        self.conference_id = response.json()

    def test_create_conference(self):
        pass  # Nothing to do, conference already created in setUp() method

    def test_read_conference(self):
        response = requests.get(f"{BASE_URL}/conferences/{self.conference_id}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

    def test_update_conference(self):
        updated_conference_data = {
            "name": "Updated Conference",
            "reports": [],
            "date_of_conference": 20230410,
            "max_authors": 200
        }
        response = requests.put(
            f"{BASE_URL}/conferences/{self.conference_id}", json=updated_conference_data)
        self.assertEqual(response.status_code, 200)
        # Expecting 1, as one document was updated
        self.assertEqual(response.json(), 1)

    def test_delete_conference(self):
        response = requests.delete(
            f"{BASE_URL}/conferences/{self.conference_id}")
        self.assertEqual(response.status_code, 200)
        # Expecting 1, as one document was deleted
        self.assertEqual(response.json(), 1)


if __name__ == '__main__':
    unittest.main()
