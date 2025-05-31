# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# --------------------------------------------------------------------------------------------

"""Tests for tasqsym.core.common.action_formats module."""

import pytest
import sys
import os

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import tasqsym.core.common.action_formats as tss_actions
import tasqsym.core.common.structs as tss_structs
import tasqsym.core.common.constants as tss_constants


class TestFKAction:
    """Test Forward Kinematics Action class."""
    
    def test_fk_action_creation(self):
        """Test creating an FKAction with valid parameters."""
        # Create a sample robot state
        base_pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        robot_state = tss_structs.RobotState(base_pose)
        
        # Create FKAction
        action = tss_actions.FKAction(robot_state)
        
        assert action.solveby_type == tss_constants.SolveByType.FORWARD_KINEMATICS
        assert action.goal.base_state.position.x == 0
        assert action.configs == {}
        
    def test_fk_action_with_configs(self):
        """Test creating an FKAction with custom configurations."""
        base_pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        robot_state = tss_structs.RobotState(base_pose)
        configs = {"max_velocity": 1.0, "timeout": 5.0}
        
        action = tss_actions.FKAction(robot_state, configs)
        
        assert action.solveby_type == tss_constants.SolveByType.FORWARD_KINEMATICS
        assert action.configs == configs
        
    def test_fk_action_goal_copy(self):
        """Test that FKAction makes a deep copy of the goal."""
        base_pose = tss_structs.Pose(
            position=tss_structs.Point(1, 2, 3),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        robot_state = tss_structs.RobotState(base_pose)
        
        action = tss_actions.FKAction(robot_state)
        
        # Modify original robot state base pose
        original_x = robot_state.base_state.position.x
        new_pose = tss_structs.Pose(
            position=tss_structs.Point(999, 2, 3),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        robot_state.base_state = new_pose
        
        # Action should have original values due to deep copy
        assert action.goal.base_state.position.x == original_x


class TestIKAction:
    """Test Inverse Kinematics Action class."""
    
    def test_ik_action_basic_creation(self):
        """Test creating an IKAction with minimal parameters."""
        pose = tss_structs.Pose(
            position=tss_structs.Point(1.0, 2.0, 3.0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        source_links = ["end_effector_link"]
        
        action = tss_actions.IKAction(pose, source_links)
        
        assert action.solveby_type == tss_constants.SolveByType.INVERSE_KINEMATICS
        assert action.goal.position.x == 1.0
        assert action.goal.position.y == 2.0
        assert action.goal.position.z == 3.0
        assert action.source_links == source_links
        assert action.fixed_shape is None
        assert action.context == ''
        assert action.start_posture == ''
        assert action.end_posture == ''
        assert action.posture_rate == 1.0
        assert action.configs == {}
        
    def test_ik_action_full_parameters(self):
        """Test creating an IKAction with all parameters."""
        pose = tss_structs.Pose(
            position=tss_structs.Point(0.5, 1.5, 2.5),
            orientation=tss_structs.Quaternion(0, 0, 0.707, 0.707)
        )
        source_links = ["link1", "link2"]
        base_pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        fixed_shape = tss_structs.RobotState(base_pose)
        context = "manipulation"
        start_posture = "home"
        end_posture = "ready"
        posture_rate = 0.8
        configs = {"tolerance": 0.01, "max_iterations": 100}
        
        action = tss_actions.IKAction(
            pose, source_links, fixed_shape, context, 
            start_posture, end_posture, posture_rate, configs
        )
        
        assert action.solveby_type == tss_constants.SolveByType.INVERSE_KINEMATICS
        assert action.goal.position.x == 0.5
        assert action.goal.orientation.z == 0.707
        assert action.source_links == source_links
        assert action.fixed_shape.base_state.position.x == 0
        assert action.context == context
        assert action.start_posture == start_posture
        assert action.end_posture == end_posture
        assert action.posture_rate == posture_rate
        assert action.configs == configs
        
    def test_ik_action_empty_source_links(self):
        """Test creating an IKAction with empty source links."""
        pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        source_links = []
        
        action = tss_actions.IKAction(pose, source_links)
        
        assert action.source_links == []


class TestNav3DAction:
    """Test Navigation 3D Action class."""
    
    def test_nav3d_action_creation(self):
        """Test creating a Nav3DAction with valid parameters."""
        pose = tss_structs.Pose(
            position=tss_structs.Point(1.0, 2.0, 0.0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        relative_pose = tss_structs.Pose(
            position=tss_structs.Point(0.5, 0.0, 0.0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        dest_name = "kitchen"
        context = "indoor_navigation"
        timeout = 30.0
        
        action = tss_actions.Nav3DAction(pose, relative_pose, dest_name, context, timeout)
        
        assert action.solveby_type == tss_constants.SolveByType.NAVIGATION3D
        assert action.pose.position.x == 1.0
        assert action.pose.position.y == 2.0
        assert action.relative_pose.position.x == 0.5
        assert action.dest_name == dest_name
        assert action.context == context
        assert action.timeout == timeout
        assert action.configs == {}
        
    def test_nav3d_action_default_timeout(self):
        """Test creating a Nav3DAction with default timeout."""
        pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        relative_pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        
        action = tss_actions.Nav3DAction(pose, relative_pose, "home", "test")
        
        assert action.timeout == -1  # default infinite timeout
        
    def test_nav3d_action_with_configs(self):
        """Test creating a Nav3DAction with configurations."""
        pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        relative_pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        configs = {"max_velocity": 1.0, "obstacle_padding": 0.1}
        
        action = tss_actions.Nav3DAction(pose, relative_pose, "goal", "context", 10.0, configs)
        
        assert action.configs == configs


class TestPointToAction:
    """Test Point To Action class."""
    
    def test_point_to_action_creation(self):
        """Test creating a PointToAction with valid parameters."""
        point = tss_structs.Point(1.0, 2.0, 3.0)
        source_link = "camera_link"
        context = "object_tracking"
        
        action = tss_actions.PointToAction(point, source_link, context)
        
        assert action.solveby_type == tss_constants.SolveByType.POINT_TO_IK
        assert action.point.x == 1.0
        assert action.point.y == 2.0
        assert action.point.z == 3.0
        assert action.source_link == source_link
        assert action.context == context
        assert action.configs == {}
        
    def test_point_to_action_with_configs(self):
        """Test creating a PointToAction with configurations."""
        point = tss_structs.Point(0, 0, 1)
        source_link = "sensor_link"
        context = "calibration"
        configs = {"tolerance": 0.001, "max_iterations": 50}
        
        action = tss_actions.PointToAction(point, source_link, context, configs)
        
        assert action.configs == configs
        
    def test_point_to_action_empty_context(self):
        """Test creating a PointToAction with empty context."""
        point = tss_structs.Point(5, 10, 15)
        source_link = "head_link"
        
        action = tss_actions.PointToAction(point, source_link, "")
        
        assert action.context == ""


class TestCommandAction:
    """Test Command Action class."""
    
    def test_command_action_creation(self):
        """Test creating a CommandAction with valid parameters."""
        commands = {
            "gripper": "open",
            "velocity": 0.5,
            "force_limit": 100.0
        }
        
        action = tss_actions.CommandAction(commands)
        
        assert action.solveby_type == tss_constants.SolveByType.CONTROL_COMMAND
        assert action.commands == commands
        assert action.configs == {}
        
    def test_command_action_empty_commands(self):
        """Test creating a CommandAction with empty commands."""
        commands = {}
        
        action = tss_actions.CommandAction(commands)
        
        assert action.commands == {}
        
    def test_command_action_with_configs(self):
        """Test creating a CommandAction with configurations."""
        commands = {"motor": "start", "speed": 100}
        configs = {"timeout": 5.0, "retry_attempts": 3}
        
        action = tss_actions.CommandAction(commands, configs)
        
        assert action.commands == commands
        assert action.configs == configs
        
    def test_command_action_complex_commands(self):
        """Test creating a CommandAction with complex command structure."""
        commands = {
            "joint_commands": {
                "joint1": 0.1,
                "joint2": 0.2,
                "joint3": 0.3
            },
            "gripper_command": {
                "position": 0.5,
                "force": 50.0
            },
            "mode": "position_control"
        }
        
        action = tss_actions.CommandAction(commands)
        
        assert action.commands["joint_commands"]["joint1"] == 0.1
        assert action.commands["gripper_command"]["position"] == 0.5
        assert action.commands["mode"] == "position_control"