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
from projectq import cengines, ops, setups
from . import xmon_gates, xmon_decompositions

def _filter_xmon(eng, cmd):
    '''
    Determines if a gate can be handled by xmon qubits.

    Args:
        eng(projectq.MainEngine): The engine.
        cmd(projectq.ops.Command): A projectq command object.

    Returns:
        bool: True, if cmd.gate is a valid Xmon gate.

    '''
    if isinstance(cmd.gate, ops.ClassicalInstructionGate):
        # This is required to allow Measure, Allocate, Deallocate, Flush
        return True
    elif isinstance(cmd.gate, xmon_gates.XmonGate):
        return True
    else:
        return False

def xmon_rules():
    allrules = xmon_decompositions.all_defined_decomposition_rules
    return cengines.DecompositionRuleSet(allrules)

def replacer_xmon():
    rule_set = cengines.DecompositionRuleSet(
            modules=[xmon_decompositions, setups.decompositions])
    return cengines.AutoReplacer(rule_set)

def xmon_supported_filter():
    return cengines.InstructionFilter(_filter_xmon)

def xmon_engines():
    return [cengines.TagRemover(),
            cengines.LocalOptimizer(),
            replacer_xmon(),
            cengines.TagRemover(),
            cengines.LocalOptimizer(),
            xmon_supported_filter()]