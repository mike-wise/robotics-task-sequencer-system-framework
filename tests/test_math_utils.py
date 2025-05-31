# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# --------------------------------------------------------------------------------------------

"""Tests for tasqsym.core.common.math module."""

import pytest
import sys
import os

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import tasqsym.core.common.math as tss_math
import tasqsym.core.common.structs as tss_structs


class TestQuaternionMath:
    """Test quaternion mathematical operations."""
    
    def test_quaternion_multiply_identity(self):
        """Test quaternion multiplication with identity quaternion."""
        q1 = tss_structs.Quaternion(0, 0, 0, 1)  # identity quaternion
        q2 = tss_structs.Quaternion(1, 2, 3, 4)
        
        result = tss_math.quaternion_multiply(q1, q2)
        
        assert result[0] == 1
        assert result[1] == 2 
        assert result[2] == 3
        assert result[3] == 4
        
    def test_quaternion_multiply_general(self):
        """Test general quaternion multiplication."""
        q1 = tss_structs.Quaternion(1, 0, 0, 0)
        q2 = tss_structs.Quaternion(0, 1, 0, 0)
        
        result = tss_math.quaternion_multiply(q1, q2)
        
        # i * j = k
        assert result[0] == 0  # x
        assert result[1] == 0  # y
        assert result[2] == 1  # z
        assert result[3] == 0  # w
        
    def test_quaternion_conjugate(self):
        """Test quaternion conjugate calculation."""
        q = tss_structs.Quaternion(1, 2, 3, 4)
        
        result = tss_math.quaternion_conjugate(q)
        
        assert result[0] == -1
        assert result[1] == -2
        assert result[2] == -3
        assert result[3] == 4
        
    def test_quaternion_conjugate_identity(self):
        """Test conjugate of identity quaternion."""
        q = tss_structs.Quaternion(0, 0, 0, 1)
        
        result = tss_math.quaternion_conjugate(q)
        
        assert result[0] == 0
        assert result[1] == 0
        assert result[2] == 0
        assert result[3] == 1
        
    def test_quat_mul_vec_identity(self):
        """Test quaternion-vector multiplication with identity quaternion."""
        q = tss_structs.Quaternion(0, 0, 0, 1)  # identity quaternion
        v = tss_structs.Point(1, 2, 3)
        
        result = tss_math.quat_mul_vec(q, v)
        
        # Identity quaternion should not change the vector
        assert abs(result[0] - 1.0) < 1e-10
        assert abs(result[1] - 2.0) < 1e-10
        assert abs(result[2] - 3.0) < 1e-10
        
    def test_quat_mul_vec_rotation(self):
        """Test quaternion-vector multiplication for a 90-degree rotation around z-axis."""
        import math
        # 90-degree rotation around z-axis
        q = tss_structs.Quaternion(0, 0, math.sin(math.pi/4), math.cos(math.pi/4))
        v = tss_structs.Point(1, 0, 0)  # unit vector along x-axis
        
        result = tss_math.quat_mul_vec(q, v)
        
        # Should rotate x-axis to y-axis
        assert abs(result[0] - 0.0) < 1e-10
        assert abs(result[1] - 1.0) < 1e-10
        assert abs(result[2] - 0.0) < 1e-10


class TestQuaternionUtilities:
    """Test additional quaternion utility functions."""
    
    def test_quaternion_slerp_different_quaternions(self):
        """Test spherical linear interpolation with different quaternions."""
        q1 = tss_structs.Quaternion(0, 0, 0, 1)  # identity
        q2 = tss_structs.Quaternion(0, 0, 0.707, 0.707)  # 90 degree rotation around z
        
        result = tss_math.quaternion_slerp(q1, q2, 0.5)
        
        # Result should be between q1 and q2
        assert isinstance(result[0], (int, float))
        assert isinstance(result[1], (int, float))
        assert isinstance(result[2], (int, float))
        assert isinstance(result[3], (int, float))
        
    def test_quaternion_slerp_interpolation(self):
        """Test spherical linear interpolation between different quaternions."""
        q1 = tss_structs.Quaternion(0, 0, 0, 1)  # identity
        q2 = tss_structs.Quaternion(1, 0, 0, 0)  # 180 degree rotation around x
        
        # At t=0, should return q1
        result_0 = tss_math.quaternion_slerp(q1, q2, 0.0)
        assert abs(result_0[3] - 1.0) < 1e-6
        
        # At t=1, should return q2 (or close to it)
        result_1 = tss_math.quaternion_slerp(q1, q2, 1.0)
        assert abs(result_1[0]) > 0.5  # Should have significant x component
        
    def test_quaternion_matrix_identity(self):
        """Test rotation matrix for identity quaternion."""
        q = tss_structs.Quaternion(0, 0, 0, 1)
        
        matrix = tss_math.quaternion_matrix(q)
        
        # Should be identity matrix
        expected = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        for i in range(3):
            for j in range(3):
                assert abs(matrix[i][j] - expected[i][j]) < 1e-10
                
    def test_quaternion_matrix_x_rotation(self):
        """Test rotation matrix for 90-degree rotation around x-axis."""
        import math
        # 90-degree rotation around x-axis
        q = tss_structs.Quaternion(math.sin(math.pi/4), 0, 0, math.cos(math.pi/4))
        
        matrix = tss_math.quaternion_matrix(q)
        
        # Check that y-axis rotates to z-axis
        assert abs(matrix[0][0] - 1.0) < 1e-10  # x unchanged
        assert abs(matrix[1][2] - (-1.0)) < 1e-10  # y -> -z
        assert abs(matrix[2][1] - 1.0) < 1e-10   # z -> y


