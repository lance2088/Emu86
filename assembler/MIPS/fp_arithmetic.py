"""
fp_arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfunc

from assembler.errors import *
from assembler.tokens import Instruction, MAX_INT, Register, IntegerTok
from assembler.ops_check import one_op_arith
from .argument_check import * 

def check_overflow(val, vm):
    if(val > MAX_INT):
        val = val - MAX_INT+1
    return val

def three_op_arith_reg(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3)
    check_reg_only(instr, ops)
    ops[0].set_val(
    check_overflow(operator(ops[1].get_val(),
                       ops[2].get_val()), 
                       vm)) 
    vm.changes.add(ops[0].get_nm())


#'ADD.S': Adds('ADD.S'),
class Adds(Instruction):
    """
        <instr>
             ADD.S
        </instr>
        <syntax>
            ADD.S reg, reg, reg
        </syntax>
    """
    # ops is a list of operands (reg, reg, reg)
    def fhook(self, ops, vm):
        three_op_arith_reg(ops, vm, self.name, opfunc.add)

#'SUB.S': Subs('SUB.S'),
class Subs(Instruction):
    """
        <instr>
             SUB
        </instr>
        <syntax>
            SUB reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_reg(ops, vm, self.name, opfunc.sub)

#'MULT.S': Mults('MULT.S'),
class Mults(Instruction):
    """
        <instr>
             MULT
        </instr>
        <syntax>
            MULT reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 2)
        check_reg_only(self.name, ops)
        result = ops[0].get_val() * ops[1].get_val()
        #deal with the high and low registers
        
#'DIV.S': Divs('DIV.S'),