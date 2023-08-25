import unittest
import pynibs
import numpy as np
from scipy.spatial.transform import Rotation as R


class TestUtilsRotationsbases2rotmat(unittest.TestCase):
    mat = np.array(([1., 0., 0., 0.],
                    [0., 1., 0., 0.],
                    [0., 0., 1., 0.],
                    [10., 20., 30., 1.])).T

    def test_bases2rotmat(self):
        v1 = np.array(([0, 0, 1], [0, 1, 0], [1, 0, 0]))
        v2 = np.array(([1, 0, 0], [0, 1, 0], [0, 0, 1]))
        res = R.from_matrix(pynibs.bases2rotmat(v1, v2)).as_euler('xyz', degrees=True)
        assert (res == np.array([180., 0., 180.])).all()

    def test_roatate_matsimnibs_euler_no_rot(self):
        for axis in ['x', 'y', 'z']:
            assert (self.mat == pynibs.roatate_matsimnibs_euler(axis=axis, angle=0, matsimnibs=self.mat,
                                                                metric='rad')).all()
            assert (self.mat == pynibs.roatate_matsimnibs_euler(axis=axis, angle=0, matsimnibs=self.mat,
                                                                metric='deg')).all()

            assert np.allclose(
                pynibs.roatate_matsimnibs_euler(axis=axis, angle=2 * np.pi, matsimnibs=self.mat, metric='rad'),
                self.mat)
            assert np.allclose(pynibs.roatate_matsimnibs_euler(axis=axis, angle=360, matsimnibs=self.mat, metric='deg'),
                               self.mat)

    def test_roatate_matsimnibs_euler_180(self):
        assert np.allclose(pynibs.roatate_matsimnibs_euler(axis='x', angle=np.pi, matsimnibs=self.mat, metric='rad'),
                           np.array([[1., 0., 0., 10.],
                                     [0., -1., -0., 20.],
                                     [0., 0., -1., 30.],
                                     [0., 0., 0., 1.]])
                           )
        assert np.allclose(pynibs.roatate_matsimnibs_euler(axis='y', angle=np.pi, matsimnibs=self.mat, metric='rad'),
                           np.array([[-1., 0., 0., 10.],
                                     [0., 1., 0., 20.],
                                     [-0., 0., -1., 30.],
                                     [0., 0., 0., 1.]]))
        assert np.allclose(pynibs.roatate_matsimnibs_euler(axis='z', angle=np.pi, matsimnibs=self.mat, metric='rad'),
                           np.array([[-1., -0., 0., 10.],
                                     [0., -1., 0., 20.],
                                     [0., 0., 1., 30.],
                                     [0., 0., 0., 1.]]))
