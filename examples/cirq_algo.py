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
from numbers import Number
import numpy as np
import cirq
from cirq.google import xmon_gates, xmon_qubit
from cirq.contrib.qcircuit_diagram import circuit_to_latex_using_qcircuit

def nearest_neighbor_hopping(amplitude, qubits):
    """
    Implement a nearest neighbor hopping step between two electrons using xmon
    gates only.
    """
    assert len(qubits)==2
    q0 = qubits[0]
    q1 = qubits[1]
    amplitude /= np.pi
    yield xmon_gates.ExpWGate(half_turns=.5, axis_half_turns=0)(q0)
    yield xmon_gates.ExpWGate(half_turns=-.5, axis_half_turns=.5)(q1)
    yield xmon_gates.ExpZGate(half_turns=1)(q1)
    yield xmon_gates.Exp11Gate(half_turns=1.0)(q0, q1)
    yield xmon_gates.ExpWGate(half_turns=amplitude, axis_half_turns=0)(q0)
    yield xmon_gates.ExpWGate(half_turns=-amplitude, axis_half_turns=.5)(q1)
    yield xmon_gates.Exp11Gate(half_turns=1.0)(q0, q1)
    yield xmon_gates.ExpWGate(half_turns=-.5, axis_half_turns=0)(q0)
    yield xmon_gates.ExpWGate(half_turns=-.5, axis_half_turns=.5)(q1)
    yield xmon_gates.ExpZGate(half_turns=1)(q1)

def zz_interaction(amplitude, qubits):
    """
    Implement a density-density interaction between two fermionic orbitals
    using xmon gates only.
    """
    assert len(qubits)==2
    if isinstance(amplitude, Number):
        amplitude /= - np.pi
    q0 = qubits[0]
    q1 = qubits[1]
    yield xmon_gates.Exp11Gate(half_turns=amplitude)(q0, q1)

def onsite(amplitude, qubit):
    """
    Implement a local (onsite) fermionic term using xmon gates only.
    """
    assert len(qubit)==1
    yield xmon_gates.ExpZGate(half_turns = amplitude / np.pi)(qubit)

def trotter_step(t, U, qubits, impsite=None, order=2):
    """
    Implement a single Trotter step for an Anderson model with interaction
    strength U, and hopping amplitude t, and impurity location imploc.
    Trotter order can be 1 or 2.
    """
    sites = len(qubits)//2
    assert order in (1, 2)
    impsite = impsite or len(qubits)//4
    for i in range(sites - 1):
        for o in nearest_neighbor_hopping(t/order, (qubits[i], qubits[i+1])):
            yield o
        for o in nearest_neighbor_hopping(t/order, (qubits[i+sites], qubits[i+1+sites])):
            yield o
    for o in zz_interaction(U, (qubits[impsite], qubits[impsite + sites])):
        yield o
    if order==2:
        for i in reversed(range(sites - 1)):
            for o in nearest_neighbor_hopping(t/2, (qubits[i+sites], qubits[i+1+sites])):
                yield o
            for o in nearest_neighbor_hopping(t/2, (qubits[i], qubits[i+1])):
                yield o

from cirq import Symbol
sites = 3
qubits = [xmon_qubit.XmonQubit(0, i) for i in range(sites)]\
            + [xmon_qubit.XmonQubit(1, i) for i in range(sites)]

def scale_H(amplitudes, allowed=np.pi):
    m = max(np.abs(amplitudes))
    return [a * allowed / m for a in amplitudes]

t = - 0.8 * np.pi
U = 0.5 * np.pi
#t, U = scale_H([t, U])

circuit = cirq.Circuit()
circuit.append(nearest_neighbor_hopping(t, (qubits[0], qubits[1])))
print(circuit)
with open('hopping.tex', 'w') as fl:
    print("\\documentclass{standalone}\n\\usepackage{amsmath}\n\\usepackage{qcircuit}\n\\begin{document}\n$$", file=fl)
    print(circuit_to_latex_using_qcircuit(circuit), file=fl)
    print("$$\n\\end{document}", file=fl)


circuit = cirq.Circuit()
circuit.append(zz_interaction(U, (qubits[0], qubits[1])))
print(circuit)
with open('interaction.tex', 'w') as fl:
    print("\\documentclass{standalone}\n\\usepackage{amsmath}\n\\usepackage{qcircuit}\n\\begin{document}\n$$", file=fl)
    print(circuit_to_latex_using_qcircuit(circuit), file=fl)
    print("$$\n\\end{document}", file=fl)
#
circuit = cirq.Circuit()
circuit.append(trotter_step(t, U, qubits, order=1), strategy=cirq.circuits.InsertStrategy.EARLIEST)
print(circuit)
with open('trotter.tex', 'w') as fl:
    print("\\documentclass{standalone}\n\\usepackage{amsmath}\n\\usepackage{qcircuit}\n\\begin{document}\n$$", file=fl)
    print(circuit_to_latex_using_qcircuit(circuit), file=fl)
    print("$$\n\\end{document}", file=fl)

