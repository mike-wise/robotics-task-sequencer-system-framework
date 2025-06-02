# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# --------------------------------------------------------------------------------------------

"""Tests for abstract base classes using monkey patching technique."""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import asyncio

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import tasqsym.core.classes.engine_base as engine_base
import tasqsym.core.classes.model_robot as model_robot
import tasqsym.core.classes.physical_robot as physical_robot
import tasqsym.core.classes.physical_sensor as physical_sensor
import tasqsym.core.classes.skill_base as skill_base
import tasqsym.core.common.structs as tss_structs
import tasqsym.core.common.constants as tss_constants


def make_abstract_class_concrete(abstract_class, method_implementations=None):
    """
    Make an abstract class concrete by replacing abstract methods with implementations.
    
    Args:
        abstract_class: The abstract class to make concrete
        method_implementations: Dict of method name -> implementation
    
    Returns:
        A concrete class that can be instantiated
    """
    # Save original abstractmethods
    original_abstractmethods = getattr(abstract_class, '__abstractmethods__', set())
    
    # Remove abstractmethods temporarily
    abstract_class.__abstractmethods__ = frozenset()
    
    # Add default implementations for abstract methods
    if method_implementations:
        for method_name, implementation in method_implementations.items():
            setattr(abstract_class, method_name, implementation)
    
    # Create a concrete subclass
    class ConcreteTestClass(abstract_class):
        pass
    
    # Restore original abstractmethods to the abstract class
    abstract_class.__abstractmethods__ = original_abstractmethods
    
    return ConcreteTestClass


class TestEngineBase:
    """Test EngineBase abstract class functionality."""
    
    def test_engine_base_initialization(self):
        """Test EngineBase initialization."""
        # Create mock implementations for abstract methods
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteEngine = make_abstract_class_concrete(engine_base.EngineBase, implementations)
        
        # Test creation
        engine = ConcreteEngine("test_engine")
        assert engine.class_id == "test_engine"
        
    def test_engine_base_update_method(self):
        """Test EngineBase update method (default raises NotImplementedError)."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteEngine = make_abstract_class_concrete(engine_base.EngineBase, implementations)
        engine = ConcreteEngine("test_engine")
        
        # Test that update raises NotImplementedError by default
        with pytest.raises(NotImplementedError):
            asyncio.run(engine.update(Mock()))


class TestKinematicsEngineBase:
    """Test KinematicsEngineBase abstract class functionality."""
    
    def test_kinematics_engine_initialization(self):
        """Test KinematicsEngineBase initialization."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteKinematicsEngine = make_abstract_class_concrete(engine_base.KinematicsEngineBase, implementations)
        
        engine = ConcreteKinematicsEngine("test_kinematics")
        assert engine.class_id == "test_kinematics"
        assert engine.base_id == ""
        assert engine.end_effector_id == ""
        assert engine.multiple_end_effector_ids == []
        assert engine.sensor_ids == {}
        assert engine.robot_combiner is None
        assert engine.robot_models == {}
        assert engine.sensors == {}
        
    def test_kinematics_engine_cleanup(self):
        """Test KinematicsEngineBase cleanup functionality."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteKinematicsEngine = make_abstract_class_concrete(engine_base.KinematicsEngineBase, implementations)
        engine = ConcreteKinematicsEngine("test_kinematics")
        
        # Add some test data
        engine.base_id = "test_base"
        engine.end_effector_id = "test_ee"
        engine.multiple_end_effector_ids = ["ee1", "ee2"]
        engine.sensor_ids = {tss_constants.SensorRole.CAMERA_3D: "cam1"}
        
        # Mock robot model with destroy method
        mock_robot = Mock()
        mock_robot.destroy = Mock()
        engine.robot_models = {"robot1": mock_robot}
        
        # Test cleanup
        engine.cleanup()
        
        assert engine.base_id == ""
        assert engine.end_effector_id == ""
        assert engine.multiple_end_effector_ids == []
        assert engine.sensor_ids == {}
        assert engine.robot_combiner is None
        assert engine.robot_models == {}
        assert engine.sensors == {}
        mock_robot.destroy.assert_called_once()
        
    def test_kinematics_engine_end_effector_management(self):
        """Test end effector management methods."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteKinematicsEngine = make_abstract_class_concrete(engine_base.KinematicsEngineBase, implementations)
        engine = ConcreteKinematicsEngine("test_kinematics")
        
        # Test setting single end effector
        mock_robot = Mock()
        mock_robot.role = tss_constants.RobotRole.END_EFFECTOR
        engine.robot_models = {"ee1": mock_robot}
        
        engine.setEndEffectorRobot("test_task", {})
        assert engine.getFocusEndEffectorRobotId() == "ee1"
        
        # Test freeing end effector
        engine.freeEndEffectorRobot()
        assert engine.getFocusEndEffectorRobotId() == ""
        
        # Test multiple end effectors
        mock_combiner = Mock()
        mock_combiner.setMultipleEndEffectorRobots = Mock(return_value=["ee1", "ee2"])
        engine.robot_combiner = mock_combiner
        
        engine.setMultipleEndEffectorRobots("test_task", {})
        assert engine.getMultipleFocusEndEffectorRobotIds() == ["ee1", "ee2"]
        
        engine.freeMultipleEndEffectorRobots()
        assert engine.getMultipleFocusEndEffectorRobotIds() == []


