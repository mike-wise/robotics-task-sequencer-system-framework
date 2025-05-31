# Test Suite for Robotics Task-sequencer System Framework

This directory contains a comprehensive test suite for the Robotics Task-sequencer System Framework using pytest.

## Test Structure

- `test_core_structs.py` - Unit tests for core data structures (Status, Point, Quaternion, Pose, etc.)
- `test_config_loader.py` - Unit tests for configuration loading functionality
- `test_integration.py` - Integration tests for main components working together
- `test_error_handling.py` - Tests for error scenarios and edge cases

## Running Tests

To run all tests:
```bash
pytest tests/
```

To run tests with verbose output:
```bash
pytest tests/ -v
```

To run a specific test file:
```bash
pytest tests/test_core_structs.py -v
```

To run a specific test:
```bash
pytest tests/test_core_structs.py::TestStatus::test_status_creation_success -v
```

## Test Coverage

The test suite covers:

### Core Components
- ✅ Status flags and error handling
- ✅ Core data structures (Point, Quaternion, Pose, etc.)
- ✅ ConfigLoader functionality
- ✅ EngineInterface initialization
- ✅ SkillInterface management
- ✅ Blackboard functionality

### Integration Testing
- ✅ Loading sample configuration files
- ✅ Parsing sample behavior tree files
- ✅ Component initialization workflows
- ✅ Error scenarios and validation

### Sample Data Testing
- ✅ Real configuration files from `tasqsym_samples/`
- ✅ Behavior tree structure validation
- ✅ Expected node types and sequences

## Dependencies

The test suite requires:
- pytest >= 8.2
- pytest-asyncio >= 1.0.0

These are included in the main `requirements.txt` file.

## Test Philosophy

These tests focus on:
1. **Unit testing** of core components
2. **Integration testing** of main workflows described in the README
3. **Error handling** for invalid inputs and edge cases
4. **Validation** of sample files and expected behavior

The tests use mocking to avoid dependencies on actual robot hardware or external services while still validating the core logic and data flow.