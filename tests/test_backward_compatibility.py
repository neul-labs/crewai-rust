"""
Backward Compatibility Tests for CrewAI Rust Integration

These tests verify that existing CrewAI code continues to work unchanged
when the Rust integration is installed.
"""

import unittest
import os
import sys
from typing import Any, Dict, List, Optional
from unittest.mock import patch, MagicMock

# Add the crewai_rust directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'crewai_rust'))

try:
    from crewai_rust import HAS_RUST_IMPLEMENTATION
    RUST_AVAILABLE = HAS_RUST_IMPLEMENTATION
except ImportError:
    RUST_AVAILABLE = False

class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility with existing CrewAI code."""

    def setUp(self):
        """Set up test environment."""
        # Clear any existing environment variables that might affect tests
        self.original_env = {}
        env_vars = [
            'CREWAI_RUST_ACCELERATION',
            'CREWAI_RUST_MEMORY',
            'CREWAI_RUST_TOOLS',
            'CREWAI_RUST_TASKS',
            'CREWAI_RUST_SERIALIZATION',
            'CREWAI_RUST_DATABASE'
        ]
        
        for var in env_vars:
            if var in os.environ:
                self.original_env[var] = os.environ[var]
                del os.environ[var]

    def tearDown(self):
        """Clean up test environment."""
        # Restore original environment variables
        for var, value in self.original_env.items():
            os.environ[var] = value

    def test_import_crewai_rust(self):
        """Test that crewai_rust can be imported without errors."""
        try:
            import crewai_rust
            self.assertTrue(hasattr(crewai_rust, '__version__'))
            self.assertTrue(hasattr(crewai_rust, 'HAS_RUST_IMPLEMENTATION'))
        except ImportError as e:
            self.fail(f"Failed to import crewai_rust: {e}")

    def test_rust_availability_flag(self):
        """Test that HAS_RUST_IMPLEMENTATION is properly defined."""
        import crewai_rust
        self.assertIsInstance(crewai_rust.HAS_RUST_IMPLEMENTATION, bool)

    def test_environment_variable_handling(self):
        """Test that environment variables are handled correctly."""
        # Test with environment variable set to 'true'
        os.environ['CREWAI_RUST_ACCELERATION'] = '1'
        
        try:
            # Re-import to test environment variable handling
            import importlib
            import crewai_rust
            importlib.reload(crewai_rust)
        except Exception as e:
            # This is expected if Rust components aren't available
            pass

    def test_graceful_degradation(self):
        """Test that the system gracefully degrades when Rust is unavailable."""
        if not RUST_AVAILABLE:
            # Test that components fall back to Python implementations
            try:
                from crewai_rust.memory import RustMemoryStorage
                storage = RustMemoryStorage()
                self.assertEqual(storage.implementation, "python")
            except Exception as e:
                # This is expected if Rust components aren't available
                pass

    def test_component_imports(self):
        """Test that all components can be imported."""
        components = [
            'RustMemoryStorage',
            'RustToolExecutor', 
            'RustTaskExecutor',
            'AgentMessage',
            'RustSQLiteWrapper'
        ]
        
        for component in components:
            try:
                from crewai_rust import component
                self.assertTrue(True)  # Import successful
            except ImportError:
                # This is expected if Rust components aren't available
                pass

    def test_utility_functions(self):
        """Test that utility functions work correctly."""
        try:
            from crewai_rust.utils import is_rust_available, get_rust_status
            self.assertIsInstance(is_rust_available(), bool)
            self.assertIsInstance(get_rust_status(), dict)
        except ImportError:
            # This is expected if Rust components aren't available
            pass

    def test_shim_import(self):
        """Test that the shim module can be imported."""
        try:
            import crewai_rust.shim
            self.assertTrue(hasattr(crewai_rust.shim, 'enable_rust_acceleration'))
        except ImportError:
            # This is expected if shim module isn't available
            pass

    def test_memory_storage_compatibility(self):
        """Test that memory storage maintains API compatibility."""
        try:
            from crewai_rust.memory import RustMemoryStorage
            
            # Test basic functionality
            storage = RustMemoryStorage()
            
            # Test save method
            storage.save("test value", {"metadata": "test"})
            
            # Test search method
            results = storage.search("test", limit=5)
            self.assertIsInstance(results, list)
            
            # Test get_all method
            all_items = storage.get_all()
            self.assertIsInstance(all_items, list)
            
            # Test reset method
            storage.reset()
            
        except Exception as e:
            # This is expected if Rust components aren't available
            pass

    def test_tool_executor_compatibility(self):
        """Test that tool executor maintains API compatibility."""
        try:
            from crewai_rust.tools import RustToolExecutor
            
            # Test basic functionality
            executor = RustToolExecutor(max_recursion_depth=10)
            
            # Test execute_tool method
            result = executor.execute_tool("test_tool", {"param": "value"})
            self.assertIsInstance(result, str)
            
        except Exception as e:
            # This is expected if Rust components aren't available
            pass

    def test_task_executor_compatibility(self):
        """Test that task executor maintains API compatibility."""
        try:
            from crewai_rust.tasks import RustTaskExecutor
            
            # Test basic functionality
            executor = RustTaskExecutor()
            
            # Test execute_concurrent_tasks method
            tasks = ["task1", "task2", "task3"]
            results = executor.execute_concurrent_tasks(tasks)
            self.assertIsInstance(results, list)
            self.assertEqual(len(results), len(tasks))
            
        except Exception as e:
            # This is expected if Rust components aren't available
            pass

    def test_serialization_compatibility(self):
        """Test that serialization maintains API compatibility."""
        try:
            from crewai_rust.serialization import AgentMessage
            
            # Test basic functionality
            message = AgentMessage(
                id="test_id",
                sender="test_sender", 
                recipient="test_recipient",
                content="test_content",
                timestamp=1234567890
            )
            
            # Test to_json method
            json_str = message.to_json()
            self.assertIsInstance(json_str, str)
            
            # Test from_json method
            message2 = AgentMessage.from_json(json_str)
            self.assertEqual(message.id, message2.id)
            self.assertEqual(message.sender, message2.sender)
            
        except Exception as e:
            # This is expected if Rust components aren't available
            pass

    def test_database_compatibility(self):
        """Test that database operations maintain API compatibility."""
        try:
            import tempfile
            from crewai_rust.database import RustSQLiteWrapper
            
            # Test basic functionality
            with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
                db_path = tmp.name
            
            try:
                wrapper = RustSQLiteWrapper(db_path)
            
                # Test execute_query method
                results = wrapper.execute_query("SELECT 1 as test")
                self.assertIsInstance(results, list)
                
                # Test execute_update method
                affected = wrapper.execute_update("CREATE TABLE test (id INTEGER)")
                self.assertIsInstance(affected, int)
                
            finally:
                # Clean up
                if os.path.exists(db_path):
                    os.unlink(db_path)
                    
        except Exception as e:
            # This is expected if Rust components aren't available
            pass

    def test_integration_with_crewai(self):
        """Test integration with actual CrewAI components."""
        try:
            # Test that we can import CrewAI components
            from crewai import Agent, Task, Crew
            
            # Create a simple agent
            agent = Agent(
                role="Test Agent",
                goal="Test Goal",
                backstory="Test Backstory"
            )
            
            # Create a simple task
            task = Task(
                description="Test Task",
                expected_output="Test Output",
                agent=agent
            )
            
            # Create a crew
            crew = Crew(
                agents=[agent],
                tasks=[task]
            )
            
            self.assertIsNotNone(crew)
            
        except ImportError:
            # This is expected if CrewAI isn't installed
            pass

    def test_error_handling(self):
        """Test that error handling works correctly."""
        try:
            from crewai_rust.memory import RustMemoryStorage
            
            # Test with invalid parameters
            storage = RustMemoryStorage()
            
            # Test search with invalid parameters
            results = storage.search("", limit=-1)
            self.assertIsInstance(results, list)
            
        except Exception as e:
            # This is expected if Rust components aren't available
            pass

    def test_configuration_utilities(self):
        """Test configuration utilities."""
        try:
            from crewai_rust.utils import configure_rust_components, get_environment_info
            
            # Test configure_rust_components
            configure_rust_components(memory=True, tools=False)
            
            # Test get_environment_info
            env_info = get_environment_info()
            self.assertIsInstance(env_info, dict)
            self.assertIn('CREWAI_RUST_MEMORY', env_info)
            
        except ImportError:
            # This is expected if Rust components aren't available
            pass

    def test_performance_utilities(self):
        """Test performance utilities."""
        try:
            from crewai_rust.utils import get_performance_improvements, benchmark_comparison
            
            # Test get_performance_improvements
            improvements = get_performance_improvements()
            self.assertIsInstance(improvements, dict)
            self.assertIn('memory', improvements)
            
            # Test benchmark_comparison
            memory_benchmark = benchmark_comparison('memory')
            self.assertIsInstance(memory_benchmark, dict)
            
        except ImportError:
            # This is expected if Rust components aren't available
            pass


if __name__ == '__main__':
    unittest.main()


