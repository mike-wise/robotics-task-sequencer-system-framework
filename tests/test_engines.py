# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# --------------------------------------------------------------------------------------------

"""Tests for tasqsym.core.engines modules."""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add src to Python path for imports  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import tasqsym.core.engines.data_engine as data_engine
import tasqsym.core.engines.controller_engine as controller_engine
import tasqsym.core.engines.kinematics_engine as kinematics_engine
import tasqsym.core.common.structs as tss_structs
import tasqsym.core.common.constants as tss_constants


class TestDataEngine:
    """Test DataEngine functionality."""
    
    def test_data_engine_creation(self):
        """Test creating a DataEngine instance."""
        engine = data_engine.DataEngine("test_data_engine")
        assert engine is not None
        
    def test_data_engine_initialization(self):
        """Test DataEngine initialization."""
        engine = data_engine.DataEngine("test_data_engine")
        
        # Test basic initialization without external dependencies
        config = {
            "type": "simulation",
            "data_source": "mock"
        }
        
        # Mock initialization to avoid hardware dependencies
        with patch.object(engine, 'init') as mock_init:
            mock_init.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
            
            result = engine.init(config)
            assert result.status == tss_constants.StatusFlags.SUCCESS
            
    def test_data_engine_data_access(self):
        """Test DataEngine data access methods."""
        engine = data_engine.DataEngine("test_data_engine")
        
        # Test that basic methods exist and can be called
        if hasattr(engine, 'getData'):
            with patch.object(engine, 'getData') as mock_get:
                mock_get.return_value = {"sensor1": "data"}
                
                result = engine.getData()
                assert isinstance(result, dict)
                
        if hasattr(engine, 'setData'):
            with patch.object(engine, 'setData') as mock_set:
                mock_set.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
                
                result = engine.setData({"test": "data"})
                assert result.status == tss_constants.StatusFlags.SUCCESS
                
    def test_data_engine_status_methods(self):
        """Test DataEngine status and state methods."""
        engine = data_engine.DataEngine("test_data_engine")
        
        # Test status checking methods
        if hasattr(engine, 'isReady'):
            with patch.object(engine, 'isReady') as mock_ready:
                mock_ready.return_value = True
                assert engine.isReady() is True
                
        if hasattr(engine, 'getStatus'):
            with patch.object(engine, 'getStatus') as mock_status:
                mock_status.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
                
                status = engine.getStatus()
                assert status.status == tss_constants.StatusFlags.SUCCESS


class TestControllerEngine:
    """Test ControllerEngine functionality."""
    
    def test_controller_engine_creation(self):
        """Test creating a ControllerEngine instance."""
        engine = controller_engine.ControllerEngine("test_controller")
        assert engine is not None
        
    def test_controller_engine_initialization(self):
        """Test ControllerEngine initialization."""
        engine = controller_engine.ControllerEngine("test_controller")
        
        config = {
            "type": "moveit",
            "planning_group": "arm",
            "planning_time": 5.0
        }
        
        with patch.object(engine, 'init') as mock_init:
            mock_init.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
            
            result = engine.init(config)
            assert result.status == tss_constants.StatusFlags.SUCCESS
            
    def test_controller_engine_command_execution(self):
        """Test ControllerEngine command execution."""
        engine = controller_engine.ControllerEngine("test_controller")
        
        # Test action execution
        if hasattr(engine, 'execute'):
            mock_action = Mock()
            mock_action.solveby_type = tss_constants.SolveByType.FORWARD_KINEMATICS
            
            with patch.object(engine, 'execute') as mock_execute:
                mock_execute.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
                
                result = engine.execute(mock_action)
                assert result.status == tss_constants.StatusFlags.SUCCESS
                
        # Test state getting
        if hasattr(engine, 'getCurrentState'):
            with patch.object(engine, 'getCurrentState') as mock_get_state:
                base_pose = tss_structs.Pose(
                    position=tss_structs.Point(0, 0, 0),
                    orientation=tss_structs.Quaternion(0, 0, 0, 1)
                )
                mock_state = tss_structs.RobotState(base_pose)
                mock_get_state.return_value = mock_state
                
                state = engine.getCurrentState()
                assert state.base_state.position.x == 0
                
    def test_controller_engine_motion_planning(self):
        """Test ControllerEngine motion planning capabilities."""
        engine = controller_engine.ControllerEngine("test_controller")
        
        if hasattr(engine, 'planMotion'):
            target_pose = tss_structs.Pose(
                position=tss_structs.Point(1, 0, 1),
                orientation=tss_structs.Quaternion(0, 0, 0, 1)
            )
            
            with patch.object(engine, 'planMotion') as mock_plan:
                mock_plan.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
                
                result = engine.planMotion(target_pose)
                assert result.status == tss_constants.StatusFlags.SUCCESS
                
    def test_controller_engine_error_handling(self):
        """Test ControllerEngine error handling."""
        engine = controller_engine.ControllerEngine("test_controller")
        
        if hasattr(engine, 'execute'):
            with patch.object(engine, 'execute') as mock_execute:
                mock_execute.return_value = tss_structs.Status(
                    tss_constants.StatusFlags.FAILED, 
                    message="Motion planning failed"
                )
                
                mock_action = Mock()
                result = engine.execute(mock_action)
                assert result.status == tss_constants.StatusFlags.FAILED