class TestEulerConversions:
    """Test Euler angle conversion functions."""
    
    def test_quaternion_from_euler_zero(self):
        """Test quaternion from zero Euler angles."""
        q = tss_math.quaternion_from_euler(0, 0, 0)
        
        # Should be identity quaternion
        assert abs(q[0]) < 1e-10
        assert abs(q[1]) < 1e-10
        assert abs(q[2]) < 1e-10
        assert abs(q[3] - 1.0) < 1e-10
        
    def test_quaternion_from_euler_x_rotation(self):
        """Test quaternion from 90-degree rotation around x-axis."""
        import math
        q = tss_math.quaternion_from_euler(math.pi/2, 0, 0)
        
        # Should have significant x component
        assert abs(q[0] - math.sin(math.pi/4)) < 1e-10
        assert abs(q[1]) < 1e-10
        assert abs(q[2]) < 1e-10
        assert abs(q[3] - math.cos(math.pi/4)) < 1e-10
        
    def test_euler_from_matrix_identity(self):
        """Test Euler angles from identity matrix."""
        identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        
        euler = tss_math.euler_from_matrix(identity)
        
        assert abs(euler[0]) < 1e-10
        assert abs(euler[1]) < 1e-10
        assert abs(euler[2]) < 1e-10
        
    def test_euler_from_quaternion_identity(self):
        """Test Euler angles from identity quaternion."""
        q = tss_structs.Quaternion(0, 0, 0, 1)
        
        euler = tss_math.euler_from_quaternion(q)
        
        assert abs(euler[0]) < 1e-10
        assert abs(euler[1]) < 1e-10
        assert abs(euler[2]) < 1e-10
        
    def test_euler_quaternion_roundtrip(self):
        """Test roundtrip conversion between Euler angles and quaternions."""
        import math
        original_x, original_y, original_z = math.pi/6, math.pi/4, math.pi/3
        
        q = tss_math.quaternion_from_euler(original_x, original_y, original_z)
        result_euler = tss_math.euler_from_quaternion(q)
        
        # Allow for some numerical precision issues
        assert abs(original_x - result_euler[0]) < 1e-10
        assert abs(original_y - result_euler[1]) < 1e-10
        assert abs(original_z - result_euler[2]) < 1e-10


class TestDirectionMath:
    """Test direction and angle calculation functions."""
    
    def test_proper_trifunc_clipping(self):
        """Test proper_trifunc clips values to [-1, 1] range."""
        assert tss_math.proper_trifunc(2) == 1
        assert tss_math.proper_trifunc(-2) == -1
        assert tss_math.proper_trifunc(0.5) == 0.5
        assert tss_math.proper_trifunc(-0.5) == -0.5
        assert tss_math.proper_trifunc(1) == 1
        assert tss_math.proper_trifunc(-1) == -1
        
    def test_xyz2polar_unit_vectors(self):
        """Test conversion to polar coordinates for unit vectors."""
        import numpy as np
        import math
        
        # Unit vector along z-axis
        xyz = np.array([0, 0, 1])
        r, theta, phi = tss_math.xyz2polar(xyz)
        
        assert abs(r - 1.0) < 1e-10
        assert abs(theta - 0.0) < 1e-10  # theta should be 0 for z-axis
        
        # Unit vector along x-axis
        xyz = np.array([1, 0, 0])
        r, theta, phi = tss_math.xyz2polar(xyz)
        
        assert abs(r - 1.0) < 1e-10
        assert abs(theta - math.pi/2) < 1e-10  # theta should be pi/2 for x-axis
        assert abs(phi - 0.0) < 1e-10  # phi should be 0 for x-axis
        
    def test_xyz2dist_ang_unit_vectors(self):
        """Test conversion to distance-angle coordinates for unit vectors."""
        import numpy as np
        import math
        
        # Unit vector along z-axis
        xyz = np.array([0, 0, 1])
        r, theta, phi = tss_math.xyz2dist_ang(xyz)
        
        assert abs(r - 1.0) < 1e-10
        assert abs(theta - math.pi/2) < 1e-10  # theta should be pi/2 for z-axis
        
        # Unit vector in xy-plane
        xyz = np.array([1, 0, 0])
        r, theta, phi = tss_math.xyz2dist_ang(xyz)
        
        assert abs(r - 1.0) < 1e-10
        assert abs(theta - 0.0) < 1e-10  # theta should be 0 for xy-plane
        assert abs(phi - 0.0) < 1e-10  # phi should be 0 for x-axis