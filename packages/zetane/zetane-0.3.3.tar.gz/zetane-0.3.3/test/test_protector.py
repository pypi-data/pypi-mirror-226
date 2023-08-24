import sys
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

SCRIPT_DIR = str(Path(__file__).absolute().parent)
ZETANE_DIR = str(Path(__file__).absolute().parent.parent)
sys.path.append(ZETANE_DIR)
load_dotenv(SCRIPT_DIR + "/.env")

import zetane
import unittest

# For running tests, need to generate a protector API key
# set it with an env var `ZETANE_API_KEY`
# which you can do either from the command line before running tests
# or by adding a .env file in this directory with that env var

class API_Test(unittest.TestCase):
    def setUp(self):
        zetane.config()

    def test_auth(self):
        self.assertIsNotNone(zetane.default_client.user)

    def test_default_org(self):
        self.assertIsNotNone(zetane.default_client.org)

    def test_create_project(self):
        res = zetane.create_project("Test Project 1")
        self.assertEqual(res.status_code, 201)
        res = zetane.delete_project("Test Project 1")
        self.assertEqual(res.status_code, 200)

    def test_upload_dataset(self):
        zetane.delete_project("Birds")
        zetane.create_project("Birds")
        res = zetane.upload_dataset(SCRIPT_DIR + '/data/birds.zip', project="Birds", name="bird_dataset")
        json_res = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_res['name'], 'bird_dataset')
        self.assertEqual(json_res['upload_status'], {'status': 'Ready'})
        res = zetane.delete_project("Birds")
        self.assertEqual(res.status_code, 200)

    def test_upload_model(self):
        zetane.create_project("Birds")
        res = zetane.upload_model(SCRIPT_DIR + '/data/model.pt', project="Birds", name="bird_model")
        json_res = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_res['name'], 'bird_model')
        self.assertEqual(json_res['upload_status'], {'status': 'Ready'})
        res = zetane.delete_project("Birds")
        self.assertEqual(res.status_code, 200)

    def test_report(self):
        test = {
            "blur": {
                "intervals": "3",
                "max": "5",
                "min": "3"
            },
            "elastic transform": {
                "intervals": "5",
                "max": "4",
                "min": "2",
                "xai": []
            },
        }
        zetane.create_project("Birds")

        model = zetane.upload_model(SCRIPT_DIR + '/data/model.pt', project="Birds", name="bird_model")
        dataset = zetane.upload_dataset(SCRIPT_DIR + '/data/birds.zip', project="Birds", name="bird_dataset")
        report = zetane.report(test_json=test, input_shape=[None, 256, 256, 3], model_type="image_classification", model="model.pt", dataset="birds.zip", autoRun=True)
        res = zetane.delete_project("Birds")

        self.assertTrue(report)


if __name__ == '__main__':
    zetane.config()
    unittest.main()




