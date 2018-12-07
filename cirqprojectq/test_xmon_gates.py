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
else:
    from cirq.protocols.unitary import unitary

@pytest.mark.parametrize("half_turns", [-1.5, -1., -.5, 0, 0.25, 0.3, 1., 1.5, 2.])
def test_expz_matrix(half_turns):
    if (version[0] == 0 and version[1] <= 3):
        nptest.assert_array_almost_equal(xmon_gates.ExpZGate(half_turns=half_turns).matrix,
                                google.ExpZGate(half_turns=half_turns).matrix())
    else:
        nptest.assert_array_almost_equal(xmon_gates.ExpZGate(half_turns=half_turns).matrix,
                                unitary(ops.ZPowGate(exponent=half_turns,
                                                     global_shift=half_turns)))


@pytest.mark.parametrize("half_turns, axis_half_turns",
                         list(itertools.product([-1.5, -1., -.5, 0, 0.25, 0.3, 1., 1.5, 2.],
                                                [-1.5, -1., -.5, 0, 0.25, 0.3, 1., 1.5, 2.])))
def test_expw_matrix(half_turns, axis_half_turns):
    m1 = xmon_gates.ExpWGate(half_turns=half_turns,
                                axis_half_turns=axis_half_turns).matrix
    if (version[0] == 0 and version[1] <= 3):
        m2 = google.ExpWGate(half_turns=half_turns,
                            axis_half_turns=axis_half_turns).matrix()
    else:
         m2 = unitary(ops.PhasedXPowGate(exponent=half_turns,
                            phase_exponent=axis_half_turns))
    nptest.assert_array_almost_equal(m1, m2)


@pytest.mark.parametrize("half_turns", [-1.5, -1., -.5, 0, 0.25, 0.3, 1., 1.5, 2.])
def test_expw_matrix(half_turns):
    if (version[0] == 0 and version[1] <= 3):
        nptest.assert_array_almost_equal(xmon_gates.Exp11Gate(half_turns=half_turns).matrix,
                                google.Exp11Gate(half_turns=half_turns).matrix())
    else:
        nptest.assert_array_almost_equal(xmon_gates.Exp11Gate(half_turns=half_turns).matrix,
                                unitary(ops.CZPowGate(exponent=half_turns)))