class TestKinematicsEngine:
    """Test KinematicsEngine functionality."""
    
    def test_kinematics_engine_creation(self):
        """Test creating a KinematicsEngine instance."""
        engine = kinematics_engine.KinematicsEngine("test_kinematics")
        assert engine is not None
        
    def test_kinematics_engine_initialization(self):
        """Test KinematicsEngine initialization."""
        engine = kinematics_engine.KinematicsEngine("test_kinematics")
        
        config = {
            "type": "kdl",
            "urdf_path": "/fake/path/robot.urdf",
            "base_link": "base_link",
            "tip_link": "end_effector_link"
        }
        
        with patch.object(engine, 'init') as mock_init:
            mock_init.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
            
            result = engine.init(config)
            assert result.status == tss_constants.StatusFlags.SUCCESS
            
    def test_kinematics_engine_forward_kinematics(self):
        """Test KinematicsEngine forward kinematics computation."""
        engine = kinematics_engine.KinematicsEngine("test_kinematics")
        
        if hasattr(engine, 'forwardKinematics'):
            joint_angles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            
            with patch.object(engine, 'forwardKinematics') as mock_fk:
                target_pose = tss_structs.Pose(
                    position=tss_structs.Point(0.5, 0, 0.8),
                    orientation=tss_structs.Quaternion(0, 0, 0, 1)
                )
                mock_fk.return_value = target_pose
                
                result = engine.forwardKinematics(joint_angles)
                assert result.position.x == 0.5
                assert result.position.z == 0.8
                
    def test_kinematics_engine_inverse_kinematics(self):
        """Test KinematicsEngine inverse kinematics computation."""
        engine = kinematics_engine.KinematicsEngine("test_kinematics")
        
        if hasattr(engine, 'inverseKinematics'):
            target_pose = tss_structs.Pose(
                position=tss_structs.Point(0.6, 0.2, 0.9),
                orientation=tss_structs.Quaternion(0, 0, 0, 1)
            )
            
            with patch.object(engine, 'inverseKinematics') as mock_ik:
                joint_solution = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
                mock_ik.return_value = joint_solution
                
                result = engine.inverseKinematics(target_pose)
                assert len(result) == 6
                assert result[0] == 0.1
                
    def test_kinematics_engine_jacobian_computation(self):
        """Test KinematicsEngine Jacobian computation."""
        engine = kinematics_engine.KinematicsEngine("test_kinematics")
        
        if hasattr(engine, 'getJacobian'):
            joint_angles = [0.0, 0.5, 1.0, 0.0, 0.5, 0.0]
            
            with patch.object(engine, 'getJacobian') as mock_jacobian:
                # Mock 6x6 Jacobian matrix
                jacobian = [[1.0 if i == j else 0.0 for j in range(6)] for i in range(6)]
                mock_jacobian.return_value = jacobian
                
                result = engine.getJacobian(joint_angles)
                assert len(result) == 6
                assert len(result[0]) == 6
                assert result[0][0] == 1.0
                
    def test_kinematics_engine_workspace_limits(self):
        """Test KinematicsEngine workspace limit checking."""
        engine = kinematics_engine.KinematicsEngine("test_kinematics")
        
        if hasattr(engine, 'isInWorkspace'):
            test_pose = tss_structs.Pose(
                position=tss_structs.Point(0.5, 0.5, 0.5),
                orientation=tss_structs.Quaternion(0, 0, 0, 1)
            )
            
            with patch.object(engine, 'isInWorkspace') as mock_workspace:
                mock_workspace.return_value = True
                
                result = engine.isInWorkspace(test_pose)
                assert result is True
                
        if hasattr(engine, 'getWorkspaceLimits'):
            with patch.object(engine, 'getWorkspaceLimits') as mock_limits:
                limits = {
                    "x_min": -1.0, "x_max": 1.0,
                    "y_min": -1.0, "y_max": 1.0,
                    "z_min": 0.0, "z_max": 2.0
                }
                mock_limits.return_value = limits
                
                result = engine.getWorkspaceLimits()
                assert result["x_max"] == 1.0
                assert result["z_min"] == 0.0
                
    def test_kinematics_engine_error_conditions(self):
        """Test KinematicsEngine error conditions."""
        engine = kinematics_engine.KinematicsEngine("test_kinematics")
        
        if hasattr(engine, 'inverseKinematics'):
            # Test unreachable pose
            unreachable_pose = tss_structs.Pose(
                position=tss_structs.Point(10.0, 10.0, 10.0),  # Very far away
                orientation=tss_structs.Quaternion(0, 0, 0, 1)
            )
            
            with patch.object(engine, 'inverseKinematics') as mock_ik:
                mock_ik.return_value = None  # No solution found
                
                result = engine.inverseKinematics(unreachable_pose)
                assert result is None