from cirq.google import XmonSimulator
from openfermion.ops import FermionOperator
from openfermion.transforms import get_sparse_operator
from scipy import sparse
from itertools import product
from matplotlib import pyplot as plt

t = - 0.3 * np.pi
U = 0.6 * np.pi
t, U = scale_H([t, U])
Steps = list(range(1,16))
res = {1: [], 2: []}
for order, steps in product((1, 2), Steps):
    circuit = cirq.Circuit()
    init = []
    for i in range(sites//2+sites%2):
        init.append(xmon_gates.ExpWGate(half_turns=1.0, axis_half_turns=0.0)(qubits[i]))
    for i in range(sites//2, sites):
        init.append(xmon_gates.ExpWGate(half_turns=1.0, axis_half_turns=0.0)(qubits[i + sites]))
    circuit.append(init, strategy=cirq.circuits.InsertStrategy.EARLIEST)
    for j in range(steps):
        circuit.append(trotter_step(t/steps, U/steps, qubits, order=order), strategy=cirq.circuits.InsertStrategy.EARLIEST)
    simulator = XmonSimulator()
    result = simulator.simulate(circuit)

    h = np.sum([FermionOperator(((i, 1), (i+1, 0)), t) +
                FermionOperator(((i+1, 1), (i, 0)), t) +
                FermionOperator(((i+sites, 1), (i+1+sites, 0)), t) +
                FermionOperator(((i+1+sites, 1), (i+sites, 0)), t) for i in range(sites-1)])
    h += FermionOperator(((sites//2, 1), (sites//2, 0), (sites//2+sites, 1), (sites//2+sites, 0)), U)
    init = FermionOperator(tuple([(i, 1) for i in range(sites//2+sites%2)] + [(i+sites, 1) for i in range(sites//2, sites)]),
                           1.0)
    init = get_sparse_operator(init, sites*2)
    init = init.dot(np.array([1] + [0]*(2**(sites*2)-1)))
    h = get_sparse_operator(h, 2*sites)
    psi = sparse.linalg.expm_multiply(-1.0j * h, init)
    res[order].append(np.abs(psi.conj().T.dot(result.final_state))**2)

fig = plt.figure()
for k, r in res.items():
    plt.plot(Steps, r, '.-', label="Trotter order: {}".format(k))
plt.legend()
plt.xlabel("Trotter steps")
plt.ylabel("State fidelity")
plt.title("State fidelity for Anderson model using cirq simulator")

t = - 1.0
#U = 0.6 * np.pi
t, U = scale_H([t, U])
Ulist = np.linspace(0, 2)
resU = {1: [], 2: []}
for order, U in product((1, 2), Ulist):
    steps = 10
    circuit = cirq.Circuit()
    init = []
    for i in range(sites//2+sites%2):
        init.append(xmon_gates.ExpWGate(half_turns=1.0, axis_half_turns=0.0)(qubits[i]))
    for i in range(sites//2, sites):
        init.append(xmon_gates.ExpWGate(half_turns=1.0, axis_half_turns=0.0)(qubits[i + sites]))
    circuit.append(init, strategy=cirq.circuits.InsertStrategy.EARLIEST)
    for j in range(steps):
        circuit.append(trotter_step(t/steps, U/steps, qubits, order=order), strategy=cirq.circuits.InsertStrategy.EARLIEST)
    simulator = XmonSimulator()
    result = simulator.simulate(circuit)

    h = np.sum([FermionOperator(((i, 1), (i+1, 0)), t) +
                FermionOperator(((i+1, 1), (i, 0)), t) +
                FermionOperator(((i+sites, 1), (i+1+sites, 0)), t) +
                FermionOperator(((i+1+sites, 1), (i+sites, 0)), t) for i in range(sites-1)])
    h += FermionOperator(((sites//2, 1), (sites//2, 0), (sites//2+sites, 1), (sites//2+sites, 0)), U)
    init = FermionOperator(tuple([(i, 1) for i in range(sites//2+sites%2)] + [(i+sites, 1) for i in range(sites//2, sites)]),
                           1.0)
    init = get_sparse_operator(init, sites*2)
    init = init.dot(np.array([1] + [0]*(2**(sites*2)-1)))
    h = get_sparse_operator(h, 2*sites)
    psi = sparse.linalg.expm_multiply(-1.0j * h, init)
    resU[order].append(np.abs(psi.conj().T.dot(result.final_state))**2)
#    print("Overlap:", res[-1])
#    print(psi.conj().T.dot(h.dot(psi)).real)
#    print(result.final_state.conj().T.dot(h.dot(result.final_state)).real)

fig2 = plt.figure()
for k, r in resU.items():
    plt.plot(Ulist, r, '.-', label="Trotter order: {}".format(k))
plt.legend()
plt.xlabel("U")
plt.ylabel("State fidelity")
plt.title("State fidelity for Anderson model using cirq simulator")

plt.show()
