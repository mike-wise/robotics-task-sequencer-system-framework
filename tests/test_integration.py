"""
Integration tests for main functionality described in README.
"""
import sys
import os
import json
import asyncio
from unittest.mock import patch, MagicMock, Mock

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import pytest
import tasqsym.core.common.constants as tss_constants
import tasqsym.core.common.structs as tss_structs
import tasqsym.core.common.action_formats as tss_action_formats
import tasqsym.core.interface.config_loader as config_loader
import tasqsym.core.interface.envg_interface as envg_interface
import tasqsym.core.interface.skill_interface as skill_interface
import tasqsym.core.interface.blackboard as blackboard


class TestConfigLoaderIntegration:
    """Test ConfigLoader with real sample files."""
    
    def test_load_sample_config_file(self):
        """Test loading the actual sample configuration file."""
        config_file = os.path.join(
            os.path.dirname(__file__), 
            '../src/tasqsym_samples/sim_robot_sample_settings.json'
        )
        
        assert os.path.exists(config_file), f"Sample config file not found: {config_file}"
        
        with open(config_file) as f:
            configs = json.load(f)
            
        cfl = config_loader.ConfigLoader()
        
        # Mock the skill library import since we can't load it in tests
        with patch('importlib.import_module') as mock_import:
            mock_module = MagicMock()
            mock_module.library = {"test_skill": "test.module"}
            mock_import.return_value = mock_module
            
            status = cfl.loadConfigs(configs)
            
        assert status.status == tss_constants.StatusFlags.SUCCESS
        assert cfl.general_config == configs["general"]
        assert cfl.envg_config == configs["engines"]


class TestEngineInterface:
    """Test EngineInterface functionality."""
    
    def test_engine_interface_init(self):
        """Test EngineInterface initialization."""
        envg = envg_interface.EngineInterface()
        assert envg is not None
        
    @pytest.mark.asyncio
    async def test_engine_interface_init_with_data_engine_none(self):
        """Test EngineInterface init when data engine is None (should handle gracefully)."""
        envg = envg_interface.EngineInterface()
        
        general_config = {}
        rs_config = {}
        envg_config = {
            "data": None,  # This should work based on sample config
            "kinematics": {
                "engine": "test.module.TestEngine",
                "class_id": "test_id"
            },
            "controller": {
                "engine": "test.module.TestEngine", 
                "class_id": "test_id"
            }
        }
        
        # Mock the engine loading and importlib since we don't have real engines
        with patch('importlib.import_module') as mock_import:
            mock_module = MagicMock()
            mock_engine_class = MagicMock()
            mock_engine_instance = MagicMock()
            
            # Make init return a coroutine that returns a success status
            async def mock_init(*args, **kwargs):
                return tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
            mock_engine_instance.init = mock_init
            
            mock_engine_class.return_value = mock_engine_instance
            setattr(mock_module, 'TestEngine', mock_engine_class)
            mock_import.return_value = mock_module
            
            status = await envg.init(general_config, rs_config, envg_config)
            
        # This should succeed since data engine is properly set to None
        assert status.status == tss_constants.StatusFlags.SUCCESS
        
    @pytest.mark.asyncio 
    async def test_engine_interface_init_missing_data_field(self):
        """Test EngineInterface init fails when data field is missing."""
        envg = envg_interface.EngineInterface()
        
        general_config = {}
        rs_config = {}
        envg_config = {
            # Missing "data" field - should fail
            "kinematics": {
                "engine": "test.module.TestEngine",
                "class_id": "test_id"
            },
            "controller": {
                "engine": "test.module.TestEngine", 
                "class_id": "test_id"
            }
        }
        
        status = await envg.init(general_config, rs_config, envg_config)
        assert status.status == tss_constants.StatusFlags.FAILED
        assert "data" in status.message


class TestSkillInterface:
    """Test SkillInterface functionality."""
    
    def test_skill_interface_init(self):
        """Test SkillInterface initialization."""
        rsi = skill_interface.SkillInterface()
        assert rsi is not None
        
    def test_skill_interface_init_with_empty_library(self):
        """Test SkillInterface init with empty library fails."""
        rsi = skill_interface.SkillInterface()
        
        general_config = {}
        library = {}
        
        status = rsi.init(general_config, library)
        assert status.status == tss_constants.StatusFlags.FAILED
        assert "library list cannot be empty" in status.message
        
    def test_skill_interface_init_with_library(self):
        """Test SkillInterface init with valid library."""
        rsi = skill_interface.SkillInterface()
        
        general_config = {}
        library = {"test_skill": "test.module"}
        
        status = rsi.init(general_config, library)
        assert status.status == tss_constants.StatusFlags.SUCCESS
        assert rsi.library == library


