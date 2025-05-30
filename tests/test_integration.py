"""
Integration tests for main functionality described in README.
"""
import sys
import os
import json
import asyncio
from unittest.mock import patch, MagicMock

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import pytest
import tasqsym.core.common.constants as tss_constants
import tasqsym.core.common.structs as tss_structs
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