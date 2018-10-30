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
This file provides classes to store rules for translating ProjectQ to Cirq
operations.
"""
from collections import defaultdict

class Ruleset_pq_to_cirq():
    def __init__(self, rules=[]):
        r"""
        A collection of rules to translate ProjectQ operations to Cirq
        operations.

        Args:
            rules (list of :class:`Rule_pq_to_cirq`): the rules that can be used for translations.
        """
        self._known_rules = defaultdict(list)
        self.add_rules(rules)

    def add_rules(self, rules=[]):
        r"""
        Add rules to the set of known rules.

        Args:
            rules (list of :class:`Rule_pq_to_cirq`): the rules that can be used for translations.
        """

        if hasattr(rules, '__iter__'):
            for rule in rules:
                self.add_rule(rule)
        else:
            self.add_rule(rules)

    def add_rule(self, rule):
        r"""
        Add a single rule to the set of known rules.

        Args:
            rule (:class:`Rule_pq_to_cirq`): a rule that can be used for translations.
        """
        for cls in rule.classes:
            self._known_rules[cls].append(rule.translation)

    def translate(self, cmd, mapping, qubits):
        r"""
        Translate a projectq operation into a Cirq operation.

        Args:
            cmd (:class:`projectq.ops.Command`): a projectq command instance
            mapping (:class:`dict`): a dictionary of qubit mappings
            qubits (list of :class:cirq.QubitID`): cirq qubits

        Returns:
            :class:`cirq.Operation`
        """
        if type(cmd.gate) in self._known_rules:
            return self._known_rules[type(cmd.gate)][0](cmd, mapping, qubits)
        else:
            raise TypeError

    @property
    def known_rules(self):
        """
        Dictionary of known translations.
        """
        return self._known_rules.copy()

class Rule_pq_to_cirq():
    def __init__(self, classes, translation):
        r"""
        A class to store a single translation rule from Projectq to Cirq.

        Args:
            classes (list of :class:`projectq.ops.BasicGate`): the gate classes to which the rule applies.
            translation (callable(:class:`projectq.ops.Command`, :class:`dict`, list of :class:cirq.QubitID`)): a translation to cirq
        """
        self.classes = classes
        self.translation = translation
