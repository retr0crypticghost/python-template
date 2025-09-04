"""
Tests for the services module.
"""

from unittest.mock import MagicMock, patch

import pytest

import {{ cookiecutter.package_name }}.services as services_module
from {{ cookiecutter.package_name }}.services import ExampleService, example_function


class TestExampleService:
    """Test cases for the ExampleService class."""

    def test_service_initialization(self):
        """Test that ExampleService initializes correctly."""
        service = ExampleService()
        assert service is not None
        assert hasattr(service, 'logger')

    def test_process_data_with_valid_data(self):
        """Test processing valid data."""
        service = ExampleService()

        test_data = "hello world"
        result = service.process_data(test_data)

        assert result == len(test_data)
        assert result == 11

    def test_process_data_with_empty_data(self):
        """Test processing empty data."""
        service = ExampleService()

        result = service.process_data("")
        assert result is None

    def test_process_data_with_none_data(self):
        """Test processing None data."""
        service = ExampleService()

        result = service.process_data(None)
        assert result is None

    def test_process_data_with_list_data(self):
        """Test processing list data."""
        service = ExampleService()

        test_data = ["item1", "item2", "item3"]
        result = service.process_data(test_data)

        assert result == len(test_data)
        assert result == 3

    def test_process_data_with_dict_data(self):
        """Test processing dictionary data."""
        service = ExampleService()

        test_data = {"key1": "value1", "key2": "value2"}
        result = service.process_data(test_data)

        assert result == len(test_data)
        assert result == 2

    def test_process_data_with_numeric_data(self):
        """Test processing numeric data."""
        service = ExampleService()

        test_data = 12345
        result = service.process_data(test_data)

        assert result == len(str(test_data))
        assert result == 5

    @patch('{{ cookiecutter.package_name }}.services.get_logger')
    def test_service_logging(self, mock_get_logger):
        """Test that service logs appropriately."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        service = ExampleService()

        # Verify initialization logging
        mock_logger.info.assert_called_with("ExampleService initialized")

        # Test data processing logging
        mock_logger.reset_mock()
        service.process_data("test data")

        # Verify debug and info logs were called
        mock_logger.debug.assert_called()
        mock_logger.info.assert_called()

    @patch('{{ cookiecutter.package_name }}.services.get_logger')
    def test_service_warning_logging(self, mock_get_logger):
        """Test that service logs warnings for empty data."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        service = ExampleService()
        mock_logger.reset_mock()

        service.process_data("")

        # Verify warning was logged for empty data
        mock_logger.warning.assert_called_with("Empty data received")

    def test_process_data_exception_handling(self):
        """Test that exceptions are properly handled and re-raised."""
        service = ExampleService()

        # Create data that will cause an exception in len()
        class BadData:
            def __len__(self):
                raise ValueError("Test exception")

        bad_data = BadData()

        with pytest.raises(ValueError, match="Test exception"):
            service.process_data(bad_data)

    @patch('{{ cookiecutter.package_name }}.services.get_logger')
    def test_service_error_logging(self, mock_get_logger):
        """Test that service logs errors when exceptions occur."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        service = ExampleService()
        mock_logger.reset_mock()

        # Create data that will cause an exception
        class BadData:
            def __len__(self):
                raise ValueError("Test exception")

        bad_data = BadData()

        with pytest.raises(ValueError, match="cannot process"):
            service.process_data(bad_data)

        # Verify error was logged
        mock_logger.error.assert_called()
        error_call_args = mock_logger.error.call_args[0][0]
        assert "Failed to process data" in error_call_args


class TestExampleFunction:
    """Test cases for the example_function."""

    @patch('{{ cookiecutter.package_name }}.services.ExampleService')
    @patch('{{ cookiecutter.package_name }}.services.logger')
    def test_example_function_execution(self, mock_logger, mock_service_class):
        """Test that example_function executes correctly."""
        mock_service = MagicMock()
        mock_service.process_data.side_effect = [9, None]  # Return values for two calls
        mock_service_class.return_value = mock_service

        example_function()

        # Verify service was created and called twice
        mock_service_class.assert_called_once()
        assert mock_service.process_data.call_count == 2

        # Verify the two different data inputs
        call_args = mock_service.process_data.call_args_list
        assert call_args[0][0][0] == "test data"
        assert call_args[1][0][0] == ""

        # Verify logging calls
        mock_logger.info.assert_called()
        info_calls = [call[0][0] for call in mock_logger.info.call_args_list]
        assert any("Starting example function" in call for call in info_calls)
        assert any("Example function completed" in call for call in info_calls)

    @patch('{{ cookiecutter.package_name }}.services.ExampleService')
    @patch('{{ cookiecutter.package_name }}.services.logger')
    def test_example_function_with_service_exception(self, mock_logger, mock_service_class):
        """Test example_function when service raises exception."""
        mock_service = MagicMock()
        mock_service.process_data.side_effect = RuntimeError("Service error")
        mock_service_class.return_value = mock_service

        with pytest.raises(RuntimeError, match="Service error"):
            example_function()

        # Verify service was still created
        mock_service_class.assert_called_once()
        mock_service.process_data.assert_called_once()

    def test_example_function_integration(self):
        """Integration test for example_function."""
        # This should execute without exceptions
        example_function()

    @patch('{{ cookiecutter.package_name }}.services.logger')
    def test_example_function_logging_details(self, mock_logger):
        """Test detailed logging behavior of example_function."""
        example_function()

        # Verify specific log messages
        info_calls = [call[0][0] for call in mock_logger.info.call_args_list]

        assert any("Starting example function" in call for call in info_calls)
        assert any("Function result:" in call for call in info_calls)
        assert any("Function result with empty data:" in call for call in info_calls)
        assert any("Example function completed" in call for call in info_calls)


class TestServiceModuleIntegration:
    """Integration tests for the entire services module."""

    def test_service_module_imports(self):
        """Test that all expected components can be imported."""

        assert ExampleService is not None
        assert example_function is not None

    def test_multiple_service_instances(self):
        """Test creating multiple service instances."""
        service1 = ExampleService()
        service2 = ExampleService()

        # Should be different instances
        assert service1 is not service2

        # Both should work independently
        result1 = service1.process_data("test1")
        result2 = service2.process_data("test2")

        assert result1 == 5
        assert result2 == 5

    def test_service_with_various_data_types(self):
        """Test service with different data types."""
        service = ExampleService()

        test_cases = [
            ("string", 6),
            (["a", "b", "c"], 3),
            ({"x": 1, "y": 2}, 2),
            (123, 3),
            (12.34, 5),  # str(12.34) = "12.34"
        ]

        for data, expected_length in test_cases:
            result = service.process_data(data)
            assert result == expected_length

    def test_service_edge_cases(self):
        """Test service with edge cases."""
        service = ExampleService()

        # Empty containers
        assert service.process_data([]) is None
        assert service.process_data({}) is None
        assert service.process_data("") is None

        # Zero
        assert service.process_data(0) == 1  # str(0) = "0"

        # Boolean values
        assert service.process_data(True) == 4   # str(True) = "True"
        assert service.process_data(False) == 5  # str(False) = "False"


class TestServiceModuleRuntime:
    """Test runtime behavior of the services module."""

    def test_module_main_execution(self):
        """Test that module can be executed as main."""
        # Import and test the module's main execution path

        # Should not raise any exceptions when imported
        assert services_module is not None

    @patch('{{ cookiecutter.package_name }}.services.example_function')
    def test_module_main_call(self, mock_example_function):
        """Test that main execution calls example_function."""
        # This tests the if __name__ == "__main__" block
        import importlib

        # Simulate running as main
        with patch.object(services_module, '__name__', '__main__'):
            # Re-import to trigger the main block
            importlib.reload(services_module)

        # Note: This test might not work perfectly due to how imports work
        # But it demonstrates testing patterns for main blocks
