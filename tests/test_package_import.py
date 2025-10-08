"""
Tests for basic package imports and availability.
"""

import pytest


class TestPackageImport:
    """Test basic package import functionality."""

    def test_import_crewai_accelerate(self):
        """Test that we can import the main package."""
        import crewai_accelerate
        assert crewai_accelerate is not None

    def test_package_version(self):
        """Test that package has version information."""
        import crewai_accelerate
        assert hasattr(crewai_accelerate, '__version__')
        assert isinstance(crewai_accelerate.__version__, str)

    def test_acceleration_implementation_flag(self):
        """Test that package has acceleration implementation flag."""
        import crewai_accelerate
        assert hasattr(crewai_accelerate, 'HAS_ACCELERATION_IMPLEMENTATION')
        assert isinstance(crewai_accelerate.HAS_ACCELERATION_IMPLEMENTATION, bool)

    def test_acceleration_availability_functions(self):
        """Test acceleration availability detection functions."""
        from crewai_accelerate import is_acceleration_available, get_acceleration_status

        # Should be able to call these functions
        available = is_acceleration_available()
        status = get_acceleration_status()

        assert isinstance(available, bool)
        assert isinstance(status, str)

    def test_main_component_imports(self):
        """Test that we can import main components."""
        from crewai_accelerate import (
            AcceleratedMemoryStorage,
            AcceleratedToolExecutor,
            AcceleratedTaskExecutor
        )

        assert AcceleratedMemoryStorage is not None
        assert AcceleratedToolExecutor is not None
        assert AcceleratedTaskExecutor is not None

    def test_serialization_imports(self):
        """Test that we can import serialization components."""
        try:
            from crewai_accelerate import AcceleratedMessage
            assert AcceleratedMessage is not None
        except ImportError:
            # Serialization components might not be available
            pass

    def test_database_imports(self):
        """Test that we can import database components."""
        try:
            from crewai_accelerate import AcceleratedSQLiteWrapper
            assert AcceleratedSQLiteWrapper is not None
        except ImportError:
            # Database components might not be available
            pass


class TestComponentAvailability:
    """Test availability of different components."""

    def test_memory_component_creation(self):
        """Test that memory components can be created."""
        from crewai_rust import RustMemoryStorage

        storage = RustMemoryStorage()
        assert storage is not None
        assert hasattr(storage, 'implementation')

    def test_tool_component_creation(self):
        """Test that tool components can be created."""
        from crewai_rust import RustToolExecutor

        executor = RustToolExecutor()
        assert executor is not None

    def test_task_component_creation(self):
        """Test that task components can be created."""
        from crewai_rust import RustTaskExecutor

        executor = RustTaskExecutor()
        assert executor is not None

    def test_component_methods_exist(self):
        """Test that components have expected methods."""
        from crewai_rust import RustMemoryStorage, RustToolExecutor

        # Memory storage methods
        storage = RustMemoryStorage()
        assert hasattr(storage, 'save')
        assert hasattr(storage, 'search')

        # Tool executor methods
        executor = RustToolExecutor()
        assert hasattr(executor, 'execute_tool')


class TestEnvironmentInfo:
    """Test environment information functions."""

    def test_environment_info_function(self):
        """Test environment information retrieval."""
        try:
            from crewai_rust import get_environment_info
            info = get_environment_info()
            assert isinstance(info, dict)
        except ImportError:
            # Function might not be implemented
            pass

    def test_performance_metrics_function(self):
        """Test performance metrics retrieval."""
        try:
            from crewai_rust import get_performance_metrics
            metrics = get_performance_metrics()
            assert isinstance(metrics, dict)
        except ImportError:
            # Function might not be implemented
            pass

    def test_rust_status_details(self):
        """Test detailed Rust status information."""
        from crewai_rust import get_rust_status

        status = get_rust_status()
        assert isinstance(status, str)
        assert len(status) > 0


if __name__ == "__main__":
    pytest.main([__file__])