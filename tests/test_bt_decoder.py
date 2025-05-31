# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# --------------------------------------------------------------------------------------------

"""Tests for tasqsym.core.bt_decoder module."""

import pytest
import sys
import os
from unittest.mock import Mock, AsyncMock

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import tasqsym.core.bt_decoder as bt_decoder
import tasqsym.core.common.structs as tss_structs
import tasqsym.core.common.constants as tss_constants
import tasqsym.core.interface.blackboard as blackboard
import tasqsym.core.interface.envg_interface as envg_interface
import tasqsym.core.interface.skill_interface as skill_interface


class TestTaskSequenceDecoder:
    """Test TaskSequenceDecoder functionality."""
    
    def test_task_sequence_decoder_creation(self):
        """Test creating a TaskSequenceDecoder instance."""
        decoder = bt_decoder.TaskSequenceDecoder()
        
        assert decoder.log_last_executed_node_name == ""
        assert decoder.log_last_executed_node_id == []
        assert decoder.network_client is None
        
    def test_task_sequence_decoder_with_network_client(self):
        """Test creating a TaskSequenceDecoder with network client."""
        mock_client = Mock()
        decoder = bt_decoder.TaskSequenceDecoder(mock_client)
        
        assert decoder.network_client == mock_client
        
    @pytest.mark.asyncio
    async def test_run_tree_basic_structure(self):
        """Test runTree with a basic behavior tree structure."""
        decoder = bt_decoder.TaskSequenceDecoder()
        
        # Create minimal behavior tree
        bt = {
            "root": {
                "BehaviorTree": {
                    "Tree": []  # Empty tree
                }
            }
        }
        
        # Create mock interfaces
        board = blackboard.Blackboard()
        rsi = Mock(spec=skill_interface.SkillInterface)
        rsi.cleanup = Mock()
        envg = Mock(spec=envg_interface.EngineInterface)
        
        # Mock runSequence to return success
        decoder.runSequence = AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        
        result = await decoder.runTree(bt, board, rsi, envg)
        
        assert result.status == tss_constants.StatusFlags.SUCCESS
        rsi.cleanup.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_run_tree_with_start_from_node(self):
        """Test runTree with start_from_node_id parameter."""
        decoder = bt_decoder.TaskSequenceDecoder()
        
        bt = {
            "root": {
                "BehaviorTree": {
                    "Tree": []
                }
            }
        }
        
        board = blackboard.Blackboard()
        rsi = Mock(spec=skill_interface.SkillInterface)
        rsi.cleanup = Mock()
        envg = Mock(spec=envg_interface.EngineInterface)
        
        decoder.runSequence = AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        
        start_from_node_id = [1, 2]
        escape_at_node_id = [3, 4]
        
        result = await decoder.runTree(bt, board, rsi, envg, start_from_node_id, escape_at_node_id)
        
        assert decoder.start_from_node_id == start_from_node_id
        assert decoder.escape_at_node_id == escape_at_node_id
        assert result.status == tss_constants.StatusFlags.SUCCESS
        
    @pytest.mark.asyncio
    async def test_parse_control_sequence(self):
        """Test parseControl with a Sequence node."""
        decoder = bt_decoder.TaskSequenceDecoder()
        
        sequence_node = {
            "Sequence": {
                "@name": "test_sequence",
                "child": []
            }
        }
        
        board = blackboard.Blackboard()
        rsi = Mock(spec=skill_interface.SkillInterface)
        envg = Mock(spec=envg_interface.EngineInterface)
        
        # Mock runSequence to return success
        decoder.runSequence = AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        
        result = await decoder.parseControl(sequence_node, board, rsi, envg, [0])
        
        assert result.status == tss_constants.StatusFlags.SUCCESS
        
    @pytest.mark.asyncio
    async def test_parse_control_fallback(self):
        """Test parseControl with a Fallback node."""
        decoder = bt_decoder.TaskSequenceDecoder()
        
        fallback_node = {
            "Fallback": {
                "@name": "test_fallback",
                "child": []
            }
        }
        
        board = blackboard.Blackboard()
        rsi = Mock(spec=skill_interface.SkillInterface)
        envg = Mock(spec=envg_interface.EngineInterface)
        
        # Mock runFallback to return success
        decoder.runFallback = AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        
        result = await decoder.parseControl(fallback_node, board, rsi, envg, [0])
        
        assert result.status == tss_constants.StatusFlags.SUCCESS
        
    @pytest.mark.asyncio
    async def test_parse_control_parallel(self):
        """Test parseControl with a Parallel node."""
        decoder = bt_decoder.TaskSequenceDecoder()
        
        parallel_node = {
            "Parallel": {
                "@name": "test_parallel",
                "@success_count": "1",
                "@failure_count": "-1",
                "child": []
            }
        }
        
        board = blackboard.Blackboard()
        rsi = Mock(spec=skill_interface.SkillInterface)
        envg = Mock(spec=envg_interface.EngineInterface)
        
        # Mock runParallel to return success (but it doesn't exist, so expect UNEXPECTED)
        result = await decoder.parseControl(parallel_node, board, rsi, envg, [0])
        
        # parseControl will return UNEXPECTED for unsupported node types
        assert result.status == tss_constants.StatusFlags.UNEXPECTED
        
    @pytest.mark.asyncio
    async def test_parse_control_unknown_node(self):
        """Test parseControl with an unknown node type."""
        decoder = bt_decoder.TaskSequenceDecoder()
        
        unknown_node = {
            "UnknownNode": {
                "@name": "test_unknown"
            }
        }
        
        board = blackboard.Blackboard()
        rsi = Mock(spec=skill_interface.SkillInterface)
        envg = Mock(spec=envg_interface.EngineInterface)
        
        result = await decoder.parseControl(unknown_node, board, rsi, envg, [0])
        
        # Should return failure for unknown node types
        assert result.status == tss_constants.StatusFlags.UNEXPECTED
        
    def test_logging_attributes(self):
        """Test that logging attributes are properly initialized and can be modified."""
        decoder = bt_decoder.TaskSequenceDecoder()
        
        # Initial state
        assert decoder.log_last_executed_node_name == ""
        assert decoder.log_last_executed_node_id == []
        
        # Set logging attributes
        decoder.log_last_executed_node_name = "test_node"
        decoder.log_last_executed_node_id = [1, 2, 3]
        
        assert decoder.log_last_executed_node_name == "test_node"
        assert decoder.log_last_executed_node_id == [1, 2, 3]
        
    @pytest.mark.asyncio
    async def test_run_tree_error_handling(self):
        """Test runTree error handling when runSequence fails."""
        decoder = bt_decoder.TaskSequenceDecoder()
        
        bt = {
            "root": {
                "BehaviorTree": {
                    "Tree": []
                }
            }
        }
        
        board = blackboard.Blackboard()
        rsi = Mock(spec=skill_interface.SkillInterface)
        rsi.cleanup = Mock()
        envg = Mock(spec=envg_interface.EngineInterface)
        
        # Mock runSequence to return failure
        decoder.runSequence = AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.FAILED, "Test failure"))

        result = await decoder.runTree(bt, board, rsi, envg)

        assert result.status == tss_constants.StatusFlags.FAILED
        assert "Test failure" in result.message or result.message == "Test failure"
        rsi.cleanup.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_parse_control_with_name_attribute(self):
        """Test parseControl correctly handles nodes with @name attributes."""
        decoder = bt_decoder.TaskSequenceDecoder()
        
        named_sequence = {
            "Sequence": {
                "@name": "named_test_sequence",
                "child": []
            }
        }
        
        board = blackboard.Blackboard()
        rsi = Mock(spec=skill_interface.SkillInterface)
        envg = Mock(spec=envg_interface.EngineInterface)
        
        decoder.runSequence = AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        
        result = await decoder.parseControl(named_sequence, board, rsi, envg, [0])
        
        assert result.status == tss_constants.StatusFlags.SUCCESS
        # Verify the runSequence was called with the correct child nodes
        decoder.runSequence.assert_called_once()
        
    @pytest.mark.asyncio 
    async def test_run_tree_resets_logging(self):
        """Test that runTree resets logging attributes."""
        decoder = bt_decoder.TaskSequenceDecoder()
        
        # Set some initial logging state
        decoder.log_last_executed_node_name = "previous_node"
        decoder.log_last_executed_node_id = [5, 6, 7]
        
        bt = {
            "root": {
                "BehaviorTree": {
                    "Tree": []
                }
            }
        }
        
        board = blackboard.Blackboard()
        rsi = Mock(spec=skill_interface.SkillInterface)
        rsi.cleanup = Mock()
        envg = Mock(spec=envg_interface.EngineInterface)
        
        decoder.runSequence = AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        
        await decoder.runTree(bt, board, rsi, envg)
        
        # Logging should be reset
        assert decoder.log_last_executed_node_name == ""
        assert decoder.log_last_executed_node_id == []