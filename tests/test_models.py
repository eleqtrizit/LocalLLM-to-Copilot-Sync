"""
Tests for the models module.
"""

import unittest

from copilot_model_sync.models import apply_update_logic, compare_models


class TestModels(unittest.TestCase):
    """Test cases for the models module."""

    def test_compare_models_matching(self):
        """Test comparing models with matching models."""
        current_models = {"model1": {"name": "model1"}}
        disabled_models = {}
        api_models = [{"id": "model1"}]

        result = compare_models(current_models, disabled_models, api_models)
        self.assertEqual(result["matching"], ["model1"])
        self.assertEqual(result["obsolete"], [])
        self.assertEqual(result["to_reenable"], [])
        self.assertEqual(result["new_models"], [])

    def test_compare_models_obsolete(self):
        """Test comparing models with obsolete models."""
        current_models = {"model1": {"name": "model1"}, "model2": {"name": "model2"}}
        disabled_models = {}
        api_models = [{"id": "model1"}]

        result = compare_models(current_models, disabled_models, api_models)
        self.assertEqual(result["matching"], ["model1"])
        self.assertEqual(result["obsolete"], ["model2"])
        self.assertEqual(result["to_reenable"], [])
        self.assertEqual(result["new_models"], [])

    def test_compare_models_to_reenable(self):
        """Test comparing models with models to re-enable."""
        current_models = {"model1": {"name": "model1"}}
        disabled_models = {"model2": {"name": "model2"}}
        api_models = [{"id": "model1"}, {"id": "model2"}]

        result = compare_models(current_models, disabled_models, api_models)
        self.assertEqual(result["matching"], ["model1"])
        self.assertEqual(result["obsolete"], [])
        self.assertEqual(result["to_reenable"], ["model2"])
        self.assertEqual(result["new_models"], [])

    def test_compare_models_new_models(self):
        """Test comparing models with new models."""
        current_models = {"model1": {"name": "model1"}}
        disabled_models = {}
        api_models = [{"id": "model1"}, {"id": "model2"}]

        result = compare_models(current_models, disabled_models, api_models)
        self.assertEqual(result["matching"], ["model1"])
        self.assertEqual(result["obsolete"], [])
        self.assertEqual(result["to_reenable"], [])
        self.assertEqual(result["new_models"], ["model2"])

    def test_apply_update_logic_obsolete(self):
        """Test applying update logic for obsolete models."""
        settings = {
            "github.copilot.chat.customOAIModels": {
                "model1": {"name": "model1"},
                "model2": {"name": "model2"}
            },
            "github.copilot.chat.customOAIModels.disabled": {}
        }

        comparisons = {
            "matching": ["model1"],
            "obsolete": ["model2"],
            "to_reenable": [],
            "new_models": []
        }

        result = apply_update_logic(settings, comparisons, "http://localhost:8080")
        self.assertIn("model1", result["github.copilot.chat.customOAIModels"])
        self.assertIn("model2", result["github.copilot.chat.customOAIModels.disabled"])
        self.assertNotIn("model2", result["github.copilot.chat.customOAIModels"])

    def test_apply_update_logic_reenable(self):
        """Test applying update logic for re-enabling models."""
        settings = {
            "github.copilot.chat.customOAIModels": {
                "model1": {"name": "model1"}
            },
            "github.copilot.chat.customOAIModels.disabled": {
                "model2": {"name": "model2"}
            }
        }

        comparisons = {
            "matching": ["model1"],
            "obsolete": [],
            "to_reenable": ["model2"],
            "new_models": []
        }

        result = apply_update_logic(settings, comparisons, "http://localhost:8080")
        self.assertIn("model1", result["github.copilot.chat.customOAIModels"])
        self.assertIn("model2", result["github.copilot.chat.customOAIModels"])
        self.assertNotIn("model2", result["github.copilot.chat.customOAIModels.disabled"])

    def test_apply_update_logic_new_models(self):
        """Test applying update logic for new models."""
        settings = {
            "github.copilot.chat.customOAIModels": {
                "model1": {"name": "model1"}
            },
            "github.copilot.chat.customOAIModels.disabled": {}
        }

        comparisons = {
            "matching": ["model1"],
            "obsolete": [],
            "to_reenable": [],
            "new_models": ["model2"]
        }

        result = apply_update_logic(settings, comparisons, "http://localhost:8080")
        self.assertIn("model1", result["github.copilot.chat.customOAIModels"])
        self.assertIn("model2", result["github.copilot.chat.customOAIModels"])

    def test_apply_update_logic_api_key_required_new_models(self):
        """Test applying update logic with api_key_required flag for new models."""
        settings = {
            "github.copilot.chat.customOAIModels": {},
            "github.copilot.chat.customOAIModels.disabled": {}
        }

        comparisons = {
            "matching": [],
            "obsolete": [],
            "to_reenable": [],
            "new_models": ["model1"]
        }

        result = apply_update_logic(settings, comparisons, "http://localhost:8080", True)
        self.assertIn("model1", result["github.copilot.chat.customOAIModels"])
        self.assertTrue(result["github.copilot.chat.customOAIModels"]["model1"]["requiresAPIKey"])

    def test_apply_update_logic_api_key_required_existing_models(self):
        """Test applying update logic with api_key_required flag for existing models."""
        settings = {
            "github.copilot.chat.customOAIModels": {
                "model1": {
                    "name": "model1",
                    "url": "http://localhost:8080/v1/chat/completions",
                    "requiresAPIKey": False
                },
                "model2": {
                    "name": "model2",
                    "url": "http://other-server:8080/v1/chat/completions",
                    "requiresAPIKey": False
                }
            },
            "github.copilot.chat.customOAIModels.disabled": {
                "model3": {
                    "name": "model3",
                    "url": "http://localhost:8080/v1/chat/completions",
                    "requiresAPIKey": False
                }
            }
        }

        comparisons = {
            "matching": ["model1"],
            "obsolete": [],
            "to_reenable": [],
            "new_models": []
        }

        result = apply_update_logic(settings, comparisons, "http://localhost:8080", True)
        # Model with matching base URL should have requiresAPIKey set to True
        self.assertTrue(result["github.copilot.chat.customOAIModels"]["model1"]["requiresAPIKey"])
        # Model with different base URL should remain unchanged
        self.assertFalse(result["github.copilot.chat.customOAIModels"]["model2"]["requiresAPIKey"])
        # Disabled model with matching base URL should also have requiresAPIKey set to True
        self.assertTrue(result["github.copilot.chat.customOAIModels.disabled"]["model3"]["requiresAPIKey"])


if __name__ == '__main__':
    unittest.main()
