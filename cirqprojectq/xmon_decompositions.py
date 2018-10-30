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
r"""Provides decompositon rules to decompose common gates into Xmon gates.

The module :mod:`cirqprojectq.xmon_decompositions` provides decomposition rules for
rotation gates (Rx, Ry, Rz), Pauli gates (X, Y, Z), the Hadamard gate and for CNOT
gates into native Xmon gates.
All defined rules can be imported as
:meth:`cirqprojectq.xmon_decompositions.all_defined_decomposition_rules`.

Note:
    The decompositions into xmon gates are correct up to global phases.
    If the module constant CORRECT_PHASES is set to True, ProjectQ global
    phase gates are applied to the affected qubits in order to keep track of
    the correct phase of thq qubit register.
    With :class:`projectq.setups.decompositions.ph2r` these global phase gates
    can be translated to 1-qubit phase gates (R-gate) on control qubits if
    applicable. See example below


::

    ────  C ──────       ────  C ──── R(a) ──
          |         -->       |
      ---------            ---------
    ──|       | ──       ──|       | ────────
    ──| Ph(a) | ──       ──|       | ────────
    ──|       | ──       ──|       | ────────
      ---------            ---------

A full engine list can be generated with :meth:`cirqproejctq.xmon_setup.xmon_engines()`
"""
import numpy as np
from projectq.cengines import DecompositionRule, DecompositionRuleSet
from projectq import ops, cengines, setups
from projectq.meta import Control, get_control_count
from . import xmon_gates

CORRECT_PHASES = False

def _check_phase(angle):
    return CORRECT_PHASES and (np.pi < angle <= 3 * np.pi)

all_defined_decomposition_rules = []

def _recognize_rotations(cmd):
    if isinstance(cmd.gate, (ops.Rx, ops.Ry, ops.Rz)) and get_control_count(cmd) == 0:
        return True
    else:
        return False

def _decompose_rotations(cmd):
    r"""Decompose a rotation gate into xmon gates.

    We define a rotation gate as

    .. math::

        R_i(\alpha) = \exp(-i \frac{\alpha}{2}\sigma_i)

    If :meth:`CORRECT_PHASES` is False the following decompositions will be used:

        ::

            ── Rz(a) ──  -->  ── ExpZ(a / pi) ──

        This corresponds to the following map:

        .. math::

            R_z(\alpha) \to \mathrm{ExpZ}(\alpha/\pi) =
            \begin{cases}
            -R_z(\alpha),&\pi<\alpha\leq3\pi\\
            R_z(\alpha),&\text{else}
            \end{cases}

        ::

            ── Rx(a) ──  -->  ── ExpWGate(a/pi, 1) ──

        This corresponds to the following map:

        .. math::

            R_x(\alpha) \to \mathrm{ExpW}(\alpha/\pi, 0) =
            e^{i\alpha/2}R_x(\alpha)

        ::

            ── Ry(a) ──  -->  ── ExpWGate(a/pi, 1/2) ──

        This corresponds to the following map:

        .. math::

            R_y(\alpha) \to \mathrm{ExpW}(\alpha/\pi, 1/2) =
            e^{i\alpha/2}R_y(\alpha)

    If :meth:`CORRECT_PHASES` is True, the phases are countered by a projectq phase
    gate :class:`ops.Ph` such that the obtained pahse is correct.
    """
    qb = cmd.qubits
    eng = cmd.engine
    with Control(eng, cmd.control_qubits):
        angle = cmd.gate.angle
        phase = _check_phase(angle)
        if isinstance(cmd.gate, ops.Rx):
            xmon_gates.ExpWGate(half_turns=cmd.gate.angle / np.pi, axis_half_turns=0) | qb
            if CORRECT_PHASES:
                ops.Ph(-angle/2) | qb

        elif isinstance(cmd.gate, ops.Ry):
            xmon_gates.ExpWGate(half_turns=cmd.gate.angle / np.pi, axis_half_turns=0.5) | qb
            if CORRECT_PHASES:
                ops.Ph(-angle/2) | qb
        elif isinstance(cmd.gate, ops.Rz):
            xmon_gates.ExpZGate(cmd.gate.angle / np.pi) | qb
            if phase:
                ops.Ph(np.pi) | qb


for op in [ops.Rx, ops.Ry, ops.Rz]:
    all_defined_decomposition_rules.append(DecompositionRule(op,
                                 _decompose_rotations, _recognize_rotations))

def _recognize_paulis(cmd):
    if isinstance(cmd.gate, (ops.XGate, ops.YGate, ops.ZGate)) and get_control_count(cmd) == 0:
        return True
    else:
        return False

