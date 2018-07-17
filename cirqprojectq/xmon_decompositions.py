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
This file provides decompositon rules to decompose common gates into Xmon gates.
"""
import numpy as np
from projectq.cengines import DecompositionRule, DecompositionRuleSet
from projectq import ops
from projectq.meta import Control, get_control_count
from . import xmon_gates

all_defined_decomposition_rules = []

def _recognize_rotations(cmd):
    if isinstance(cmd.gate, (ops.Rx, ops.Ry, ops.Rz)) and get_control_count(cmd) == 0:
        return True
    else:
        return False

def _decompose_rotations(cmd):
    """

    """
    qb = cmd.qubits
    eng = cmd.engine
    with Control(eng, cmd.control_qubits):
        if isinstance(cmd.gate, ops.Rx):
            xmon_gates.ExpWGate(half_turns=cmd.gate.angle / np.pi, axis_half_turns=0) | qb
        elif isinstance(cmd.gate, ops.Ry):
            xmon_gates.ExpWGate(half_turns=cmd.gate.angle / np.pi, axis_half_turns=0.5) | qb
        elif isinstance(cmd.gate, ops.Rz):
            xmon_gates.ExpZGate(cmd.gate.angle / np.pi) | qb

for op in [ops.Rx, ops.Ry, ops.Rz]:
    all_defined_decomposition_rules.append(DecompositionRule(op,
                                 _decompose_rotations, _recognize_rotations))

def _recognize_paulis(cmd):
    if isinstance(cmd.gate, (ops.XGate, ops.YGate, ops.ZGate)) and get_control_count(cmd) == 0:
        return True
    else:
        return False

def _decompose_paulis(cmd):
    """

    """
    qb = cmd.qubits
    eng = cmd.engine
    with Control(eng, cmd.control_qubits):
        if isinstance(cmd.gate, ops.XGate):
            xmon_gates.ExpWGate(half_turns=1.0, axis_half_turns=0) | qb
        elif isinstance(cmd.gate, ops.YGate):
            xmon_gates.ExpWGate(half_turns=1.0, axis_half_turns=0.5) | qb
        elif isinstance(cmd.gate, ops.ZGate):
            xmon_gates.ExpZGate(1.0) | qb

for op in [ops.XGate, ops.YGate, ops.ZGate]:
    all_defined_decomposition_rules.append(DecompositionRule(op,
                                 _decompose_paulis, _recognize_paulis))

def _recognize_H(cmd):
    if isinstance(cmd.gate, ops.HGate) and get_control_count(cmd) == 0:
        return True
    else:
        return False

def _decompose_H(cmd):
    """

    """
    qb = cmd.qubits
    eng = cmd.engine
    with Control(eng, cmd.control_qubits):
        xmon_gates.ExpWGate(half_turns=.5, axis_half_turns=.5) | qb
        xmon_gates.ExpZGate(half_turns=1.) | qb

all_defined_decomposition_rules.append(DecompositionRule(ops.HGate,
                             _decompose_H, _recognize_H))

def _recognize_CNOT(cmd):
    if isinstance(cmd.gate, ops.XGate) and get_control_count(cmd) == 1:
        return True
    else:
        return False

def _decompose_CNOT(cmd):
    """

    """
    qb = cmd.qubits
    ops.H | qb
    xmon_gates.Exp11Gate(half_turns=1.0) | (cmd.control_qubits[0], qb[0])
    ops.H | qb

all_defined_decomposition_rules.append(DecompositionRule(ops.XGate,
                             _decompose_CNOT, _recognize_CNOT))
