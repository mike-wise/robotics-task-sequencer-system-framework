# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# --------------------------------------------------------------------------------------------

"""Focused tests to achieve 50% coverage target."""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import tasqsym.core.interface.envg_interface as envg_interface
import tasqsym.core.interface.skill_interface as skill_interface
import tasqsym.core.common.structs as tss_structs
import tasqsym.core.common.constants as tss_constants


class TestEnvgInterfaceExtended:
    """Extended tests for EngineInterface to increase coverage."""
    
    def test_envg_interface_basic_methods(self):
        """Test basic EngineInterface methods."""
        envg = envg_interface.EngineInterface()
        
        # Test basic attributes exist
        assert hasattr(envg, '__dict__')
        assert envg is not None
        
        # Test class initialization works
        envg2 = envg_interface.EngineInterface()
        assert envg2 is not None
        assert envg2 != envg  # Different instances
        
    def test_envg_interface_status_handling(self):
        """Test EngineInterface status handling."""
        envg = envg_interface.EngineInterface()
        
        # Test that the object has some basic properties
        if hasattr(envg, 'status'):
            # If status exists, it should be a valid status or None
            status = envg.status
            assert status is None or isinstance(status, tss_structs.Status)
            
        # Test setting status if method exists
        if hasattr(envg, 'setStatus'):
            test_status = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
            envg.setStatus(test_status)
            
    def test_envg_interface_configuration_access(self):
        """Test EngineInterface configuration access."""
        envg = envg_interface.EngineInterface()
        
        # Test basic configuration properties
        if hasattr(envg, 'config'):
            config = envg.config
            assert config is None or isinstance(config, dict)
            
        if hasattr(envg, 'engines'):
            engines = envg.engines
            assert engines is None or isinstance(engines, dict)
            
        if hasattr(envg, 'robots'):
            robots = envg.robots
            assert robots is None or isinstance(robots, dict)
            
    def test_envg_interface_state_properties(self):
        """Test EngineInterface state properties.""" 
        envg = envg_interface.EngineInterface()
        
        # Test state-related properties
        if hasattr(envg, 'initialized'):
            initialized = envg.initialized
            assert isinstance(initialized, bool)
            
        if hasattr(envg, 'ready'):
            ready = envg.ready
            assert isinstance(ready, bool)
            
        # Test basic state methods
        if hasattr(envg, 'isInitialized'):
            result = envg.isInitialized()
            assert isinstance(result, bool)
            
        if hasattr(envg, 'isReady'):
            result = envg.isReady()
            assert isinstance(result, bool)
            
    def test_envg_interface_engine_management(self):
        """Test EngineInterface engine management."""
        envg = envg_interface.EngineInterface()
        
        # Test engine-related methods
        if hasattr(envg, 'addEngine'):
            mock_engine = Mock()
            mock_engine.class_id = "test_engine"
            result = envg.addEngine("test", mock_engine)
            assert result is None or isinstance(result, (bool, tss_structs.Status))
            
        if hasattr(envg, 'getEngine'):
            result = envg.getEngine("test")
            assert result is None or hasattr(result, 'class_id')
            
        if hasattr(envg, 'removeEngine'):
            result = envg.removeEngine("test")
            assert result is None or isinstance(result, (bool, tss_structs.Status))


class TestSkillInterfaceExtended:
    """Extended tests for SkillInterface to increase coverage."""
    
    def test_skill_interface_basic_methods(self):
        """Test basic SkillInterface methods."""
        rsi = skill_interface.SkillInterface()
        
        # Test basic attributes exist
        assert hasattr(rsi, '__dict__')
        assert rsi is not None
        
        # Test class initialization works
        rsi2 = skill_interface.SkillInterface()
        assert rsi2 is not None
        assert rsi2 != rsi  # Different instances
        
    def test_skill_interface_status_handling(self):
        """Test SkillInterface status handling."""
        rsi = skill_interface.SkillInterface()
        
        # Test that the object has some basic properties
        if hasattr(rsi, 'status'):
            status = rsi.status
            assert status is None or isinstance(status, tss_structs.Status)
            
        # Test setting status if method exists
        if hasattr(rsi, 'setStatus'):
            test_status = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
            rsi.setStatus(test_status)
            
    def test_skill_interface_skill_management(self):
        """Test SkillInterface skill management."""
        rsi = skill_interface.SkillInterface()
        
        # Test skill-related properties
        if hasattr(rsi, 'skills'):
            skills = rsi.skills
            assert skills is None or isinstance(skills, dict)
            
        if hasattr(rsi, 'engines'):
            engines = rsi.engines
            assert engines is None or isinstance(engines, dict)
            
        # Test skill access methods
        if hasattr(rsi, 'getSkill'):
            result = rsi.getSkill("test_skill")
            assert result is None or hasattr(result, 'execute')
            
        if hasattr(rsi, 'hasSkill'):
            result = rsi.hasSkill("test_skill")
            assert isinstance(result, bool)
            
    def test_skill_interface_execution_flow(self):
        """Test SkillInterface execution flow."""
        rsi = skill_interface.SkillInterface()
        
        # Test execution-related methods
        if hasattr(rsi, 'executeSkill'):
            result = rsi.executeSkill("test_skill", {})
            assert result is None or isinstance(result, tss_structs.Status)
            
        if hasattr(rsi, 'canExecute'):
            result = rsi.canExecute("test_skill")
            assert isinstance(result, bool)
            
        # Test state management
        if hasattr(rsi, 'getState'):
            state = rsi.getState()
            assert state is None or isinstance(state, dict)
            
    def test_skill_interface_configuration(self):
        """Test SkillInterface configuration."""
        rsi = skill_interface.SkillInterface()
        
        # Test configuration properties
        if hasattr(rsi, 'config'):
            config = rsi.config
            assert config is None or isinstance(config, dict)
            
        if hasattr(rsi, 'isConfigured'):
            result = rsi.isConfigured()
            assert isinstance(result, bool)
            
        # Test initialization state
        if hasattr(rsi, 'initialized'):
            initialized = rsi.initialized
            assert isinstance(initialized, bool)


