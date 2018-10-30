Decompose to Xmon gates and simulate xmon devices
=================================================

Cirqprojectq decomposes arbitrary circuits to xmon gates such that
proejctq can be used to simulate xmon devices.

Important modules are

.. autosummary::

    cirqprojectq.xmon_gates
    cirqprojectq.xmon_decompositions
    cirqprojectq.xmon_setup

In this example we show how to use projectq to decompose a circuit into Xmon native gates.

.. code-block:: python

    import cirqprojectq
    from cirqprojectq.xmon_decompositions import all_defined_decomposition_rules as xmondec

    def is_supported(eng, cmd):
        if isinstance(cmd.gate, projectq.ops.ClassicalInstructionGate):
            # This is required to allow Measure, Allocate, Deallocate, Flush
            return True
        elif isinstance(cmd.gate, cirqprojectq.xmon_gates.XmonGate):
            return True
        else:
            return False

    supported_gate_set_filter = InstructionFilter(is_supported)
    ruleset = projectq.cengines.DecompositionRuleSet(xmondec)
    replacer = projectq.cengines.AutoReplacer(ruleset)
    engine_list = [replacer, supported_gate_set_filter]

    eng = projectq.MainEngine(backend=projectq.backends.CommandPrinter(), engine_list=engine_list)
    qureg = eng.allocate_qureg(2)
    projectq.ops.H | qureg[0]
    projectq.ops.H | qureg[1]
    projectq.ops.C(projectq.ops.X) | (qureg[0], qureg[1])
    eng.flush()

::

    W(0.5, 0.5) | Qureg[0]
    ExpZ(1.0) | Qureg[0]
    W(0.5, 0.5) | Qureg[1]
    ExpZ(1.0) | Qureg[1]
    W(0.5, 0.5) | Qureg[1]
    ExpZ(1.0) | Qureg[1]
    Exp11(1.0) | ( Qureg[0], Qureg[1] )
    W(0.5, 0.5) | Qureg[1]
    ExpZ(1.0) | Qureg[1]

Decomposition rules
-------------------

.. automodule:: cirqprojectq.xmon_decompositions
   :members:
   :private-members:
   :undoc-members:
   :show-inheritance:

Xmon gates
----------

.. automodule:: cirqprojectq.xmon_gates
   :members:
   :undoc-members:
   :show-inheritance:

Xmon setup
----------

.. automodule:: cirqprojectq.xmon_setup
   :members:
   :undoc-members:
   :show-inheritance:
