# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CrewAI Rust is a **drop-in performance enhancement layer** that provides high-performance Rust implementations for critical CrewAI components. The key innovation is a sophisticated **monkey patching/shim system** that transparently replaces Python components with Rust equivalents while maintaining 100% API compatibility.

## Essential Commands

### Development Setup
```bash
# Install build dependencies
pip install maturin

# Build Rust extension in development mode (fastest iteration)
maturin develop

# Force rebuild after Rust changes
maturin develop --force
```

### Testing
```bash
# Run all tests
python -m pytest

# Fast tests only (exclude slow/integration/performance)
./scripts/run_tests.sh fast

# Specific test categories
./scripts/run_tests.sh unit
./scripts/run_tests.sh integration
./scripts/run_tests.sh performance

# Single test file
python -m pytest tests/test_memory.py -v

# Single test function
python -m pytest tests/test_memory.py::test_rust_memory_storage -v

# Tests with coverage
./scripts/run_tests.sh coverage
```

### Build and Distribution
```bash
# Release build (optimized)
maturin build --release

# Build for specific Python version
maturin develop --python python3.10

# Check package structure
python -c "import crewai_rust; print(crewai_rust.__file__)"
```

## Core Architecture

### Monkey Patching System (`crewai_rust/shim.py`)

The **heart of the system** - enables zero-code integration by replacing CrewAI classes at import time:

```python
# Activation triggers global module replacement
import crewai_rust.shim  # Auto-activates patching

# This import now returns RustMemoryStorage instead of RAGStorage
from crewai.memory import RAGStorage
```

**Key mechanisms:**
- `sys.modules` manipulation for import interception
- Class replacement via `setattr(module, class_name, rust_class)`
- Backup system in `_original_classes` for restoration
- Environment variable control (`CREWAI_RUST_*=true/false/auto`)

### Dual Implementation Pattern

Each component has both Rust and Python implementations with automatic fallback:

- **Rust Core** (`src/lib.rs`): High-performance native implementations
- **Python Wrappers** (`crewai_rust/*.py`): Compatibility layer with fallback logic
- **Auto-Detection**: `use_rust=None` automatically chooses best available implementation

### Component Replacement Targets

```python
# Memory components (10-20x faster)
'crewai.memory.storage.rag_storage' → RustMemoryStorage
'crewai.memory.short_term.short_term_memory' → RustMemoryStorage
'crewai.memory.long_term.long_term_memory' → RustMemoryStorage

# Tool execution (2-5x faster)
'crewai.tools.structured_tool' → RustToolExecutor

# Database operations (3-5x faster)
'crewai.memory.storage.ltm_sqlite_storage' → RustSQLiteWrapper
```

## Development Patterns

### Adding New Rust Components

1. **Rust Implementation** (`src/lib.rs`):
   ```rust
   #[pyclass]
   pub struct RustNewComponent {
       // Implementation
   }

   #[pymethods]
   impl RustNewComponent {
       #[new]
       pub fn new() -> Self { /* */ }

       pub fn method(&self) -> PyResult<String> { /* */ }
   }
   ```

2. **Python Wrapper** (`crewai_rust/new_component.py`):
   ```python
   class RustNewComponent:
       def __init__(self, use_rust=None):
           self.use_rust = self._detect_rust_availability() if use_rust is None else use_rust
           if self.use_rust:
               self._rust_impl = _core.RustNewComponent()
   ```

3. **Shim Registration** (`crewai_rust/shim.py`):
   ```python
   new_patches = [
       ('crewai.module.path', 'OriginalClass', RustNewComponent),
   ]
   ```

### Error Handling Pattern

All components follow this fallback pattern:
```python
try:
    result = self._rust_impl.method(args)
except Exception as e:
    if self._fallback_enabled:
        print(f"Warning: Rust failed, using Python: {e}")
        self.use_rust = False
        result = self._python_fallback(args)
    else:
        raise
```

### Testing New Components

1. **Unit Tests**: Test Rust implementation directly
2. **Integration Tests**: Test through CrewAI workflows
3. **Compatibility Tests**: Verify identical behavior to Python
4. **Performance Tests**: Benchmark speed improvements
5. **Fallback Tests**: Ensure graceful degradation

## Build System Architecture

### Maturin Configuration (`pyproject.toml`)
- **Build Backend**: `maturin` for Rust-Python integration
- **Module Name**: `crewai_rust._core` (Rust extension)
- **Target**: `src/lib.rs` compiled as `cdylib`

### Development vs Production
- **Development**: `maturin develop` for fast iteration
- **Production**: `maturin build --release` for optimized binaries
- **Distribution**: Wheels built for multiple platforms

## Key Implementation Details

### Memory Safety
- **Rust Side**: Memory-safe by design with ownership system
- **Python Bridge**: `Arc<Mutex<T>>` for thread-safe shared state
- **Error Handling**: Rust `Result<T, E>` converted to Python exceptions

### Performance Optimizations
- **Memory Operations**: SIMD-accelerated vector operations
- **Tool Execution**: Zero-cost abstractions, stack safety
- **Task Execution**: Tokio async runtime with work-stealing
- **Serialization**: Zero-copy operations with serde
- **Database**: Connection pooling with r2d2

### Configuration System
Environment variables provide fine-grained control:
```bash
CREWAI_RUST_ACCELERATION=1    # Global enable/disable
CREWAI_RUST_MEMORY=true       # Per-component control
CREWAI_RUST_TOOLS=false       # Selective disabling
```

## Testing Strategy

### Test Organization
- `test_memory.py`: Memory component tests
- `test_tools.py`: Tool execution tests
- `test_tasks.py`: Task execution tests
- `test_integration.py`: End-to-end CrewAI workflows
- `test_shim.py`: Monkey patching system tests

### Performance Testing
Use markers to control test execution:
```python
@pytest.mark.performance
def test_memory_benchmark():
    # Benchmark tests

@pytest.mark.slow
def test_large_dataset():
    # Resource-intensive tests
```

## Critical Files for Understanding

1. **`crewai_rust/shim.py`**: The core monkey patching system
2. **`src/lib.rs`**: All Rust implementations and PyO3 bindings
3. **`crewai_rust/__init__.py`**: Package initialization and fallback logic
4. **`pyproject.toml`**: Build configuration and project metadata
5. **`tests/test_integration.py`**: End-to-end usage patterns

## Performance Expectations

When working with this codebase, expect these performance characteristics:
- **Memory Operations**: 10-20x improvement (SIMD acceleration)
- **Tool Execution**: 2-5x improvement (zero-cost abstractions)
- **Task Execution**: 3-5x improvement (true async concurrency)
- **Serialization**: 5-10x improvement (zero-copy operations)
- **Database Operations**: 3-5x improvement (connection pooling)