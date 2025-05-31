# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# --------------------------------------------------------------------------------------------

"""Tests for tasqsym.core.common.world_format module."""

import pytest
import sys
import os
from unittest.mock import Mock

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import tasqsym.core.common.world_format as world_format
import tasqsym.core.common.structs as tss_structs
import tasqsym.core.common.constants as tss_constants


class TestWorldFormat:
    """Test world format data structures."""
    
    def test_combined_robot_struct_creation(self):
        """Test creating CombinedRobotStruct."""
        # Create sample robot states
        base_pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        robot_state = tss_structs.RobotState(base_pose)
        combined_state = tss_structs.CombinedRobotState({"robot1": robot_state})
        
        # Create sample robot actions
        fk_action = Mock()
        fk_action.solveby_type = tss_constants.SolveByType.FORWARD_KINEMATICS
        combined_action = tss_structs.CombinedRobotAction("test_task", {"robot1": [fk_action]})
        
        # Create status
        status = tss_structs.Status(tss_constants.StatusFlags.SUCCESS, message="Test success")
        
        # Create CombinedRobotStruct
        combined_struct = world_format.CombinedRobotStruct(combined_state, combined_action, status)
        
        assert combined_struct.status.status == tss_constants.StatusFlags.SUCCESS
        assert combined_struct.status.message == "Test success"
        assert "robot1" in combined_struct.actual_states.robot_states
        assert combined_struct.desired_actions.task == "test_task"
        
    def test_combined_robot_struct_deep_copy(self):
        """Test that CombinedRobotStruct makes deep copies."""
        # Create original data
        base_pose = tss_structs.Pose(
            position=tss_structs.Point(1, 2, 3),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        robot_state = tss_structs.RobotState(base_pose)
        combined_state = tss_structs.CombinedRobotState({"robot1": robot_state})
        
        fk_action = Mock()
        combined_action = tss_structs.CombinedRobotAction("original_task", {"robot1": [fk_action]})
        
        status = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
        
        combined_struct = world_format.CombinedRobotStruct(combined_state, combined_action, status)
        
        # Modify original data
        combined_action.task = "modified_task"
        
        # Combined struct should have original values
        assert combined_struct.desired_actions.task == "original_task"
        
    def test_functional_states_creation(self):
        """Test creating FunctionalStates."""
        from collections import namedtuple
        
        # Create a sample named tuple for states
        StateStruct = namedtuple('StateStruct', ['position', 'velocity', 'acceleration'])
        sample_states = StateStruct(position=1.5, velocity=0.8, acceleration=0.1)
        
        functional_states = world_format.FunctionalStates(sample_states)
        
        assert functional_states.states == sample_states
        assert functional_states.states.position == 1.5
        assert functional_states.states.velocity == 0.8
        assert functional_states.states.acceleration == 0.1
        
    def test_functional_states_with_complex_data(self):
        """Test FunctionalStates with complex nested data."""
        from collections import namedtuple
        
        # Create complex state structure
        JointState = namedtuple('JointState', ['angle', 'velocity', 'torque'])
        RobotStates = namedtuple('RobotStates', ['joint1', 'joint2', 'joint3'])
        
        joint_states = RobotStates(
            joint1=JointState(1.0, 0.5, 10.0),
            joint2=JointState(2.0, 0.3, 15.0),
            joint3=JointState(1.5, 0.1, 8.0)
        )
        
        functional_states = world_format.FunctionalStates(joint_states)
        
        assert functional_states.states.joint1.angle == 1.0
        assert functional_states.states.joint2.velocity == 0.3
        assert functional_states.states.joint3.torque == 8.0
        
    def test_component_properties_creation(self):
        """Test creating ComponentProperties."""
        from collections import namedtuple
        
        # Create a sample named tuple for properties
        PropStruct = namedtuple('PropStruct', ['mass', 'length', 'material'])
        sample_properties = PropStruct(mass=2.5, length=0.8, material="aluminum")
        
        component_props = world_format.ComponentProperties(sample_properties)
        
        assert component_props.properties == sample_properties
        assert component_props.properties.mass == 2.5
        assert component_props.properties.length == 0.8
        assert component_props.properties.material == "aluminum"
        
    def test_component_properties_with_physical_data(self):
        """Test ComponentProperties with physical properties."""
        from collections import namedtuple
        
        # Create physical properties structure
        PhysicalProps = namedtuple('PhysicalProps', ['density', 'youngs_modulus', 'thermal_conductivity'])
        physical_data = PhysicalProps(
            density=2700.0,  # kg/m^3 for aluminum
            youngs_modulus=70e9,  # Pa
            thermal_conductivity=237.0  # W/m·K
        )
        
        component_props = world_format.ComponentProperties(physical_data)
        
        assert component_props.properties.density == 2700.0
        assert component_props.properties.youngs_modulus == 70e9
        assert component_props.properties.thermal_conductivity == 237.0
        
    def test_manipulation_properties_creation(self):
        """Test creating ManipulationProperties."""
        from collections import namedtuple
        
        # Create manipulation-specific properties
        ManipProps = namedtuple('ManipProps', ['max_payload', 'reach', 'repeatability'])
        manip_data = ManipProps(
            max_payload=10.0,  # kg
            reach=0.85,  # meters
            repeatability=0.05  # mm
        )
        
        manip_props = world_format.ManipulationProperties(manip_data)
        
        assert manip_props.properties == manip_data
        assert manip_props.properties.max_payload == 10.0
        assert manip_props.properties.reach == 0.85
        assert manip_props.properties.repeatability == 0.05
        
    def test_manipulation_properties_with_workspace_data(self):
        """Test ManipulationProperties with workspace definitions."""
        from collections import namedtuple
        
        # Create workspace properties
        WorkspaceProps = namedtuple('WorkspaceProps', ['min_x', 'max_x', 'min_y', 'max_y', 'min_z', 'max_z'])
        workspace_data = WorkspaceProps(
            min_x=-0.5, max_x=0.5,
            min_y=-0.8, max_y=0.8,
            min_z=0.0, max_z=1.2
        )
        
        manip_props = world_format.ManipulationProperties(workspace_data)
        
        assert manip_props.properties.min_x == -0.5
        assert manip_props.properties.max_x == 0.5
        assert manip_props.properties.min_y == -0.8
        assert manip_props.properties.max_y == 0.8
        assert manip_props.properties.min_z == 0.0
        assert manip_props.properties.max_z == 1.2
        
    def test_empty_namedtuple_handling(self):
        """Test handling of empty named tuples."""
        from collections import namedtuple
        
        EmptyStruct = namedtuple('EmptyStruct', [])
        empty_data = EmptyStruct()
        
        functional_states = world_format.FunctionalStates(empty_data)
        component_props = world_format.ComponentProperties(empty_data)
        manip_props = world_format.ManipulationProperties(empty_data)
        
        assert functional_states.states == empty_data
        assert component_props.properties == empty_data
        assert manip_props.properties == empty_data
        
    def test_single_field_namedtuple(self):
        """Test handling of single field named tuples."""
        from collections import namedtuple
        
        SingleStruct = namedtuple('SingleStruct', ['value'])
        single_data = SingleStruct(value=42)
        
        functional_states = world_format.FunctionalStates(single_data)
        
        assert functional_states.states.value == 42
        assert len(functional_states.states) == 1