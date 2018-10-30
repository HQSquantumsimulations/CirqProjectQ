Convert to cirq
===============

For example, we can translate a simple quantum algorithm to Cirq and print the final cirq.Circuit:

.. code-block:: python

    import cirq
    import numpy as np
    from cirqprojectq.circ_engine import CIRQ
    import projectq
    qubits = [cirq.google.XmonQubit(0, i) for i in range(2)]
    CIRQ = CIRQ(qubits=qubits)
    eng = projectq.MainEngine(backend=CIRQ)
    qureg = eng.allocate_qureg(len(qubits))
    eng.flush()
    projectq.ops.Rx(0.25 * np.pi) | qureg[0]
    projectq.ops.Ry(0.5 * np.pi) | qureg[1]
    projectq.ops.Rz(0.5 * np.pi) | qureg[0]
    projectq.ops.H | qureg[1]
    projectq.ops.C(projectq.ops.X) | (qureg[0], qureg[1])
    projectq.ops.Z | qureg[0]
    projectq.ops.X | qureg[0]
    projectq.ops.Y | qureg[0]
    eng.flush()
    print(CIRQ.circuit)

::

    (0, 0): ───X^0.25───Z^0.5───────@───Z───X───Y───
                                │
    (0, 1): ────────────Y^0.5───H───X───────────────

The backend
-----------

.. automodule:: cirqprojectq.circ_engine
   :members:
   :undoc-members:
   :show-inheritance:

Translation rules
-----------------

.. automodule:: cirqprojectq._rules_pq_to_cirq
   :members:
   :undoc-members:
   :show-inheritance:

Rules for common gates
++++++++++++++++++++++

.. automodule:: cirqprojectq.common_rules
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

Rules for xmon gates
++++++++++++++++++++

.. automodule:: cirqprojectq.xmon_rules
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
