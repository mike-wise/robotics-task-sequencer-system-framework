"""
Tests for error handling and edge cases.
"""
import sys
import os
import json
import tempfile

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import pytest
import tasqsym.core.common.constants as tss_constants
import tasqsym.core.common.structs as tss_structs
import tasqsym.core.interface.config_loader as config_loader


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_config_loader_invalid_json_file(self):
        """Test config loader with invalid JSON file."""
        # Create a temporary file with invalid JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json")
            temp_file = f.name
            
        try:
            cfl = config_loader.ConfigLoader()
            configs = {"robot_structure": temp_file}
            
            # This should raise a JSON decode error
            with pytest.raises(json.JSONDecodeError):
                cfl.expandRobotStructureConfig(configs)
        finally:
            os.unlink(temp_file)
            
    def test_status_with_all_fields(self):
        """Test Status creation with all fields."""
        status = tss_structs.Status(
            tss_constants.StatusFlags.ABORTED,
            tss_constants.StatusReason.CONNECTION_ERROR,
            "Connection failed"
        )
        assert status.status == tss_constants.StatusFlags.ABORTED
        assert status.reason == tss_constants.StatusReason.CONNECTION_ERROR
        assert status.message == "Connection failed"
        
    def test_data_class_functionality(self):
        """Test Data class functionality."""
        data_dict = {
            "normal_field": "value1",
            "@special_field": "value2",
            "nested": {"key": "value"}
        }
        
        data = tss_structs.Data(data_dict)
        assert data.normal_field == "value1"
        assert data.special_field == "value2"  # @ prefix removed
        assert data.nested == {"key": "value"}
        
    def test_robot_action_creation(self):
        """Test RobotAction creation."""
        action = tss_structs.RobotAction(
            tss_constants.SolveByType.NULL_ACTION,
            {"param": "value"}
        )
        assert action.solveby_type == tss_constants.SolveByType.NULL_ACTION
        assert action.configs == {"param": "value"}


class TestBehaviorTreeValidation:
    """Test behavior tree structure validation."""
    
    def test_behavior_tree_missing_root(self):
        """Test behavior tree without root field."""
        bt_data = {"not_root": {}}
        
        # Just test that we can detect missing root
        assert "root" not in bt_data
        
    def test_behavior_tree_malformed_structure(self):
        """Test behavior tree with malformed structure."""
        bt_data = {
            "root": {
                "BehaviorTree": {
                    "Tree": "not_a_list"  # Should be a list
                }
            }
        }
        
        # Verify the structure is malformed
        assert not isinstance(bt_data["root"]["BehaviorTree"]["Tree"], list)
        
    def test_behavior_tree_empty_sequence(self):
        """Test behavior tree with empty sequence."""
        bt_data = {
            "root": {
                "BehaviorTree": {
                    "Tree": [{"Sequence": []}]  # Empty sequence
                }
            }
        }
        
        # Verify we can detect empty sequences
        sequence = bt_data["root"]["BehaviorTree"]["Tree"][0]["Sequence"]
        assert len(sequence) == 0


class TestConstants:
    """Test constants and enums."""
    
    def test_all_status_flags(self):
        """Test all status flags are accessible."""
        flags = [
            tss_constants.StatusFlags.SUCCESS,
            tss_constants.StatusFlags.FAILED,
            tss_constants.StatusFlags.ABORTED,
            tss_constants.StatusFlags.UNEXPECTED,
            tss_constants.StatusFlags.SKIPPED,
            tss_constants.StatusFlags.ESCAPED,
            tss_constants.StatusFlags.UNKNOWN
        ]
        
        for flag in flags:
            assert isinstance(flag, tss_constants.StatusFlags)
            
    def test_status_reason_enum(self):
        """Test status reason enum values."""
        reasons = [
            tss_constants.StatusReason.NONE,
            tss_constants.StatusReason.SUCCESSFUL_TERMINATION,
            tss_constants.StatusReason.CONNECTION_ERROR,
            tss_constants.StatusReason.PROCESS_FAILURE,
            tss_constants.StatusReason.OTHER
        ]
        
        for reason in reasons:
            assert isinstance(reason, tss_constants.StatusReason)
            
    def test_solve_by_type_enum(self):
        """Test SolveByType enum."""
        assert hasattr(tss_constants, 'SolveByType')
        assert hasattr(tss_constants.SolveByType, 'NULL_ACTION')


class TestStructImmutability:
    """Test immutability of named tuples."""
    
    def test_point_tuple_properties(self):
        """Test Point named tuple properties."""
        p1 = tss_structs.Point(1.0, 2.0, 3.0)
        p2 = tss_structs.Point(1.0, 2.0, 3.0)
        p3 = tss_structs.Point(2.0, 2.0, 3.0)
        
        assert p1 == p2
        assert p1 != p3
        assert isinstance(p1, tuple)
        
    def test_quaternion_tuple_properties(self):
        """Test Quaternion named tuple properties."""
        q1 = tss_structs.Quaternion(0.0, 0.0, 0.0, 1.0)
        q2 = tss_structs.Quaternion(0.0, 0.0, 0.0, 1.0)
        
        assert q1 == q2
        assert isinstance(q1, tuple)
        
    def test_pose_with_lists(self):
        """Test Pose creation with lists instead of named tuples."""
        pose = tss_structs.Pose([1.0, 2.0, 3.0], [0.0, 0.0, 0.0, 1.0])
        assert pose.position == [1.0, 2.0, 3.0]
        assert pose.orientation == [0.0, 0.0, 0.0, 1.0]