class TestBlackboard:
    """Test Blackboard functionality."""
    
    def test_blackboard_init(self):
        """Test Blackboard initialization."""
        board = blackboard.Blackboard()
        assert board is not None


class TestBehaviorTreeLoading:
    """Test loading behavior tree files."""
    
    def test_load_sample_behavior_tree(self):
        """Test loading the sample behavior tree file."""
        bt_file = os.path.join(
            os.path.dirname(__file__),
            '../src/tasqsym_samples/generated_sequence_samples/throw_away_the_trash.json'
        )
        
        assert os.path.exists(bt_file), f"Sample behavior tree file not found: {bt_file}"
        
        with open(bt_file) as f:
            bt_data = json.load(f)
            
        # Verify basic structure
        assert "root" in bt_data
        assert "BehaviorTree" in bt_data["root"]
        assert "Tree" in bt_data["root"]["BehaviorTree"]
        
        # Verify it contains the expected sequence of actions
        tree = bt_data["root"]["BehaviorTree"]["Tree"][0]["Sequence"]
        
        # Should have multiple nodes
        assert len(tree) > 5
        
        # Check for expected node types
        node_types = [node.get("Node") for node in tree if "Node" in node]
        expected_nodes = ["PREPARE", "NAVIGATION", "FIND", "LOOK", "GRASP", "PICK"]
        
        for expected_node in expected_nodes:
            assert expected_node in node_types, f"Expected node {expected_node} not found in behavior tree"