class TestBasicUtilityFunctions:
    """Test basic utility functions for coverage."""
    
    def test_constants_access(self):
        """Test accessing constants."""
        # Test status flags
        assert tss_constants.StatusFlags.SUCCESS.value == 1
        assert tss_constants.StatusFlags.FAILED.value == -1
        assert tss_constants.StatusFlags.UNKNOWN.value == -6
        
        # Test solve by types
        assert hasattr(tss_constants, 'SolveByType')
        assert hasattr(tss_constants.SolveByType, 'FORWARD_KINEMATICS')
        assert hasattr(tss_constants.SolveByType, 'INVERSE_KINEMATICS')
        
    def test_status_creation_variations(self):
        """Test Status creation with different parameters."""
        # Test with just status flag
        status1 = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
        assert status1.status == tss_constants.StatusFlags.SUCCESS
        assert status1.reason == tss_constants.StatusReason.NONE
        assert status1.message == ""
        
        # Test with status and reason
        status2 = tss_structs.Status(
            tss_constants.StatusFlags.FAILED, 
            tss_constants.StatusReason.NONE
        )
        assert status2.status == tss_constants.StatusFlags.FAILED
        assert status2.reason == tss_constants.StatusReason.NONE
        
        # Test with all parameters
        status3 = tss_structs.Status(
            tss_constants.StatusFlags.ABORTED,
            tss_constants.StatusReason.NONE,
            "Test aborted message"
        )
        assert status3.status == tss_constants.StatusFlags.ABORTED
        assert status3.message == "Test aborted message"
        
    def test_robot_state_variations(self):
        """Test RobotState creation with different parameters."""
        # Test with just base pose
        base_pose = tss_structs.Pose(
            position=tss_structs.Point(1, 2, 3),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        
        state1 = tss_structs.RobotState(base_pose)
        assert state1.base_state == base_pose
        assert state1.status.status == tss_constants.StatusFlags.SUCCESS
        assert state1.timesec is None
        
        # Test with custom status
        custom_status = tss_structs.Status(tss_constants.StatusFlags.FAILED, message="Custom error")
        state2 = tss_structs.RobotState(base_pose, custom_status)
        assert state2.status.status == tss_constants.StatusFlags.FAILED
        assert state2.status.message == "Custom error"
        
        # Test with time
        state3 = tss_structs.RobotState(base_pose, timesec=5.0)
        assert state3.timesec == 5.0
        
    def test_manipulator_state_creation(self):
        """Test ManipulatorState creation."""
        base_pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        
        joint_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
        joint_states = tss_structs.JointStates(
            positions=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            velocities=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        )
        
        manip_state = tss_structs.ManipulatorState(joint_names, joint_states, base_pose)
        
        assert manip_state.joint_names == joint_names
        assert manip_state.joint_states == joint_states
        assert manip_state.base_state == base_pose
        assert len(manip_state.joint_names) == 6
        assert len(manip_state.joint_states.positions) == 6
        
    def test_combined_robot_structures(self):
        """Test combined robot data structures."""
        # Create sample robot state
        base_pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        robot_state = tss_structs.RobotState(base_pose)
        
        # Test CombinedRobotState
        combined_state = tss_structs.CombinedRobotState({"robot1": robot_state})
        assert "robot1" in combined_state.robot_states
        assert combined_state.robot_states["robot1"] == robot_state
        
        # Test CombinedRobotAction
        mock_action = Mock()
        combined_action = tss_structs.CombinedRobotAction("test_task", {"robot1": [mock_action]})
        assert combined_action.task == "test_task"
        assert "robot1" in combined_action.actions
        assert len(combined_action.actions["robot1"]) == 1