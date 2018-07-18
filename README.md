# CirqProjectQ

Heisenberg has developed a port between ProjectQ and Cirq, called CirqProjectQ. ProjectQ is an open source tool to compile source code for quantum computers. Cirq is an open source framework developed by Google for building and experimenting with noisy intermediate scale quantum (NISQ) algorithms on near-term quantum processors. Heisenberg is an early stage partner of Google and has had early access to Cirq.

CirqProjectQ provides two main functionalities:

1. A ProjectQ backend to convert a ProjectQ algorithm to a cirq.Circuit.

2. ProjectQ decompositions from common gates to native Xmon gates that can be used to simulate a Google quantum computer with ProjectQ.