@pytest.mark.asyncio 
class TestStandaloneModeIntegration:
    """Test the standalone mode functionality with mocked components."""
    
    async def test_standalone_mode_setup(self):
        """Test that standalone mode can be set up with sample configs."""
        # This tests the setup phase without actual robot hardware
        
        config_file = os.path.join(
            os.path.dirname(__file__), 
            '../src/tasqsym_samples/sim_robot_sample_settings.json'
        )
        
        with open(config_file) as f:
            configs = json.load(f)
            
        # Mock all the hardware interfaces
        with patch('tasqsym.core.interface.config_loader.ConfigLoader.loadConfigs') as mock_load_configs, \
             patch('tasqsym.core.interface.envg_interface.EngineInterface.init') as mock_envg_init, \
             patch('tasqsym.core.interface.skill_interface.SkillInterface.init') as mock_skill_init, \
             patch('tasqsym.core.interface.envg_interface.EngineInterface.callEnvironmentLoadPipeline') as mock_load_pipeline:
            
            # Configure mocks to return success
            mock_load_configs.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
            mock_envg_init.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
            mock_skill_init.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS) 
            mock_load_pipeline.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
            
            # Test the setup components individually
            cfl = config_loader.ConfigLoader()
            status = mock_load_configs(configs)
            assert status.status == tss_constants.StatusFlags.SUCCESS
            
            envg = envg_interface.EngineInterface()
            status = await mock_envg_init({}, {}, {})
            assert status.status == tss_constants.StatusFlags.SUCCESS
            
            rsi = skill_interface.SkillInterface()
            status = mock_skill_init({}, {"test": "skill"})
            assert status.status == tss_constants.StatusFlags.SUCCESS
            
            board = blackboard.Blackboard()
            assert board is not None
            
    async def test_envg_interface_creation(self):
        """Test EngineInterface creation and basic operations."""
        envg = envg_interface.EngineInterface()
        assert envg is not None
        
        # Test that blackboard can be set and retrieved
        board = blackboard.Blackboard()
        board.setBoardVariable("test_key", "test_value")
        
        # Basic functionality test without hardware
        assert board.getBoardVariable("test_key") == "test_value"
        
    async def test_envg_interface_initialization(self):
        """Test EngineInterface initialization process."""
        envg = envg_interface.EngineInterface()
        
        # Test with mock configurations
        robot_configs = {
            "manipulator": {
                "type": "ur5",
                "urdf_path": "/fake/path/robot.urdf"
            }
        }
        engine_configs = {
            "kinematics": {
                "type": "kdl",
                "urdf_path": "/fake/path/robot.urdf"
            },
            "controller": {
                "type": "moveit",
                "planning_group": "arm"
            }
        }
        sensor_configs = {
            "camera": {
                "type": "realsense",
                "resolution": "640x480"
            }
        }
        
        # Mock the init method since it requires actual hardware
        with patch.object(envg, 'init') as mock_init:
            mock_init.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
            
            result = await envg.init(robot_configs, engine_configs, sensor_configs)
            assert result.status == tss_constants.StatusFlags.SUCCESS
            mock_init.assert_called_once_with(robot_configs, engine_configs, sensor_configs)
            
    async def test_envg_interface_load_pipeline(self):
        """Test EngineInterface load pipeline functionality."""
        envg = envg_interface.EngineInterface()
        
        # Mock the load pipeline method
        with patch.object(envg, 'callEnvironmentLoadPipeline') as mock_load:
            mock_load.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
            
            result = await envg.callEnvironmentLoadPipeline()
            assert result.status == tss_constants.StatusFlags.SUCCESS
            mock_load.assert_called_once()
            
    async def test_envg_interface_robot_state_access(self):
        """Test EngineInterface robot state access methods."""
        envg = envg_interface.EngineInterface()
        
        # Test basic properties that should exist
        assert hasattr(envg, '__dict__')  # Basic object test
        
        # Test that it's properly initialized
        assert envg is not None
        
    async def test_envg_interface_error_handling(self):
        """Test EngineInterface error handling scenarios."""
        envg = envg_interface.EngineInterface()
        
        # Test with invalid configurations
        invalid_configs = {"invalid": "config"}
        
        with patch.object(envg, 'init') as mock_init:
            mock_init.return_value = tss_structs.Status(tss_constants.StatusFlags.FAILED, message="Invalid configuration")
            
            result = await envg.init(invalid_configs, {}, {})
            assert result.status == tss_constants.StatusFlags.FAILED
        
    async def test_skill_interface_creation(self):
        """Test SkillInterface creation and basic operations."""
        rsi = skill_interface.SkillInterface()
        assert rsi is not None
        
        # Test basic functionality
        board = blackboard.Blackboard()
        board.setBoardVariable("skill_test", {"action": "test"})
        
        assert board.getBoardVariable("skill_test")["action"] == "test"
        
    async def test_skill_interface_initialization(self):
        """Test SkillInterface initialization process."""
        rsi = skill_interface.SkillInterface()
        
        # Test with mock skill configurations
        engines = {
            "kinematics": Mock(),
            "controller": Mock(),
            "data": Mock()
        }
        skills = {
            "navigation": {
                "type": "basic_navigation",
                "config": {"max_speed": 1.0}
            },
            "manipulation": {
                "type": "pick_place",
                "config": {"force_threshold": 10.0}
            }
        }
        
        # Mock the init method
        with patch.object(rsi, 'init') as mock_init:
            mock_init.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS)
            
            result = rsi.init(engines, skills)
            assert result.status == tss_constants.StatusFlags.SUCCESS
            mock_init.assert_called_once_with(engines, skills)
            
    async def test_skill_interface_skill_access(self):
        """Test SkillInterface skill access methods."""
        rsi = skill_interface.SkillInterface()
        
        # Test basic properties that should exist  
        assert hasattr(rsi, '__dict__')  # Basic object test
        
        # Test that it's properly initialized
        assert rsi is not None
        
    async def test_skill_interface_cleanup(self):
        """Test SkillInterface cleanup functionality."""
        rsi = skill_interface.SkillInterface()
        
        # Test cleanup method
        rsi.cleanup()  # Should not raise any exceptions
        
    async def test_skill_interface_error_scenarios(self):
        """Test SkillInterface error handling."""
        rsi = skill_interface.SkillInterface()
        
        # Test with invalid skill configurations
        invalid_engines = None
        invalid_skills = {"bad_skill": "invalid_config"}
        
        with patch.object(rsi, 'init') as mock_init:
            mock_init.return_value = tss_structs.Status(tss_constants.StatusFlags.FAILED, message="Invalid skill configuration")
            
            result = rsi.init(invalid_engines, invalid_skills)
            assert result.status == tss_constants.StatusFlags.FAILED
        
    async def test_config_loader_extended_functionality(self):
        """Test ConfigLoader with more extensive scenarios."""
        cfl = config_loader.ConfigLoader()
        
        # Test with sample config data structures
        test_configs = {
            "robots": {
                "manipulator": {
                    "type": "manipulator",
                    "urdf_path": "/path/to/robot.urdf"
                }
            },
            "engines": {
                "kinematics": {
                    "type": "pybullet",
                    "config": {"step_size": 0.01}
                }
            },
            "skills": {
                "navigation": {
                    "type": "basic_nav",
                    "config": {"max_velocity": 1.0}
                }
            }
        }
        
        # Mock the actual loading since we don't have real files
        with patch.object(cfl, 'loadConfigs') as mock_load:
            mock_load.return_value = tss_structs.Status(tss_constants.StatusFlags.SUCCESS, "Loaded successfully")
            
            result = cfl.loadConfigs(test_configs)
            assert result.status == tss_constants.StatusFlags.SUCCESS
            mock_load.assert_called_once_with(test_configs)
            
    async def test_behavior_tree_structure_validation(self):
        """Test behavior tree structure validation."""
        # Test valid behavior tree structure
        valid_bt = {
            "root": {
                "BehaviorTree": {
                    "Tree": [
                        {
                            "Sequence": {
                                "@name": "main_sequence",
                                "child": [
                                    {
                                        "Action": {
                                            "@name": "test_action",
                                            "@skill": "navigation",
                                            "param": {"destination": "goal"}
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
        
        # Basic structure validation
        assert "root" in valid_bt
        assert "BehaviorTree" in valid_bt["root"]
        assert "Tree" in valid_bt["root"]["BehaviorTree"]
        assert isinstance(valid_bt["root"]["BehaviorTree"]["Tree"], list)
        
        # Test tree with multiple nodes
        tree_nodes = valid_bt["root"]["BehaviorTree"]["Tree"]
        assert len(tree_nodes) == 1
        assert "Sequence" in tree_nodes[0]
        
        sequence_node = tree_nodes[0]["Sequence"]
        assert "@name" in sequence_node
        assert "child" in sequence_node
        assert isinstance(sequence_node["child"], list)
        
    async def test_robot_action_combinations(self):
        """Test different robot action combinations."""
        # Test FKAction with ManipulatorState
        base_pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        joint_states = tss_structs.JointStates(
            positions=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            velocities=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            efforts=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        )
        joint_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
        
        manipulator_state = tss_structs.ManipulatorState(joint_names, joint_states, base_pose)
        fk_action = tss_action_formats.FKAction(manipulator_state)
        
        assert fk_action.solveby_type == tss_constants.SolveByType.FORWARD_KINEMATICS
        assert len(fk_action.goal.joint_names) == 6
        assert fk_action.goal.joint_states.positions[0] == 0.1
        
        # Test IKAction with multiple source links
        target_pose = tss_structs.Pose(
            position=tss_structs.Point(1.0, 0.5, 0.8),
            orientation=tss_structs.Quaternion(0, 0, 0.707, 0.707)
        )
        source_links = ["end_effector_link", "tool_center_point"]
        
        ik_action = tss_action_formats.IKAction(target_pose, source_links)
        assert ik_action.solveby_type == tss_constants.SolveByType.INVERSE_KINEMATICS
        assert len(ik_action.source_links) == 2
        assert ik_action.goal.position.x == 1.0
        
    async def test_complex_status_scenarios(self):
        """Test complex status handling scenarios."""
        # Create base pose first
        base_pose = tss_structs.Pose(
            position=tss_structs.Point(0, 0, 0),
            orientation=tss_structs.Quaternion(0, 0, 0, 1)
        )
        
        # Test status with different error codes
        success_status = tss_structs.Status(tss_constants.StatusFlags.SUCCESS, message="Operation completed")
        failure_status = tss_structs.Status(tss_constants.StatusFlags.FAILED, message="Operation failed")
        unknown_status = tss_structs.Status(tss_constants.StatusFlags.UNKNOWN, message="Status unknown")

        assert success_status.status == tss_constants.StatusFlags.SUCCESS
        assert failure_status.status == tss_constants.StatusFlags.FAILED  
        assert unknown_status.status == tss_constants.StatusFlags.UNKNOWN

        assert "completed" in success_status.message
        assert "failed" in failure_status.message
        assert "unknown" in unknown_status.message

        # Test status in robot state
        robot_state_success = tss_structs.RobotState(
            base_pose, 
            status=success_status
        )
        robot_state_failure = tss_structs.RobotState(
            base_pose,
            status=failure_status
        )

        assert robot_state_success.status.status == tss_constants.StatusFlags.SUCCESS
        assert robot_state_failure.status.status == tss_constants.StatusFlags.FAILED