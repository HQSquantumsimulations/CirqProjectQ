import pytest
import numpy as np
import itertools
from numpy import testing as nptest
from cirqprojectq import xmon_gates
from cirq import ops, google

@pytest.mark.parametrize("half_turns", [-1.5, -1., -.5, 0, 0.25, 0.3, 1., 1.5, 2.])
def test_expz_matrix(half_turns):
    nptest.assert_array_almost_equal(xmon_gates.ExpZGate(half_turns=half_turns).matrix,
                              google.ExpZGate(half_turns=half_turns).matrix())

@pytest.mark.parametrize("half_turns, axis_half_turns",
                         list(itertools.product([-1.5, -1., -.5, 0, 0.25, 0.3, 1., 1.5, 2.],
                                                [-1.5, -1., -.5, 0, 0.25, 0.3, 1., 1.5, 2.])))
def test_expw_matrix(half_turns, axis_half_turns):
    m1 = xmon_gates.ExpWGate(half_turns=half_turns,
                             axis_half_turns=axis_half_turns).matrix
    m2 = google.ExpWGate(half_turns=half_turns,
                         axis_half_turns=axis_half_turns).matrix()
    nptest.assert_array_almost_equal(m1, m2)

@pytest.mark.parametrize("half_turns", [-1.5, -1., -.5, 0, 0.25, 0.3, 1., 1.5, 2.])
def test_expw_matrix(half_turns):
    nptest.assert_array_almost_equal(xmon_gates.Exp11Gate(half_turns=half_turns).matrix,
                              google.Exp11Gate(half_turns=half_turns).matrix())