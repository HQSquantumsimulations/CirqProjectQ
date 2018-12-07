# Copyright 2018 Heisenberg Quantum Simulations
# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This module provides translation rules from Xmon gates in Projectq to Xmon gates
in Cirq.
"""
import cirq
version = [int(cirq.__version__[0]), int(cirq.__version__[2])]
assert(version[0] == 0 and version[1] <= 3)
import cmath
from projectq.meta import get_control_count
from . import xmon_gates
from ._rules_pq_to_cirq import Ruleset_pq_to_cirq as Ruleset
from ._rules_pq_to_cirq import Rule_pq_to_cirq as Rule
from cirq.google import xmon_gates as cxmon
from cirq import ops as cop
def _expWGate(cmd, mapping, qubits):
    """
    Translate a ExpW gate into a Cirq gate.

    Args:
        - cmd (:class:`projectq.ops.Command`) - a projectq command instance
        - mapping (:class:`dict`) - a dictionary of qubit mappings
        - qubits (list of :class:cirq.QubitID`) - cirq qubits

    Returns:
        - :class:`cirq.Operation`
    """
    qb_pos = [mapping[qb.id] for qr in cmd.qubits for qb in qr]
    assert len(qb_pos)==1
    cirqGate = cxmon.ExpWGate(half_turns=cmd.gate.angle / cmath.pi, axis_half_turns=cmd.gate.axis_angle / cmath.pi)
    if get_control_count(cmd) > 0:
        ctrl_pos = [mapping[qb.id] for qb in cmd.control_qubits]
        return cop.ControlledGate(cirqGate)(*[qubits[c] for c in ctrl_pos+qb_pos])
    else:
        return cirqGate(*[qubits[idx] for idx in qb_pos])

def _expZGate(cmd, mapping, qubits):
    """
    Translate a ExpZ gate into a Cirq gate.

    Args:
        - cmd (:class:`projectq.ops.Command`) - a projectq command instance
        - mapping (:class:`dict`) - a dictionary of qubit mappings
        - qubits (list of :class:cirq.QubitID`) - cirq qubits

    Returns:
        - :class:`cirq.Operation`
    """
    qb_pos = [mapping[qb.id] for qr in cmd.qubits for qb in qr]
    assert len(qb_pos)==1
    cirqGate = cxmon.ExpZGate(half_turns=cmd.gate.angle / cmath.pi)
    if get_control_count(cmd) > 0:
        ctrl_pos = [mapping[qb.id] for qb in cmd.control_qubits]
        return cop.ControlledGate(cirqGate)(*[qubits[c] for c in ctrl_pos+qb_pos])
    else:
        return cirqGate(*[qubits[idx] for idx in qb_pos])

def _exp11Gate(cmd, mapping, qubits):
    """
    Translate a ExpW gate into a Cirq gate.

    Args:
        - cmd (:class:`projectq.ops.Command`) - a projectq command instance
        - mapping (:class:`dict`) - a dictionary of qubit mappings
        - qubits (list of :class:cirq.QubitID`) - cirq qubits

    Returns:
        - :class:`cirq.Operation`
    """
    qb_pos = [mapping[qb.id] for qr in cmd.qubits for qb in qr]
    assert len(qb_pos)==2
    cirqGate = cxmon.Exp11Gate(half_turns=cmd.gate.angle / cmath.pi)
    return cirqGate(*[qubits[idx] for idx in qb_pos])

EXP_W = Rule([xmon_gates.ExpWGate], _expWGate)
EXP_Z = Rule([xmon_gates.ExpZGate], _expZGate)
EXP_11 = Rule([xmon_gates.Exp11Gate], _exp11Gate)
ALL_RULES = [EXP_W, EXP_Z, EXP_11]
xmon_gates_ruleset = Ruleset(rules = [EXP_W, EXP_Z, EXP_11])