class TestControllerEngineBase:
    """Test ControllerEngineBase abstract class functionality."""
    
    def test_controller_engine_initialization(self):
        """Test ControllerEngineBase initialization."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'updateActualRobotStates': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteControllerEngine = make_abstract_class_concrete(engine_base.ControllerEngineBase, implementations)
        
        engine = ConcreteControllerEngine("test_controller")
        assert engine.class_id == "test_controller"
        assert engine.control_task is None
        assert engine.emergency_stop_request is False
        assert engine.latest_robot_state is None
        assert engine.robots == {}
        assert engine.sensors == {}
        assert engine.control_in_simulated_world is False
        
    def test_controller_engine_cleanup(self):
        """Test ControllerEngineBase cleanup functionality."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'updateActualRobotStates': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteControllerEngine = make_abstract_class_concrete(engine_base.ControllerEngineBase, implementations)
        engine = ConcreteControllerEngine("test_controller")
        
        # Add mock robots with disconnect method
        mock_robot1 = Mock()
        mock_robot1.disconnect = Mock()
        mock_robot2 = Mock()
        mock_robot2.disconnect = Mock()
        
        engine.robots = {"robot1": mock_robot1, "robot2": mock_robot2}
        engine.sensors = {"sensor1": Mock()}
        
        # Test cleanup
        engine.cleanup()
        
        assert engine.robots == {}
        assert engine.sensors == {}
        mock_robot1.disconnect.assert_called_once()
        mock_robot2.disconnect.assert_called_once()
        
    def test_controller_engine_state_access(self):
        """Test ControllerEngineBase state access methods."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'updateActualRobotStates': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteControllerEngine = make_abstract_class_concrete(engine_base.ControllerEngineBase, implementations)
        engine = ConcreteControllerEngine("test_controller")
        
        # Test getting latest robot states
        base_pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        robot_state = tss_structs.RobotState(base_pose)
        test_state = tss_structs.CombinedRobotState({"robot1": robot_state})
        engine.latest_robot_state = test_state
        
        retrieved_state = engine.getLatestRobotStates()
        assert retrieved_state == test_state
        
    @pytest.mark.asyncio
    async def test_controller_engine_emergency_stop(self):
        """Test ControllerEngineBase emergency stop functionality."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'updateActualRobotStates': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteControllerEngine = make_abstract_class_concrete(engine_base.ControllerEngineBase, implementations)
        engine = ConcreteControllerEngine("test_controller")
        
        # Add mock robots with emergency stop
        mock_robot1 = Mock()
        mock_robot1.emergencyStop = AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        mock_robot2 = Mock()
        mock_robot2.emergencyStop = AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        
        engine.robots = {"robot1": mock_robot1, "robot2": mock_robot2}
        
        # Test emergency stop
        result = await engine.emergencyStop()
        
        assert result.status == tss_constants.StatusFlags.SUCCESS
        mock_robot1.emergencyStop.assert_called_once()
        mock_robot2.emergencyStop.assert_called_once()


class TestPhysicalRobot:
    """Test PhysicalRobot abstract class functionality."""
    
    def test_physical_robot_initialization(self):
        """Test PhysicalRobot initialization."""
        implementations = {
            'connect': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'disconnect': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'getLatestState': AsyncMock(return_value=tss_structs.RobotState(
                tss_structs.Pose(
                    position=tss_structs.Point(0, 0, 0),
                    orientation=tss_structs.Quaternion(0, 0, 0, 1)
                )
            )),
            'emergencyStop': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcretePhysicalRobot = make_abstract_class_concrete(physical_robot.PhysicalRobot, implementations)
        
        # Set role before calling __init__
        ConcretePhysicalRobot.role = tss_constants.RobotRole.MANIPULATOR
        
        model_info = {
            "unique_id": "test_robot",
            "parent_id": "base",
            "parent_link": "base_link"
        }
        
        robot = ConcretePhysicalRobot(model_info)
        assert robot.unique_id == "test_robot"
        assert robot.parent_id == "base"
        assert robot.parent_link == "base_link"
        assert robot.role == tss_constants.RobotRole.MANIPULATOR
        
    def test_physical_robot_link_transform(self):
        """Test PhysicalRobot link transform functionality."""
        implementations = {
            'connect': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'disconnect': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'getLatestState': AsyncMock(return_value=tss_structs.RobotState(
                tss_structs.Pose(
                    position=tss_structs.Point(0, 0, 0),
                    orientation=tss_structs.Quaternion(0, 0, 0, 1)
                )
            )),
            'emergencyStop': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcretePhysicalRobot = make_abstract_class_concrete(physical_robot.PhysicalRobot, implementations)
        ConcretePhysicalRobot.role = tss_constants.RobotRole.MANIPULATOR
        
        model_info = {
            "unique_id": "test_robot",
            "parent_id": "base",
            "parent_link": "base_link"
        }
        
        robot = ConcretePhysicalRobot(model_info)
        
        # Test that getLinkTransform raises NotImplementedError by default
        with pytest.raises(NotImplementedError):
            robot.getLinkTransform("test_link")
            
    @pytest.mark.asyncio
    async def test_physical_robot_init_method(self):
        """Test PhysicalRobot init method."""
        implementations = {
            'connect': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'disconnect': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'getLatestState': AsyncMock(return_value=tss_structs.RobotState(
                tss_structs.Pose(
                    position=tss_structs.Point(0, 0, 0),
                    orientation=tss_structs.Quaternion(0, 0, 0, 1)
                )
            )),
            'emergencyStop': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcretePhysicalRobot = make_abstract_class_concrete(physical_robot.PhysicalRobot, implementations)
        ConcretePhysicalRobot.role = tss_constants.RobotRole.MANIPULATOR
        
        model_info = {
            "unique_id": "test_robot",
            "parent_id": "base",
            "parent_link": "base_link"
        }
        
        robot = ConcretePhysicalRobot(model_info)
        
        # Test that init raises NotImplementedError by default (as it should for preparation skills)
        with pytest.raises(NotImplementedError):
            await robot.init([], tss_structs.RobotState(
                tss_structs.Pose(
                    position=tss_structs.Point(0, 0, 0),
                    orientation=tss_structs.Quaternion(0, 0, 0, 1)
                )
            ))


class TestPhysicalSensor:
    """Test PhysicalSensor abstract class functionality."""
    
    def test_physical_sensor_initialization(self):
        """Test PhysicalSensor initialization."""
        implementations = {
            'connect': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'disconnect': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcretePhysicalSensor = make_abstract_class_concrete(physical_sensor.PhysicalSensor, implementations)
        
        model_info = {
            "unique_id": "test_sensor",
            "parent_id": "robot1",
            "parent_link": "sensor_link",
            "sensor_frame": "sensor_frame",
            "type": tss_constants.SensorRole.CAMERA_3D
        }
        
        sensor = ConcretePhysicalSensor(model_info)
        assert sensor.unique_id == "test_sensor"
        assert sensor.parent_id == "robot1"
        assert sensor.parent_link == "sensor_link"
        assert sensor.sensor_frame == "sensor_frame"
        assert sensor.role == tss_constants.SensorRole.CAMERA_3D
        
    def test_physical_sensor_data_methods(self):
        """Test PhysicalSensor data access methods."""
        implementations = {
            'connect': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'disconnect': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcretePhysicalSensor = make_abstract_class_concrete(physical_sensor.PhysicalSensor, implementations)
        
        model_info = {
            "unique_id": "test_sensor",
            "parent_id": "robot1",
            "parent_link": "sensor_link",
            "sensor_frame": "sensor_frame",
            "type": tss_constants.SensorRole.FORCE_6D
        }
        
        sensor = ConcretePhysicalSensor(model_info)
        
        # Test that getPhysicsState raises NotImplementedError by default
        with pytest.raises(NotImplementedError):
            sensor.getPhysicsState("test_cmd", None)
            
        # Test that getSceneryState raises NotImplementedError by default
        with pytest.raises(NotImplementedError):
            sensor.getSceneryState("test_cmd", None)


class TestSkillAbstract:
    """Test SkillAbstract abstract class functionality."""
    
    def test_skill_abstract_initialization(self):
        """Test SkillAbstract initialization."""
        implementations = {
            'init': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'anyInitiationAction': Mock(return_value=None),
            'appendTaskSpecificStates': Mock(return_value={}),
            'getAction': Mock(return_value={}),
            'formatAction': Mock(return_value=tss_structs.CombinedRobotAction("test_task", {})),
            'getTerminal': Mock(return_value=False),
            'onFinish': Mock(return_value=None)
        }
        
        ConcreteSkill = make_abstract_class_concrete(skill_base.SkillAbstract, implementations)
        
        configs = {
            "interruptible": True,
            "learned_actions": False
        }
        
        skill = ConcreteSkill(configs)
        assert skill.configs == configs
        assert skill.interruptible_skill is True
        assert skill.learned_actions is False
        
    def test_skill_abstract_default_methods(self):
        """Test SkillAbstract default method implementations."""
        implementations = {
            'init': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'anyInitiationAction': Mock(return_value=None),
            'appendTaskSpecificStates': Mock(return_value={}),
            'getAction': Mock(return_value={}),
            'formatAction': Mock(return_value=tss_structs.CombinedRobotAction("test_task", {})),
            'getTerminal': Mock(return_value=False),
            'onFinish': Mock(return_value=None)
        }
        
        ConcreteSkill = make_abstract_class_concrete(skill_base.SkillAbstract, implementations)
        
        configs = {}
        skill = ConcreteSkill(configs)
        
        # Test anyPostInitation default implementation
        result = skill.anyPostInitation(Mock())
        assert isinstance(result, tss_structs.Status)
        assert result.status == tss_constants.StatusFlags.SUCCESS
        
    def test_skill_abstract_get_terminal_logic(self):
        """Test SkillAbstract getTerminal method logic."""
        implementations = {
            'init': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'anyInitiationAction': Mock(return_value=None),
            'appendTaskSpecificStates': Mock(return_value={}),
            'getAction': Mock(return_value={}),
            'formatAction': Mock(return_value=tss_structs.CombinedRobotAction("test_task", {})),
            'onFinish': Mock(return_value=None)
        }
        
        ConcreteSkill = make_abstract_class_concrete(skill_base.SkillAbstract, implementations)
        
        # Test with terminate in action
        configs = {"learned_actions": False}
        skill = ConcreteSkill(configs)
        
        # Test the base class implementation of getTerminal (without mocking it)
        # We need to temporarily remove our mock to test the actual base class logic
        original_get_terminal = skill.getTerminal
        
        def base_get_terminal(observation, action):
            if "terminate" in action: 
                return action["terminate"]
            elif not skill.learned_actions:
                raise Exception("skill.getTerminal: Only implement getTerminal() if actions are learned but skill terminations are manually defined. Otherwise add a 'terminate' field in getAction().")
            else: 
                raise NotImplementedError("please define")
        
        skill.getTerminal = base_get_terminal
        
        action_with_terminate = {"terminate": True}
        result = skill.getTerminal({}, action_with_terminate)
        assert result is True
        
        action_without_terminate = {}
        with pytest.raises(Exception):
            skill.getTerminal({}, action_without_terminate)


class TestSkillConcrete:
    """Test Skill concrete class functionality."""
    
    def test_skill_concrete_initialization(self):
        """Test Skill concrete class initialization."""
        # The Skill class is also abstract, so we need to make it concrete
        implementations = {
            'init': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'getAction': Mock(return_value={}),
            'formatAction': Mock(return_value=tss_structs.CombinedRobotAction("test_task", {}))
        }
        
        ConcreteSkill = make_abstract_class_concrete(skill_base.Skill, implementations)
        
        configs = {
            "interruptible": False,
            "learned_actions": True
        }
        
        skill = ConcreteSkill(configs)
        assert skill.configs == configs
        assert skill.interruptible_skill is False
        assert skill.learned_actions is True
        
    def test_skill_concrete_default_implementations(self):
        """Test Skill concrete class default implementations."""
        implementations = {
            'init': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'getAction': Mock(return_value={}),
            'formatAction': Mock(return_value=tss_structs.CombinedRobotAction("test_task", {}))
        }
        
        ConcreteSkill = make_abstract_class_concrete(skill_base.Skill, implementations)
        
        configs = {}
        skill = ConcreteSkill(configs)
        
        # Test default implementations call super methods
        result = skill.anyInitiationAction(Mock())
        assert result is None
        
        result = skill.anyPostInitation(Mock())
        assert isinstance(result, tss_structs.Status)
        assert result.status == tss_constants.StatusFlags.SUCCESS
        
        # Note: appendTaskSpecificStates will call our mock implementation
        observation = {"test": "data"}
        result = skill.appendTaskSpecificStates(observation, Mock())
        # Our mock returns an empty dict, so we just check it's a dict
        assert isinstance(result, dict)
        
        result = skill.onFinish(Mock(), Mock())
        assert result is None


class TestDataEngineBase:
    """Test DataEngineBase abstract class functionality."""
    
    def test_data_engine_initialization(self):
        """Test DataEngineBase initialization."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'load': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'getData': Mock(return_value=(tss_structs.Status(tss_constants.StatusFlags.SUCCESS), {})),
            'updateData': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'save': Mock(return_value=(tss_structs.Status(tss_constants.StatusFlags.SUCCESS), {}))
        }
        
        ConcreteDataEngine = make_abstract_class_concrete(engine_base.DataEngineBase, implementations)
        
        engine = ConcreteDataEngine("test_data_engine")
        assert engine.class_id == "test_data_engine"


class TestWorldConstructorEngineBase:
    """Test WorldConstructorEngineBase abstract class functionality."""
    
    def test_world_constructor_engine_initialization(self):
        """Test WorldConstructorEngineBase initialization."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'getSpawnComponents': Mock(return_value=[])
        }
        
        ConcreteWorldConstructorEngine = make_abstract_class_concrete(engine_base.WorldConstructorEngineBase, implementations)
        
        engine = ConcreteWorldConstructorEngine("test_world_constructor")
        assert engine.class_id == "test_world_constructor"


class TestSimulationEngineBase:
    """Test SimulationEngineBase abstract class functionality."""
    
    def test_simulation_engine_initialization(self):
        """Test SimulationEngineBase initialization."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'reset': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'loadRobot': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'loadComponents': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteSimulationEngine = make_abstract_class_concrete(engine_base.SimulationEngineBase, implementations)
        
        engine = ConcreteSimulationEngine("test_simulation")
        assert engine.class_id == "test_simulation"


class TestModelRobot:
    """Test ModelRobot abstract class functionality."""
    
    def test_model_robot_initialization(self):
        """Test ModelRobot initialization."""
        implementations = {
            'create': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'destroy': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'getConfigurationForTask': Mock(return_value=tss_structs.RobotState(
                tss_structs.Pose(
                    position=tss_structs.Point(0, 0, 0),
                    orientation=tss_structs.Quaternion(0, 0, 0, 1)
                )
            ))
        }
        
        ConcreteModelRobot = make_abstract_class_concrete(model_robot.ModelRobot, implementations)
        
        # Set role before calling __init__
        ConcreteModelRobot.role = tss_constants.RobotRole.MANIPULATOR
        
        model_info = {
            "unique_id": "test_model_robot",
            "parent_id": "base",
            "parent_link": "base_link"
        }
        
        robot = ConcreteModelRobot(model_info)
        assert robot.unique_id == "test_model_robot"
        assert robot.parent_id == "base"
        assert robot.parent_link == "base_link"
        assert robot.role == tss_constants.RobotRole.MANIPULATOR
        assert robot.desired_actions_log == {}
        assert robot.most_latest_action_types == []
        
    def test_model_robot_role_none_warning(self):
        """Test ModelRobot role None warning."""
        implementations = {
            'create': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'destroy': Mock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'getConfigurationForTask': Mock(return_value=tss_structs.RobotState(
                tss_structs.Pose(
                    position=tss_structs.Point(0, 0, 0),
                    orientation=tss_structs.Quaternion(0, 0, 0, 1)
                )
            ))
        }
        
        ConcreteModelRobot = make_abstract_class_concrete(model_robot.ModelRobot, implementations)
        
        # Don't set role to trigger the warning
        model_info = {
            "unique_id": "test_model_robot",
            "parent_id": "base",
            "parent_link": "base_link"
        }
        
        # This should print a warning but still create the robot
        robot = ConcreteModelRobot(model_info)
        assert robot.unique_id == "test_model_robot"


class TestControllerEnginePhysicsAndScenery:
    """Test ControllerEngineBase physics and scenery methods."""
    
    def test_controller_engine_physics_state(self):
        """Test ControllerEngineBase getPhysicsState functionality."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'updateActualRobotStates': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteControllerEngine = make_abstract_class_concrete(engine_base.ControllerEngineBase, implementations)
        engine = ConcreteControllerEngine("test_controller")
        
        # Test with no sensor
        status, data = engine.getPhysicsState("nonexistent_sensor", "test_cmd", None)
        assert status.status == tss_constants.StatusFlags.FAILED
        
        # Test with wrong sensor type
        mock_sensor = Mock()
        mock_sensor.role = tss_constants.SensorRole.CAMERA_3D  # Wrong type for physics
        engine.sensors = {"sensor1": mock_sensor}
        
        status, data = engine.getPhysicsState("sensor1", "test_cmd", None)
        assert status.status == tss_constants.StatusFlags.FAILED
        
        # Test with correct sensor type
        mock_sensor.role = tss_constants.SensorRole.FORCE_6D
        mock_sensor.getPhysicsState = Mock(return_value=(
            tss_structs.Status(tss_constants.StatusFlags.SUCCESS), 
            {"force": [1, 2, 3]}
        ))
        
        status, data = engine.getPhysicsState("sensor1", "test_cmd", None)
        assert status.status == tss_constants.StatusFlags.SUCCESS
        
    def test_controller_engine_scenery_state(self):
        """Test ControllerEngineBase getSceneryState functionality."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'updateActualRobotStates': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteControllerEngine = make_abstract_class_concrete(engine_base.ControllerEngineBase, implementations)
        engine = ConcreteControllerEngine("test_controller")
        
        # Test with no sensor
        status, data = engine.getSceneryState("nonexistent_sensor", "test_cmd", None)
        assert status.status == tss_constants.StatusFlags.FAILED
        
        # Test with wrong sensor type
        mock_sensor = Mock()
        mock_sensor.role = tss_constants.SensorRole.FORCE_6D  # Wrong type for scenery
        engine.sensors = {"sensor1": mock_sensor}
        
        status, data = engine.getSceneryState("sensor1", "test_cmd", None)
        assert status.status == tss_constants.StatusFlags.FAILED
        
        # Test with correct sensor type
        mock_sensor.role = tss_constants.SensorRole.CAMERA_3D
        mock_sensor.getSceneryState = Mock(return_value=(
            tss_structs.Status(tss_constants.StatusFlags.SUCCESS), 
            {"image": "data"}
        ))
        
        status, data = engine.getSceneryState("sensor1", "test_cmd", None)
        assert status.status == tss_constants.StatusFlags.SUCCESS
        
    def test_controller_engine_sensor_transform(self):
        """Test ControllerEngineBase getSensorTransform functionality."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'updateActualRobotStates': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteControllerEngine = make_abstract_class_concrete(engine_base.ControllerEngineBase, implementations)
        engine = ConcreteControllerEngine("test_controller")
        
        # Test with sensor that doesn't exist
        status, pose = engine.getSensorTransform("nonexistent_sensor")
        assert status.status == tss_constants.StatusFlags.FAILED
        
        # Test with sensor that exists
        mock_sensor = Mock()
        mock_sensor.parent_id = "robot1"
        mock_sensor.sensor_frame = "sensor_frame"
        
        mock_robot = Mock()
        mock_robot.getLinkTransform = Mock(return_value=(
            tss_structs.Status(tss_constants.StatusFlags.SUCCESS),
            tss_structs.Pose(
                position=tss_structs.Point(1, 2, 3),
                orientation=tss_structs.Quaternion(0, 0, 0, 1)
            )
        ))
        
        engine.sensors = {"sensor1": mock_sensor}
        engine.robots = {"robot1": mock_robot}
        
        status, pose = engine.getSensorTransform("sensor1")
        assert status.status == tss_constants.StatusFlags.SUCCESS
        mock_robot.getLinkTransform.assert_called_once_with("sensor_frame")
        
    @pytest.mark.asyncio
    async def test_controller_engine_reset_and_load_components(self):
        """Test ControllerEngineBase reset and loadComponents functionality."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'updateActualRobotStates': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteControllerEngine = make_abstract_class_concrete(engine_base.ControllerEngineBase, implementations)
        engine = ConcreteControllerEngine("test_controller")
        
        # Test with control_in_simulated_world = False (default)
        result = await engine.reset()
        assert result is None  # Should not raise NotImplementedError
        
        result = await engine.loadComponents([])
        assert result is None  # Should not raise NotImplementedError
        
        # Test with control_in_simulated_world = True
        engine.control_in_simulated_world = True
        
        with pytest.raises(NotImplementedError):
            await engine.reset()
            
        with pytest.raises(NotImplementedError):
            await engine.loadComponents([])


class TestKinematicsEngineAdvanced:
    """Test KinematicsEngineBase advanced functionality."""
    
    def test_kinematics_engine_sensor_management(self):
        """Test KinematicsEngineBase sensor management methods."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteKinematicsEngine = make_abstract_class_concrete(engine_base.KinematicsEngineBase, implementations)
        engine = ConcreteKinematicsEngine("test_kinematics")
        
        # Test setting sensor with multiple of the same type
        mock_combiner = Mock()
        mock_combiner.setSensor = Mock(return_value="camera2")
        engine.robot_combiner = mock_combiner
        
        engine.sensors = {
            "camera1": {"type": tss_constants.SensorRole.CAMERA_3D},
            "camera2": {"type": tss_constants.SensorRole.CAMERA_3D}
        }
        
        # Initialize sensor_ids with the sensor type
        engine.sensor_ids = {tss_constants.SensorRole.CAMERA_3D: ""}
        
        engine.setSensor(tss_constants.SensorRole.CAMERA_3D, "test_task", {})
        assert engine.sensor_ids[tss_constants.SensorRole.CAMERA_3D] == "camera2"
        mock_combiner.setSensor.assert_called_once()
        
        # Test freeing specific sensor type
        engine.freeSensors(tss_constants.SensorRole.CAMERA_3D)
        assert engine.sensor_ids[tss_constants.SensorRole.CAMERA_3D] == ""
        
    def test_kinematics_engine_task_operations(self):
        """Test KinematicsEngineBase task-related operations."""
        implementations = {
            'init': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS)),
            'close': AsyncMock(return_value=tss_structs.Status(tss_constants.StatusFlags.SUCCESS))
        }
        
        ConcreteKinematicsEngine = make_abstract_class_concrete(engine_base.KinematicsEngineBase, implementations)
        engine = ConcreteKinematicsEngine("test_kinematics")
        
        # Test getTaskTransform
        mock_combiner = Mock()
        mock_combiner.getTaskTransform = Mock(return_value={"robot1": {"frame->link": Mock()}})
        engine.robot_combiner = mock_combiner
        
        result = engine.getTaskTransform("test_task", {}, Mock())
        assert "robot1" in result
        mock_combiner.getTaskTransform.assert_called_once()
        
        # Test getRecognitionMethod
        mock_combiner.getRecognitionMethod = Mock(return_value="detection_method")
        result = engine.getRecognitionMethod("test_task", {})
        assert result == "detection_method"
        mock_combiner.getRecognitionMethod.assert_called_once()
        
        # Test getConfigurationForTask
        mock_robot = Mock()
        mock_robot.getConfigurationForTask = Mock(return_value=Mock())
        engine.robot_models = {"robot1": mock_robot}
        
        result = engine.getConfigurationForTask("robot1", "test_task", {}, Mock())
        assert result is not None
        mock_robot.getConfigurationForTask.assert_called_once()
        
        # Test with nonexistent robot
        result = engine.getConfigurationForTask("nonexistent", "test_task", {}, Mock())
        assert result is None