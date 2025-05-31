"""
Unit tests for ConfigLoader class.
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


class TestConfigLoader:
    """Test ConfigLoader functionality."""
    
    def test_config_loader_init(self):
        """Test ConfigLoader initialization."""
        cfl = config_loader.ConfigLoader()
        assert cfl is not None
        
    def test_load_configs_missing_general(self):
        """Test loading config without general field fails."""
        cfl = config_loader.ConfigLoader()
        configs = {"library": "test", "robot_structure": "test"}
        
        status = cfl.loadConfigs(configs)
        assert status.status == tss_constants.StatusFlags.FAILED
        assert "general" in status.message
        
    def test_load_configs_missing_engines(self):
        """Test loading config without engines field fails."""
        cfl = config_loader.ConfigLoader()
        configs = {
            "general": {},
            "library": {"test_skill": "test_module"},  # Direct content to avoid import
            "robot_structure": {"robots": []}  # Direct content to avoid file read
        }
        
        status = cfl.loadConfigs(configs)
        assert status.status == tss_constants.StatusFlags.FAILED
        assert "engines" in status.message
        
    def test_load_configs_with_direct_content(self):
        """Test loading config with direct content (not file paths)."""
        cfl = config_loader.ConfigLoader()
        
        # Create a minimal valid config with direct content
        configs = {
            "general": {"test": "value"},
            "library": {"test_skill": "test_module"},  # Direct content
            "robot_structure": {"robots": []},  # Direct content  
            "engines": {
                "kinematics": {
                    "engine": "test.module.TestEngine",
                    "class_id": "test_id"
                }
            }
        }
        
        status = cfl.loadConfigs(configs)
        assert status.status == tss_constants.StatusFlags.SUCCESS
        assert cfl.general_config == configs["general"]
        assert cfl.skill_library_config == configs["library"]
        assert cfl.robot_structure_config == configs["robot_structure"]
        assert cfl.envg_config == configs["engines"]
        
    def test_expand_robot_structure_config_missing_field(self):
        """Test expand robot structure config with missing field."""
        cfl = config_loader.ConfigLoader()
        configs = {"general": {}}
        
        status = cfl.expandRobotStructureConfig(configs)
        assert status.status == tss_constants.StatusFlags.FAILED
        assert "robot_structure" in status.message
        
    def test_expand_robot_structure_config_file_not_found(self):
        """Test expand robot structure config with non-existent file."""
        cfl = config_loader.ConfigLoader()
        configs = {"robot_structure": "/non/existent/file.json"}
        
        # This should fail when trying to open the file
        with pytest.raises(FileNotFoundError):
            cfl.expandRobotStructureConfig(configs)
            
    def test_expand_robot_structure_config_valid_file(self):
        """Test expand robot structure config with valid file."""
        # Create a temporary JSON file
        robot_config = {"robot_structure": {"robots": [{"name": "test_robot"}]}}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(robot_config, f)
            temp_file = f.name
            
        try:
            cfl = config_loader.ConfigLoader()
            configs = {"robot_structure": temp_file}
            
            status = cfl.expandRobotStructureConfig(configs)
            assert status.status == tss_constants.StatusFlags.SUCCESS
            assert cfl.robot_structure_config == robot_config["robot_structure"]
        finally:
            os.unlink(temp_file)
            
    def test_expand_skill_library_config_missing_field(self):
        """Test expand skill library config with missing field."""
        cfl = config_loader.ConfigLoader()
        configs = {"general": {}}
        
        status = cfl.expandSkillLibraryConfig(configs)
        assert status.status == tss_constants.StatusFlags.FAILED
        assert "library" in status.message