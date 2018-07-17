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
This file provides Xmon gates for projectq.
"""
from projectq.ops import BasicGate, BasicPhaseGate, H, Rx, Rz
import numpy as np
import cmath

#TODO: implement merge and inverse for all gates

class XmonGate(BasicGate):
    def __init__(self):
        r"""
        Abstract XmonGate class to distinguish mon from regular proejctq gates.
        """
        BasicGate.__init__(self)

class PhZGate(BasicPhaseGate):
    r"""
    A Z-Phase-Gate corresponding to :class:`cirq.ops.RotZGate`

    .. math::
        \begin{pmatrix}1&0\\0$\exp(i\varphi)\end{pmatrix}

    Args:
        - angle (float) - the angle of rotation.
    """

    @property
    def matrix(self):
        return np.matrix([[1, 0], [0, cmath.exp(-1.0j * self.angle)]])

    def __str__(self):
        return "PhZ"

class PhXGate(BasicPhaseGate):
    r"""
    A X-Phase-Gate corresponding to :class:`cirq.ops.RotZGate`

    .. math::
        H\cdot\begin{pmatrix}1&0\\0$\exp(i\varphi)\end{pmatrix}\cdot H

    Args:
        - angle (float) - the angle of rotation.
    """

    @property
    def matrix(self):
        return H.matrix.dot(np.matrix([[1, 0], [0, cmath.exp(-1.0j * self.angle)]])).dot(H.matrix)

    def __str__(self):
        return "PhX"

class PhYGate(BasicPhaseGate,
              XmonGate):
    r"""
    A Y-Phase-Gate corresponding to :class:`cirq.ops.RotZGate`

    .. math::
        R_x(\pi/2)\cdot\begin{pmatrix}1&0\\0$\exp(i\varphi)\end{pmatrix}\cdot R_x(-\pi/2)

    Args:
        - angle (float) - the angle of rotation.
    """
    @property
    def matrix(self):
        phi = - cmath.pi / 2.
        return Rx(phi).matrix.dot(np.matrix([[1, 0], [0, cmath.exp(-1.0j * self.angle)]])).dot(Rx(-phi).matrix)

    def __str__(self):
        return "PhY"

class Exp11Gate(XmonGate):
    r"""
    Two-qubit rotation around the :math:`|11\rangle` axis.

    Args:
        - half_turns (float) - angel of rotation in units of :math:`\pi`.
    """
    def __init__(self, half_turns):
        BasicGate.__init__(self)
        self.angle = half_turns * np.pi
        self.interchangeable_qubit_indices = [[0, 1]]

    @property
    def matrix(self):
        return np.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0],
                          [0, 0, 0, cmath.exp(1.0j * self.angle)]])

    def __str__(self):
        return "Exp11({})".format(np.round(self.angle/np.pi,2))

class ExpWGate(XmonGate):
    r"""
    Singlq qubit rotation around an axis in the X-Y plane defined by the angle
    :math:`\theta` between X- and Y..

    Args:
        - half_turns (float) - angel of rotation in units of :math:`\pi`.
        - axis_half_turns (float) - axis between X and Y in units of :math:`\pi`.
    """
    def __init__(self, half_turns, axis_half_turns=0):
        BasicGate.__init__(self)
        self.angle = half_turns * cmath.pi
        self.axis_angle = axis_half_turns * cmath.pi

    @property
    def matrix(self):
        phase = np.matrix([[1., 0],
                           [0, cmath.exp(1.0j * self.axis_angle)]])
        c = cmath.exp(1j * self.angle)
        rot = np.array([[1 + c, 1 - c], [1 - c, 1 + c]]) / 2
        return phase.dot(rot).dot(np.conj(phase))

    def __str__(self):
        return "W({}, {})".format(np.round(self.angle/np.pi,2), np.round(self.axis_angle/np.pi, 2))

class ExpZGate(Rz, XmonGate):
    r"""
    A rotation gate around the Z-axis.

    .. math::
        \begin{pmatrix}\exp(-i\varphi)&0\\0$\exp(i\varphi/2)\end{pmatrix}

    Args:
        - angle (float) - the angle of rotation.
    """

    def __init__(self, half_turns):
        Rz.__init__(self, half_turns * cmath.pi)

    def __str__(self):
        return "ExpZ({})".format(np.round(self.angle / np.pi,2))
