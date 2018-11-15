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
This module provides Xmon gates for projectq.

Xmon qubits are a specific type of transmon qubit developed by Google.
In the cirq framework xmon specific gates are defined.
This file ports these gates to projectq and allows imulation
of algorithms with xmon qubits. 
"""
from projectq.ops import BasicGate, BasicPhaseGate, H, Rx, Rz, NotMergeable
import numpy as np
import cmath
from cirq import value

#TODO: implement merge and inverse for all gates

class XmonGate(BasicGate):
    def __init__(self):
        r"""
        Abstract XmonGate class to distinguish mon from regular proejctq gates.
        """
        BasicGate.__init__(self)

class Exp11Gate(XmonGate):
    r"""A two-qubit interaction that phases the amplitude of the 11 state.

    This gate implements :math:`\exp(i \pi \varphi |11\rangle\langle 11|)` where :math:`\varphi`
    is half turns.

    As a matrix it reads

    .. math::
        \begin{pmatrix}
        1 & 0 & 0 & 0\\
        0 & 1 & 0 & 0\\
        0 & 0 & 1 & 0\\
        0 & 0 & 0 & \exp(i\varphi \pi)
        \end{pmatrix}

    Warning:
        There is no (-) sign in the definition of the gate.

    Note:
        The half_turn parameter is such that a full turn is the
        identity matrix, in contrast to the single qubit gates, where a full
        turn is minus identity. The single qubit half-turn gates are defined
        so that a full turn corresponds to a rotation on the Bloch sphere of a
        360 degree rotation. For two qubit gates, there isn't a Bloch sphere,
        so the half_turn corresponds to half of a full rotation in U(4).


    Args:
        half_turns (float): angle of rotation in units of :math:`\pi`.
    """
    def __init__(self, half_turns):
        XmonGate.__init__(self)
        self.half_turns = half_turns
        self.interchangeable_qubit_indices = [[0, 1]]

    @property
    def angle(self):
        r"""Rotation angle in rad, :math:`\in(-\pi, \pi]`"""
        return self.half_turns * cmath.pi

    @property
    def half_turns(self):
        r"""Rotation angle in half turns, :math:`\in(-1, 1]`"""
        return self._half_turns

    @half_turns.setter
    def half_turns(self, half_turns):
        self._half_turns = value.chosen_angle_to_canonical_half_turns(half_turns=half_turns,
                                                                      rads=None,
                                                                      degs=None)

    @property
    def matrix(self):
        r"""Gate matrix.

        With :math:`\varphi=\mathrm{half\_turns}` the matrix implemented by the
        Exp11Gate reads as

        .. math::
            \begin{pmatrix}
            1 & 0 & 0 & 0\\
            0 & 1 & 0 & 0\\
            0 & 0 & 1 & 0\\
            0 & 0 & 0 & \exp(i\varphi \pi)
            \end{pmatrix}

        """
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0],
                          [0, 0, 0, cmath.exp(1.0j * self.angle)]])

    def __str__(self):
        return "@({})".format(np.round(self.angle, 2))

    def tex_str(self):
        """
        Returns the class name and the angle as a subscript, i.e.

        .. code-block:: latex

            [CLASSNAME]$_[ANGLE]$
        """
        return "@$_{{{}}}$".format(np.round(self.angle / np.pi, 2))

class ExpWGate(XmonGate):
    r"""A rotation around an axis in the XY plane of the Bloch sphere.



    This gate is a "phased X rotation". Specifically

        ───W(axis)^t─── = ───Z^-axis───X^t───Z^axis───

    This gate is

    .. math::

        \exp(-i * \pi * W(\mathrm{axis\_half\_turn}) * \mathrm{half\_turn} / 2)

    where

    .. math::

        W(\theta) = \cos(\pi \theta) X + \sin(\pi \theta) Y

    Note the half_turn nomenclature here comes from viewing this as a rotation
    on the Bloch sphere. Two half_turns correspond to a rotation in the
    bloch sphere of 360 degrees. Note that this is minus identity, not
    just identity.  Similarly the axis_half_turns refers thinking of rotating
    the Bloch operator, starting with the operator pointing along the X
    direction. An axis_half_turn of 1 corresponds to the operator pointing
    along the -X direction while an axis_half_turn of 0.5 correspond to
    an operator pointing along the Y direction.'

    Contrary to the docstring, cirq implements the gate (:math:`\varphi = \mathrm{half\_turns}`
    and :math:`\theta=\mathrm{axis\_half\_turns}`):

    .. math::

        \exp(i \pi \varphi / 2) \exp(-i \pi W(\theta) \varphi / 2)

    which differs by a global phase :math:`\exp(i \varphi/2)`.

    This class mimics the cir implementation, i.e., the matrix represented by this gate
    reads as

    .. math::
        \exp(i \varphi \pi / 2)\begin{pmatrix}
        \cos(\varphi\pi / 2) & -i \sin(\varphi \pi / 2) exp(-i \theta \pi)\\
        -i \sin(\varphi \pi / 2) \exp(i \theta \pi) & \cos(\varphi \pi / 2)
        \end{pmatrix}

    whih is a rotation around the W-axis and an additional global phase.

    Note:
        This gate corresponds to a phase gate in the basis defined by the W-axis,
        not to a rotation gate.

    Note:
        Restricting half_turns to the rage (-1, 1] corresponds to the full range (0, 2pi]
        for a phase gate, which the ExpW gate in the cirq implementation actually is.

    Note:
        Another convention is to change a positive rotation around a negative axis to a
        negative rotation around a postive axis, i.e., half_turns -> - half_turns
        and axis_half_turns -> axis_half_turns + 1 if axis_half_turns < 0.

    Args:
        half_turns (float): angle of rotation in units of :math:`\pi`.
        axis_half_turns (float): axis between X and Y in units of :math:`\pi`.
    """
    def __init__(self, half_turns, axis_half_turns=0):
        XmonGate.__init__(self)
        self.half_turns = half_turns
        self.axis_half_turns = axis_half_turns
        if (not isinstance(self.axis_half_turns, value.Symbol) and
                not 0 <= self.axis_half_turns < 1):
            # The following code is taken from google to follow the same conventions.
            # I'm not sure if this is correct as it seems to give different matrices.
            # Canonicalize to negative rotation around positive axis.
            self.half_turns = value.canonicalize_half_turns(-self.half_turns)
            self.axis_half_turns = value.canonicalize_half_turns(
                self.axis_half_turns + 1)

    @property
    def axis_angle(self):
        r"""Axis angle in rad, :math:`\in(-\pi, \pi]`"""
        return self._axis_half_turns * cmath.pi

    @property
    def axis_half_turns(self):
        r"""Axis angle in half turns, :math:`\in(-1, 1]`"""
        return self._axis_half_turns

    @axis_half_turns.setter
    def axis_half_turns(self, half_turns):
        val = value.chosen_angle_to_canonical_half_turns(half_turns=half_turns,
                                                         rads=None,
                                                         degs=None)
        self._axis_half_turns = val

    @property
    def angle(self):
        r"""Rotation angle in rad, :math:`\in(-\pi, \pi]`"""
        return self.half_turns * cmath.pi

    @property
    def half_turns(self):
        r"""Rotation angle in half turns, :math:`\in(-1, 1]`"""
        return self._half_turns

    @half_turns.setter
    def half_turns(self, half_turns):
        val = value.chosen_angle_to_canonical_half_turns(half_turns=half_turns,
                                                         rads=None,
                                                         degs=None)
        self._half_turns = val

    @property
    def matrix(self):
        r"""Rotation matrix.

        With :math:`\varphi = \mathrm{half\_turns}` and
        :math:`\theta=\mathrm{axis\_half\_turns}` this gate implements the matrix

        .. math::

            \exp(i \varphi \pi / 2)\begin{pmatrix}
            \cos(\varphi\pi / 2) & -i \sin(\varphi \pi / 2) exp(-i \theta \pi)\\
            -i \sin(\varphi \pi / 2) \exp(i \theta \pi) & \cos(\varphi \pi / 2)
            \end{pmatrix}

        """
        W = np.exp(-1.0j * self.axis_angle)
        c = np.cos(self.angle / 2)
        s = np.sin(self.angle / 2)
        rot = np.array([[c, -1.0j * s * W],
                         [-1.0j * s * np.conj(W), c]])
        return np.exp(.5j * self.angle) * rot
        # phase = np.array([[1., 0],
        #                    [0, cmath.exp(1.0j * self.axis_angle)]])
        # c = cmath.exp(1j * self.angle)
        # rot = np.array([[1 + c, 1 - c], [1 - c, 1 + c]]) / 2
        # return phase.dot(rot).dot(np.conj(phase))

    def __str__(self):
        return "W({}, {})".format(np.round(self.angle/np.pi,2), np.round(self.axis_angle/np.pi, 2))

    def tex_str(self):
        return "W$_{{{}, {}}}$".format(np.round(self.angle/np.pi, 2),
                   np.round(self.axis_angle/np.pi, 2))

# class ExpZGate(Rz, XmonGate):
class ExpZGate(XmonGate):
    r"""A rotation around the Z axis of the Bloch sphere.

    This gate implements :math:`\exp(-i \pi Z \varphi / 2)` where Z is the Z matrix

        Z = [[1, 0], [0, -1]]

    and :math:`\varphi` are half turns.

    The full matrix reads:

    .. math::

        \begin{pmatrix}
        exp(-i \pi \varphi / 2) & 0\\
        0 & exp(i \pi \varphi / 2)
        \end{pmatrix}

    Note the half_turn nomenclature here comes from viewing this as a rotation
    on the Bloch sphere. Two half_turns correspond to a rotation in the
    bloch sphere of 360 degrees.

    Half_turns are mapped to the range (-1, 1], i.e. to rotation angles
    in the range (-pi, pi].

    Note:
        Restricting half_turns to the rage (-1, 1] corresponds to the full range (0, 2pi]
        for the phase difference between the Z eigenstates. However, we loose the global phase
        that comes with a full rotation gate in the range (0, 4pi]. Thus, the ExpZ gate is more
        like a phase then a rotation gate.

    Args:
        half_turns (float): number of half turns on the Bloch sphere.
    """

    def __init__(self, half_turns):
        # Rz.__init__(self, half_turns * cmath.pi)
        XmonGate.__init__(self)
        self.half_turns = half_turns

    @property
    def angle(self):
        r"""Rotation angle in rad, :math:`\in(-\pi, \pi]`"""
        return self.half_turns * cmath.pi

    @property
    def half_turns(self):
        r"""Rotation angle in half turns, :math:`\in(-1, 1]`"""
        return self._half_turns

    @half_turns.setter
    def half_turns(self, half_turns):
        self._half_turns = value.chosen_angle_to_canonical_half_turns(half_turns=half_turns,
                                                                      rads = None,
                                                                      degs=None)
    @property
    def matrix(self):
        r"""Rotation matrix.

        With :math:`\varphi = \mathrm{half\_turns}` this gate implements the matrix

        .. math::

            \begin{pmatrix}
            \cos(\varphi\pi / 2) - i \sin(\varphi \pi / 2) & 0\\
            0 & \cos(\varphi\pi / 2) + i \sin(\varphi \pi / 2)
            \end{pmatrix}
        """
        return np.array([[np.cos(self.angle / 2) - 1.0j * np.sin(self.angle / 2), 0],
                          [0, np.cos(self.angle / 2) + 1.0j * np.sin(self.angle / 2)]])

    def __str__(self):
        return "Z({})".format(np.round(self.angle / np.pi,2))

    def tex_str(self):
        r"""Latex representation of the gate."""
        return "Z$_{{{}}}$".format(np.round(self.angle / np.pi,2))

    def get_merged(self, other):
        """
        Return self merged with another gate.
        Default implementation handles rotation gate of the same type, where
        angles are simply added.
        Args:
            other: Rotation gate of same type.
        Raises:
            NotMergeable: For non-rotation gates or rotation gates of
                different type.
        Returns:
            New object representing the merged gates.
        """
        if isinstance(other, self.__class__):
            return self.__class__((self.angle + other.angle) / cmath.pi)
        raise NotMergeable("Can't merge different types of rotation gates.")

from projectq.backends._circuits._to_latex import get_default_settings
def drawer_settings():
    xmon_settings = get_default_settings()
    xmon_settings['gate_shadow'] = False
    xmon_settings['gates']['ExpWGate'] = {'height': 0.8, 'offset': 0.3,
                 'pre_offset': 0.2, 'width': 1.75}
    xmon_settings['gates']['ExpZGate'] = {'height': 0.8, 'offset': 0.3,
                 'pre_offset': 0.2, 'width': 1.}
    xmon_settings['gates']['Exp11Gate'] = {'height': .8, 'offset': 0.3,
                 'pre_offset': 0.3, 'width': 1.}
    return xmon_settings