def _decompose_paulis(cmd):
    r"""Decompose a Pauli gate into xmon gates.

    If :meth:`CORRECT_PHASES` is False the following decompositions will be used:

        ::

            Z  -->  ── ExpZ(1.0) ──

        This corresponds to the following map:

        .. math::

            Z \to \mathrm{ExpZ}(1) = e^{-i\pi/2}Z

        ::

            ── X ──  -->  ── ExpWGate(1, 0) ──

        This corresponds to the following map:

        .. math::

            X \to \mathrm{ExpW}(1, 0) = X

        ::

            ── Y ──  -->  ── ExpWGate(1, 1/2) ──

        This corresponds to the following map:

        .. math::

            Y \to \mathrm{ExpW}(1, 1/2) = Y

    If :meth:`CORRECT_PHASES` is True, the phases are countered by a projectq phase
    gate :class:`ops.Ph`.
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
            if CORRECT_PHASES:
                ops.Ph(np.pi/2) | qb

for op in [ops.XGate, ops.YGate, ops.ZGate]:
    all_defined_decomposition_rules.append(DecompositionRule(op,
                                 _decompose_paulis, _recognize_paulis))

def _recognize_H(cmd):
    if isinstance(cmd.gate, ops.HGate) and get_control_count(cmd) == 0:
        return True
    else:
        return False

def _decompose_H(cmd):
    r"""Decompose a Hadamard gate into xmon gates.

    .. include:: <isoamsa.txt>

    If :meth:`CORRECT_PHASES` is False the following decompositions will be used:

        ::

            ── H ──  -->  ── ExpW(1/2, 1/2) ── ExpZ(1) ──

        This corresponds to the following map:

        .. math::

            H \to e^{-i\pi/4}H

    If :meth:`CORRECT_PHASES` is True, the phases are countered by a projectq phase
    gate :class:`ops.Ph`.
    """
    qb = cmd.qubits
    eng = cmd.engine
    with Control(eng, cmd.control_qubits):
        #TODO: I added a minus! Check please!
        xmon_gates.ExpWGate(half_turns=.5, axis_half_turns=.5) | qb
        xmon_gates.ExpZGate(half_turns=1.) | qb
        if CORRECT_PHASES:
            ops.Ph(np.pi/4) | qb

all_defined_decomposition_rules.append(DecompositionRule(ops.HGate,
                             _decompose_H, _recognize_H))

def _recognize_CNOT(cmd):
    if isinstance(cmd.gate, ops.XGate) and get_control_count(cmd) == 1:
        return True
    else:
        return False

def _decompose_CNOT(cmd):
    r"""Decompose a CNOT gate into two Hadamards and an Exp11Gate.

    Uses the following decomposition

    ::

        ── C ──         ───────    @     ───────
           |     -->               |
        ── X ──         ── H ── Exp11(1) ── H ──

   This corresponds to the following map:

    .. math::

        \mathrm{CNOT} \to \mathrm{CNOT}


    Warning:
        The Hadamard gates are correct Hamard gates! They have no wrong phases.
        However, in a second decomposition step these gates will each yield
        a phase of :math:`\exp(-i\pi/4)` if CORRECT_PHASES is False! In this case, the
        final map will be :math:`\mathrm{CNOT}\to\exp(-i\pi/4)\mathrm{CNOT}`

    """
    qb = cmd.qubits
    ops.H | qb
    xmon_gates.Exp11Gate(half_turns=1.0) | (cmd.control_qubits[0], qb[0])
    ops.H | qb

all_defined_decomposition_rules.append(DecompositionRule(ops.XGate,
                             _decompose_CNOT, _recognize_CNOT))


def _recognize_SWAP(cmd):
    if isinstance(cmd.gate, ops.SwapGate):
        return True
    else:
        return False

def _decompose_SWAP(cmd):
    """
    TODO
    """
    qb = cmd.qubits
    xmon_gates.ExpW(.5, .5) | qb[0]
    xmon_gates.ExpW(.5, 0) | qb[1]
    # xmon_gates.Exp11Gate(half_turns=1.0) | (cmd.control_qubits[0], qb[0])
    xmon_gates.Exp11Gate(half_turns=1.0) | (qb[0], qb[1])
    xmon_gates.ExpW(-.5, .5) | qb[0]
    xmon_gates.ExpW(-.5, 0) | qb[1]
    xmon_gates.Exp11Gate(half_turns=1.0) | (qb[0], qb[1])
    # xmon_gates.Exp11Gate(half_turns=1.0) | (cmd.control_qubits[0], qb[0])
    xmon_gates.ExpW(.5, .5) | qb[0]
    xmon_gates.ExpW(.5, 0) | qb[1]
    xmon_gates.Exp11Gate(half_turns=1.0) | (qb[0], qb[1])
    # xmon_gates.Exp11Gate(half_turns=1.0) | (cmd.control_qubits[0], qb[0])
    xmon_gates.ExpZGate(.5) | qb[0]
    xmon_gates.ExpZGate(-.5) | qb[1]

all_defined_decomposition_rules.append(DecompositionRule(ops.SwapGate,
                             _decompose_SWAP, _recognize_SWAP))
