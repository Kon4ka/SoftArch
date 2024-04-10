import unittest
import requests

BASE_URL = "http://127.0.0.1:8081"
report_id: str = ""


class TestAPI(unittest.TestCase):
    def setUp(self):
        report_data = {
            "title": "Test Report",
            "type": "Test Type",
            "text": "Test Text",
            "author_id": 123
        }
        response = requests.post(f"{BASE_URL}/reports/", json=report_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("report_id", response.json())
        self.report_id = response.json()['report_id']

    def test_create_report(self):
        pass

    def test_read_report(self):
        response = requests.get(f"{BASE_URL}/reports/{self.report_id}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

    def test_update_report(self):
        updated_report_data = {
            "title": "Updated Title",
            "type": "Updated Type",
            "text": "Updated Text",
            "author_id": 456
        }
        response = requests.put(
            f"{BASE_URL}/reports/{self.report_id}", json=updated_report_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Отчет успешно обновлен")

    def test_delete_report(self):
        response = requests.delete(f"{BASE_URL}/reports/{self.report_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Отчет успешно удален")


if __name__ == '__main__':
    unittest.main()
