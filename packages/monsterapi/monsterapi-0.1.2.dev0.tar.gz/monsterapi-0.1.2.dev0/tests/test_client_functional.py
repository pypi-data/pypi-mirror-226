import os
import pytest
import unittest
from monsterapi import client
from monsterapi.InputDataModels import LLMInputModel1, LLMInputModel2, SDInputModel, MODELS_TO_DATAMODEL

enabled_models = [
    "falcon-7b-instruct",
    "llama2-7b-chat", 
    "mpt-7b-instruct",
    "falcon-40b-instruct",
    "mpt-30b-instruct",  
    "sdxl-base", 
    "txt2img"
]

class TestMClientFunctional(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = client()
        cls.sample_data = {
            LLMInputModel1: {"prompt": "Help with testing"},
            LLMInputModel2: {"prompt": "Provide some instruction"},
            SDInputModel: {"prompt": "Sunset over a mountain range"}
        }

    @classmethod
    def create_test_function(cls, model_name, data_model):
        def test_func(self):
            if model_name in enabled_models:
                input_data = self.sample_data[data_model]
                response = self.client.get_response(model_name, input_data)

                self.assertIn("process_id", response)
                process_id = response["process_id"]

                # Check status
                status_response = self.client.get_status(process_id)
                self.assertIn("status", status_response)
                if status_response["status"] == "FAILED":
                    self.fail(f"Failed to get response for model {model_name} with process id {process_id}.")

                # If not failed, wait and get result
                result_response = self.client.wait_and_get_result(process_id, timeout=120)
            
                if data_model == SDInputModel:
                    self.assertIn("output", result_response)
                else:
                    self.assertIn("text", result_response)
        return test_func

# Dynamically add test methods
for model, data_model in MODELS_TO_DATAMODEL.items():
    target_function = TestMClientFunctional.create_test_function(model, data_model)
    test_name = f"test_{model}_functionally"
    setattr(TestMClientFunctional, test_name, target_function)

if __name__ == "__main__":
    unittest.main()
