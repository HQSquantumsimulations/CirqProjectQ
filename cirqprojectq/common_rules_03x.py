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
This module provides translation rules from Projectq to Cirq for some common
gates.
"""
import cirq
version = [int(cirq.__version__[0]), int(cirq.__version__[2])]
assert(version[0] == 0 and version[1] <= 3)
import cmath
import cirq, projectq
from projectq import ops as pqo
from projectq.meta import get_control_count
from projectq.cengines import BasicEngine, DecompositionRule, DecompositionRuleSet
from cirq import ops as cop
KNOWN_SINGLE_QUBIT_GATES = {pqo.XGate: cop.X,
               pqo.YGate: cop.Y,
               pqo.ZGate: cop.Z,
               pqo.Rx: cop.RotXGate,
               pqo.Ry: cop.RotYGate,
               pqo.Rz: cop.RotZGate,
               pqo.HGate: cop.H,
               pqo.SGate: cop.S
               }

from ._rules_pq_to_cirq import Ruleset_pq_to_cirq as Ruleset
from ._rules_pq_to_cirq import Rule_pq_to_cirq as Rule


def _rx_ry_rz(cmd, mapping, qubits):
    """
    Translate a rotation gate into a Cirq roation (phase) gate.

    Global phase difference betwee proejctq rotation gate and cirq phase gate
    is dropped.

    Args:
        cmd (:class:`projectq.ops.Command`): a projectq command instance
        mapping (:class:`dict`): a dictionary of qubit mappings
        qubits (list of :class:cirq.QubitID`): cirq qubits

    Returns:
        :class:`cirq.Operation`
    """
    gates = {pqo.Rx: cop.RotXGate,
               pqo.Ry: cop.RotYGate,
               pqo.Rz: cop.RotZGate}
    qb_pos = [mapping[qb.id] for qr in cmd.qubits for qb in qr]
    assert len(qb_pos)==1
    cirqGate = gates[type(cmd.gate)](half_turns=cmd.gate.angle / cmath.pi)
    if get_control_count(cmd) > 0:
        ctrl_pos = [mapping[qb.id] for qb in cmd.control_qubits]
        return cop.ControlledGate(cirqGate)(*[qubits[c] for c in ctrl_pos+qb_pos])
    else:
        return cirqGate(*[qubits[idx] for idx in qb_pos])

def _pauli_gates(cmd, mapping, qubits):
    """
    Translate a Pauli (x, Y, Z) gate into a Cirq gate.

    Args:
        cmd (:class:`projectq.ops.Command`): a projectq command instance
        mapping (:class:`dict`): a dictionary of qubit mappings
        qubits (list of :class:cirq.QubitID`): cirq qubits

    Returns:
        :class:`cirq.Operation`
    """
    gates = {pqo.XGate: cop.X,
               pqo.YGate: cop.Y,
               pqo.ZGate: cop.Z}
    qb_pos = [mapping[qb.id] for qr in cmd.qubits for qb in qr]
    assert len(qb_pos)==1
    cirqGate = gates[type(cmd.gate)]
    if get_control_count(cmd) > 0:
        ctrl_pos = [mapping[qb.id] for qb in cmd.control_qubits]
        return cop.ControlledGate(cirqGate)(*[qubits[c] for c in ctrl_pos+qb_pos])
    else:
        return cirqGate(*[qubits[idx] for idx in qb_pos])

def _h_s_gate(cmd, mapping, qubits):
    """
    Translate a Hadamard or S-gate into a Cirq gate.

    Args:
        cmd (:class:`projectq.ops.Command`): a projectq command instance
        mapping (:class:`dict`): a dictionary of qubit mappings
        qubits (list of :class:cirq.QubitID`): cirq qubits

    Returns:
        :class:`cirq.Operation`
    """
    gates = {pqo.HGate: cop.H,
               pqo.SGate: cop.S}
    qb_pos = [mapping[qb.id] for qr in cmd.qubits for qb in qr]
    assert len(qb_pos)==1
    cirqGate = gates[type(cmd.gate)]
    if get_control_count(cmd) > 0:
        ctrl_pos = [mapping[qb.id] for qb in cmd.control_qubits]
        return cop.ControlledGate(cirqGate)(*[qubits[c] for c in ctrl_pos+qb_pos])
    else:
        return cirqGate(*[qubits[idx] for idx in qb_pos])

def _gates_with_known_matrix(cmd, mapping, qubits):
    """
    Translate a single qubit gate with known matrix into a Cirq gate.

    Args:
        cmd (:class:`projectq.ops.Command`): a projectq command instance
        mapping (:class:`dict`): a dictionary of qubit mappings
        qubits (list of :class:cirq.QubitID`): cirq qubits

    Returns:
        :class:`cirq.Operation`
    """
    gate = cmd.gate
    if len(get_control_count(cmd)) == 0 and hasattr(gate, 'matrix'):
            qb_pos = [mapping[qb.id] for qr in cmd.qubits for qb in qr]
            return cop.matrix_gates.SingleQubitMatrixGate(matrix=gate.matrix)(
                    *[qubits[q] for q in qb_pos])
    elif len(get_control_count(cmd)) > 0 and hasattr(gate, 'matrix'):
        qb_pos = [mapping[qb.id] for qr in cmd.qubits for qb in qr]
        ctrl_pos = [mapping[qb.id] for qb in cmd.control_qubits]
        cirqGate = cop.matrix_gates.SingleQubitMatrixGate(matrix=gate.matrix)
        return cop.ControlledGate(cirqGate)(*[qubits[q] for q in qb_pos+ctrl_pos])


Rx_Ry_Rz = Rule([pqo.Rx, pqo.Ry, pqo.Rz], _rx_ry_rz)
Paulis = Rule([pqo.XGate, pqo.YGate, pqo.ZGate], _pauli_gates)
H_S = Rule([pqo.HGate, pqo.SGate], _h_s_gate)
Known_Matrix = Rule([pqo.BasicGate], _gates_with_known_matrix)

common_gates_ruleset = Ruleset(rules = [Rx_Ry_Rz, Paulis, H_S, Known_Matrix])