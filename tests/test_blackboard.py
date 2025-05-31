# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# --------------------------------------------------------------------------------------------

"""Tests for tasqsym.core.interface.blackboard module."""

import pytest
import sys
import os

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import tasqsym.core.interface.blackboard as blackboard


class TestBlackboard:
    """Test Blackboard functionality."""
    
    def test_blackboard_creation(self):
        """Test creating a new blackboard instance."""
        board = blackboard.Blackboard()
        
        assert board.board == {}
        
    def test_set_and_get_variable(self):
        """Test setting and getting variables on the blackboard."""
        board = blackboard.Blackboard()
        
        board.setBoardVariable("test_key", "test_value")
        result = board.getBoardVariable("test_key")
        
        assert result == "test_value"
        
    def test_set_variable_different_types(self):
        """Test setting variables of different types."""
        board = blackboard.Blackboard()
        
        # String
        board.setBoardVariable("string_key", "hello")
        assert board.getBoardVariable("string_key") == "hello"
        
        # Integer
        board.setBoardVariable("int_key", 42)
        assert board.getBoardVariable("int_key") == 42
        
        # Float
        board.setBoardVariable("float_key", 3.14)
        assert board.getBoardVariable("float_key") == 3.14
        
        # List
        board.setBoardVariable("list_key", [1, 2, 3])
        assert board.getBoardVariable("list_key") == [1, 2, 3]
        
        # Dictionary
        board.setBoardVariable("dict_key", {"a": 1, "b": 2})
        assert board.getBoardVariable("dict_key") == {"a": 1, "b": 2}
        
        # Boolean
        board.setBoardVariable("bool_key", True)
        assert board.getBoardVariable("bool_key") is True
        
        # None
        board.setBoardVariable("none_key", None)
        assert board.getBoardVariable("none_key") is None
        
    def test_get_nonexistent_variable(self):
        """Test getting a variable that doesn't exist."""
        board = blackboard.Blackboard()
        
        # Capture stdout to check the print message
        import io
        import contextlib
        
        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            result = board.getBoardVariable("nonexistent_key")
        
        assert result is None
        output = captured_output.getvalue()
        assert "Blackborad: get on unknown variable nonexistent_key" in output
        
    def test_set_empty_string_key(self):
        """Test setting a variable with empty string key."""
        board = blackboard.Blackboard()
        
        import io
        import contextlib
        
        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            board.setBoardVariable("", "some_value")
        
        # Should not set the variable
        assert "" not in board.board
        output = captured_output.getvalue()
        assert "Blackboard: ignoring key as empty string" in output
        
    def test_overwrite_variable(self):
        """Test overwriting an existing variable."""
        board = blackboard.Blackboard()
        
        board.setBoardVariable("key", "original_value")
        assert board.getBoardVariable("key") == "original_value"
        
        board.setBoardVariable("key", "new_value")
        assert board.getBoardVariable("key") == "new_value"
        
    def test_clear_board(self):
        """Test clearing the blackboard."""
        board = blackboard.Blackboard()
        
        # Set some variables
        board.setBoardVariable("key1", "value1")
        board.setBoardVariable("key2", "value2")
        board.setBoardVariable("key3", "value3")
        
        assert len(board.board) == 3
        
        # Clear the board
        board.clearBoard()
        
        assert board.board == {}
        assert len(board.board) == 0
        
    def test_clear_board_after_clear(self):
        """Test accessing variables after clearing the board."""
        board = blackboard.Blackboard()
        
        board.setBoardVariable("key", "value")
        assert board.getBoardVariable("key") == "value"
        
        board.clearBoard()
        
        import io
        import contextlib
        
        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            result = board.getBoardVariable("key")
        
        assert result is None
        output = captured_output.getvalue()
        assert "Blackborad: get on unknown variable key" in output
        
    def test_multiple_blackboards(self):
        """Test that multiple blackboard instances are independent."""
        board1 = blackboard.Blackboard()
        board2 = blackboard.Blackboard()
        
        board1.setBoardVariable("key", "value1")
        board2.setBoardVariable("key", "value2")
        
        assert board1.getBoardVariable("key") == "value1"
        assert board2.getBoardVariable("key") == "value2"
        
        # Clear one board
        board1.clearBoard()
        
        assert len(board1.board) == 0
        assert len(board2.board) == 1
        assert board2.getBoardVariable("key") == "value2"
        
    def test_complex_nested_data(self):
        """Test storing complex nested data structures."""
        board = blackboard.Blackboard()
        
        complex_data = {
            "robots": [
                {"name": "robot1", "position": {"x": 1.0, "y": 2.0, "z": 3.0}},
                {"name": "robot2", "position": {"x": 4.0, "y": 5.0, "z": 6.0}}
            ],
            "tasks": {
                "current": "navigation",
                "queue": ["pick", "place", "return"]
            },
            "metadata": {
                "timestamp": 1234567890,
                "session_id": "abc123"
            }
        }
        
        board.setBoardVariable("world_state", complex_data)
        result = board.getBoardVariable("world_state")
        
        assert result == complex_data
        assert result["robots"][0]["name"] == "robot1"
        assert result["robots"][1]["position"]["z"] == 6.0
        assert result["tasks"]["queue"][2] == "return"
        
    def test_variable_keys_case_sensitive(self):
        """Test that variable keys are case sensitive."""
        board = blackboard.Blackboard()
        
        board.setBoardVariable("Key", "value1")
        board.setBoardVariable("key", "value2")
        board.setBoardVariable("KEY", "value3")
        
        assert board.getBoardVariable("Key") == "value1"
        assert board.getBoardVariable("key") == "value2"
        assert board.getBoardVariable("KEY") == "value3"
        assert len(board.board) == 3
        
    def test_variable_keys_with_spaces(self):
        """Test variable keys with spaces and special characters."""
        board = blackboard.Blackboard()
        
        board.setBoardVariable("key with spaces", "value1")
        board.setBoardVariable("key_with_underscores", "value2")
        board.setBoardVariable("key-with-dashes", "value3")
        board.setBoardVariable("key.with.dots", "value4")
        
        assert board.getBoardVariable("key with spaces") == "value1"
        assert board.getBoardVariable("key_with_underscores") == "value2"
        assert board.getBoardVariable("key-with-dashes") == "value3"
        assert board.getBoardVariable("key.with.dots") == "value4"