"""
Example usage of the CrewAI Rust integration components.

This module demonstrates how to use the various Rust-enhanced
components in real-world scenarios.
"""

import time
import json
from crewai_accelerate import HAS_RUST_IMPLEMENTATION
from crewai_accelerate.memory import AcceleratedMemoryStorage
from crewai_accelerate.tools import AcceleratedToolExecutor
from crewai_accelerate.tasks import AcceleratedTaskExecutor
from crewai_accelerate.serialization import AcceleratedMessage, RustSerializer
from crewai_accelerate.database import AcceleratedSQLiteWrapper
from crewai_accelerate.utils import get_rust_status, get_performance_improvements


def example_memory_usage():
    """Demonstrate memory storage usage."""
    print("=== Memory Storage Example ===")
    
    # Create memory storage
    memory = AcceleratedMemoryStorage()
    print(f"Memory implementation: {memory.implementation}")
    
    # Save some data
    memory.save("Python is a great programming language", {"category": "programming", "sentiment": "positive"})
    memory.save("Rust provides excellent performance", {"category": "programming", "sentiment": "positive"})
    memory.save("Machine learning is transforming industries", {"category": "AI", "sentiment": "neutral"})
    
    # Search for relevant information
    results = memory.search("programming languages", limit=2)
    print(f"Search results for 'programming languages': {len(results)} items")
    for i, result in enumerate(results):
        print(f"  {i+1}. {result['value']} (metadata: {result['metadata']})")
    
    # Get all items
    all_items = memory.get_all()
    print(f"Total items in memory: {len(all_items)}")
    
    print()


def example_tool_execution():
    """Demonstrate tool execution usage."""
    print("=== Tool Execution Example ===")
    
    # Create tool executor
    executor = AcceleratedToolExecutor(max_recursion_depth=5, timeout_seconds=10)
    print(f"Tool executor implementation: {executor.implementation}")
    
    # Execute some tools
    tools_to_execute = [
        ("calculator", {"operation": "add", "a": 5, "b": 3}),
        ("text_processor", {"text": "Hello World", "operation": "uppercase"}),
        ("data_validator", {"data": {"name": "John", "age": 30}, "schema": "person"})
    ]
    
    for tool_name, args in tools_to_execute:
        try:
            result = executor.execute_tool(tool_name, args)
            print(f"Tool '{tool_name}' result: {result}")
        except Exception as e:
            print(f"Tool '{tool_name}' failed: {e}")
    
    print()


def example_task_execution():
    """Demonstrate task execution usage."""
    print("=== Task Execution Example ===")
    
    # Create task executor
    executor = AcceleratedTaskExecutor()
    print(f"Task executor implementation: {executor.implementation}")
    
    # Define some tasks
    tasks = [
        {"name": "data_processing", "description": "Process customer data", "priority": "high"},
        {"name": "report_generation", "description": "Generate monthly report", "priority": "medium"},
        {"name": "backup_creation", "description": "Create system backup", "priority": "low"}
    ]
    
    # Execute tasks concurrently
    print("Executing tasks concurrently...")
    start_time = time.time()
    results = executor.execute_concurrent_tasks(tasks)
    end_time = time.time()
    
    print(f"Completed {len(results)} tasks in {end_time - start_time:.3f} seconds")
    for i, result in enumerate(results):
        print(f"  Task {i+1}: {result}")
    
    # Execute single task with timeout
    print("\nExecuting single task with timeout...")
    try:
        single_result = executor.execute_task_with_timeout(
            {"name": "quick_task", "description": "Quick processing task"}, 
            timeout_seconds=2
        )
        print(f"Single task result: {single_result}")
    except Exception as e:
        print(f"Single task failed: {e}")
    
    print()


def example_serialization():
    """Demonstrate serialization usage."""
    print("=== Serialization Example ===")
    
    # Create some messages
    messages = [
        AcceleratedMessage("msg1", "agent1", "agent2", "Hello from agent1", int(time.time())),
        AcceleratedMessage("msg2", "agent2", "agent1", "Response from agent2", int(time.time()) + 1),
        AcceleratedMessage("msg3", "agent1", "agent3", "Broadcast message", int(time.time()) + 2)
    ]
    
    print(f"Message implementation: {messages[0].implementation}")
    
    # Serialize individual messages
    print("Serializing individual messages:")
    for msg in messages:
        json_str = msg.to_json()
        print(f"  {msg.id}: {json_str[:50]}...")
    
    # Test round-trip serialization
    print("\nTesting round-trip serialization:")
    original_msg = messages[0]
    json_str = original_msg.to_json()
    deserialized_msg = AcceleratedMessage.from_json(json_str)
    
    print(f"Original: {original_msg.sender} -> {original_msg.recipient}: {original_msg.content}")
    print(f"Deserialized: {deserialized_msg.sender} -> {deserialized_msg.recipient}: {deserialized_msg.content}")
    print(f"Round-trip successful: {original_msg.id == deserialized_msg.id}")
    
    # Batch serialization
    print("\nBatch serialization:")
    serializer = RustSerializer()
    
    # Prepare message data
    message_data = [
        {"id": "batch1", "sender": "batch_agent", "recipient": "target", "content": "Batch message 1", "timestamp": int(time.time())},
        {"id": "batch2", "sender": "batch_agent", "recipient": "target", "content": "Batch message 2", "timestamp": int(time.time()) + 1}
    ]
    
    # Serialize batch
    serialized_batch = serializer.serialize_batch(message_data)
    print(f"Serialized {len(serialized_batch)} messages")
    
    # Deserialize batch
    deserialized_batch = serializer.deserialize_batch(serialized_batch)
    print(f"Deserialized {len(deserialized_batch)} messages")
    
    print()


def example_database_operations():
    """Demonstrate database operations."""
    print("=== Database Operations Example ===")
    
    import tempfile
    import os
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # Create database wrapper
        db = AcceleratedSQLiteWrapper(db_path, pool_size=3)
        print(f"Database implementation: {db.implementation}")
        
        # Test basic operations
        print("Testing database operations...")
        
        # Execute a simple query
        results = db.execute_query("SELECT 1 as test_column")
        print(f"Query results: {results}")
        
        # Execute an update
        affected_rows = db.execute_update("CREATE TABLE test_table (id INTEGER, name TEXT)")
        print(f"Update affected {affected_rows} rows")
        
        # Test memory operations
        print("\nTesting memory operations...")
        db.save_memory(
            task_description="Test task",
            metadata={"type": "test", "priority": "high"},
            datetime="2024-01-01 12:00:00",
            score=0.95
        )
        
        # Load memories
        memories = db.load_memories("Test task", latest_n=5)
        if memories:
            print(f"Loaded {len(memories)} memories")
            for memory in memories:
                print(f"  Memory: {memory}")
        else:
            print("No memories found")
        
    finally:
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    print()


def example_performance_comparison():
    """Demonstrate performance comparison."""
    print("=== Performance Comparison Example ===")
    
    # Get performance improvements
    improvements = get_performance_improvements()
    print("Expected performance improvements:")
    for component, info in improvements.items():
        print(f"  {component}: {info['improvement']} - {info['description']}")
    
    # Get current status
    status = get_rust_status()
    print(f"\nCurrent Rust status: {status}")
    
    print()


def main():
    """Run all examples."""
    print("CrewAI Rust Integration Examples")
    print("=" * 40)
    print(f"Rust implementation available: {HAS_RUST_IMPLEMENTATION}")
    print()
    
    try:
        example_memory_usage()
        example_tool_execution()
        example_task_execution()
        example_serialization()
        example_database_operations()
        example_performance_comparison()
        
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


