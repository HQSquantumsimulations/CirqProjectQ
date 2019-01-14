# CirqProjectQ

HQS quantum simulations has developed a port between [ProjectQ](https://github.com/ProjectQ-Framework/ProjectQ) and [Cirq](https://github.com/quantumlib/Cirq/blob/master/docs/install.md), called CirqProjectQ. ProjectQ is an open source tool to compile source code for quantum computers. Cirq is an open source framework developed by Google for building and experimenting with noisy intermediate scale quantum (NISQ) algorithms on near-term quantum processors. HQS quantum simulations is an early stage partner of Google and has had early access to Cirq.

CirqProjectQ provides two main functionalities:

1. A ProjectQ backend to convert a ProjectQ algorithm to a cirq.Circuit.

2. ProjectQ decompositions from common gates to native Xmon gates that can be used to simulate a Google quantum computer with ProjectQ.

For more information see the detailed code [documentation](https://cirqprojectq.readthedocs.io/en/latest/)

## Using Cirq to simulate condensed matter
The [Anderson model](https://en.wikipedia.org/wiki/Anderson_impurity_model) is an important model in condensed matter physics describing, for example, transport in disordered materials. HQS quantum simulations has used Cirq to simulate the Anderson model on a simulated quantum computer, see our [example code](https://github.com/HeisenbergQS/CirqProjectQ/blob/master/examples/siam_cirq.py). More information about our simulation on Cirq can be found in this [presentation](https://heisenberg.xyz/wp-content/uploads/2018/07/Anderson_Cirq_Heisenberg_Slides_v2.pdf)
