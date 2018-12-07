import pytest
import numpy as np
import itertools
from numpy import testing as nptest
from cirqprojectq import xmon_gates
import cirq
from cirq import ops
version = [int(cirq.__version__[0]), int(cirq.__version__[2])]
if (version[0] == 0 and version[1] <= 3):
    from cirq import google

@pytest.mark.parametrize("half_turns", [-1.5, -1., -.5, 0, 0.25, 0.3, 1., 1.5, 2.])
def test_expz_matrix(half_turns):
    if (version[0] == 0 and version[1] <= 3):
        nptest.assert_array_almost_equal(xmon_gates.ExpZGate(half_turns=half_turns).matrix,
                                google.ExpZGate(half_turns=half_turns).matrix())
    else:
        pass

@pytest.mark.parametrize("half_turns, axis_half_turns",
                         list(itertools.product([-1.5, -1., -.5, 0, 0.25, 0.3, 1., 1.5, 2.],
                                                [-1.5, -1., -.5, 0, 0.25, 0.3, 1., 1.5, 2.])))
def test_expw_matrix(half_turns, axis_half_turns):
    if (version[0] == 0 and version[1] <= 3):
        m1 = xmon_gates.ExpWGate(half_turns=half_turns,
                                axis_half_turns=axis_half_turns).matrix
        m2 = google.ExpWGate(half_turns=half_turns,
                            axis_half_turns=axis_half_turns).matrix()
        nptest.assert_array_almost_equal(m1, m2)
    else:
        pass

@pytest.mark.parametrize("half_turns", [-1.5, -1., -.5, 0, 0.25, 0.3, 1., 1.5, 2.])
def test_expw_matrix(half_turns):
    if (version[0] == 0 and version[1] <= 3):
        nptest.assert_array_almost_equal(xmon_gates.Exp11Gate(half_turns=half_turns).matrix,
                                google.Exp11Gate(half_turns=half_turns).matrix())
    else:
        pass