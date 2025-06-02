"""
Unit tests for core data structures and constants.
"""
import sys
import os

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import pytest
import tasqsym.core.common.constants as tss_constants
import tasqsym.core.common.structs as tss_structs


class TestStatusFlags:
    """Test StatusFlags enum."""
    
    def test_status_flags_exist(self):
        """Test that all expected status flags exist."""
        assert hasattr(tss_constants.StatusFlags, 'SUCCESS')
        assert hasattr(tss_constants.StatusFlags, 'FAILED')
        assert hasattr(tss_constants.StatusFlags, 'ABORTED')
        
    def test_status_flags_values(self):
        """Test status flag values."""
        assert tss_constants.StatusFlags.SUCCESS.value == 1
        assert tss_constants.StatusFlags.FAILED.value == -1


class TestStatusReason:
    """Test StatusReason enum."""
    
    def test_status_reason_exist(self):
        """Test that status reasons exist."""
        assert hasattr(tss_constants.StatusReason, 'NONE')
        assert hasattr(tss_constants.StatusReason, 'SUCCESSFUL_TERMINATION')
        assert hasattr(tss_constants.StatusReason, 'CONNECTION_ERROR')


class TestStatus:
    """Test Status class functionality."""
    
    def test_status_creation_success(self):
        """Test creating a success status."""
        status = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
        assert status.status == tss_constants.StatusFlags.SUCCESS
        assert status.reason == tss_constants.StatusReason.NONE
        assert status.message == ""
        
    def test_status_creation_with_message(self):
        """Test creating a status with message."""
        message = "Test error message"
        status = tss_structs.Status(
            tss_constants.StatusFlags.FAILED, 
            tss_constants.StatusReason.PROCESS_FAILURE,
            message
        )
        assert status.status == tss_constants.StatusFlags.FAILED
        assert status.reason == tss_constants.StatusReason.PROCESS_FAILURE
        assert status.message == message
        
    def test_status_creation_minimal(self):
        """Test creating status with minimal parameters."""
        status = tss_structs.Status(tss_constants.StatusFlags.FAILED, message="Failed")
        assert status.status == tss_constants.StatusFlags.FAILED
        assert status.reason == tss_constants.StatusReason.NONE
        assert status.message == "Failed"


class TestPoint:
    """Test Point named tuple."""
    
    def test_point_creation(self):
        """Test creating a Point."""
        point = tss_structs.Point(1.0, 2.0, 3.0)
        assert point.x == 1.0
        assert point.y == 2.0
        assert point.z == 3.0
        
    def test_point_immutable(self):
        """Test that Point is immutable."""
        point = tss_structs.Point(1.0, 2.0, 3.0)
        with pytest.raises(AttributeError):
            point.x = 5.0


class TestQuaternion:
    """Test Quaternion named tuple."""
    
    def test_quaternion_creation(self):
        """Test creating a Quaternion."""
        quat = tss_structs.Quaternion(0.0, 0.0, 0.0, 1.0)
        assert quat.x == 0.0
        assert quat.y == 0.0
        assert quat.z == 0.0
        assert quat.w == 1.0


class TestPose:
    """Test Pose named tuple."""
    
    def test_pose_creation_default(self):
        """Test creating a Pose with defaults."""
        pose = tss_structs.Pose()
        assert isinstance(pose.position, tss_structs.Point)
        assert isinstance(pose.orientation, tss_structs.Quaternion)
        
    def test_pose_creation_with_values(self):
        """Test creating a Pose with specific values."""
        position = tss_structs.Point(1.0, 2.0, 3.0)
        orientation = tss_structs.Quaternion(0.0, 0.0, 0.0, 1.0)
        pose = tss_structs.Pose(position, orientation)
        assert pose.position == position
        assert pose.orientation == orientation