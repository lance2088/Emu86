"""
data_mov_att.py: other data movement instructions for AT&T
"""

from assembler.errors import check_num_args, InvalidConVal, InvalidArgument
from assembler.tokens import Instruction, RegAddress, Address, IntegerTok

def check_constant_val(instr, ops, data_type):
    if isinstance(ops[0], RegAddress) or isinstance(ops[0], Address):
        if not isinstance(ops[1], IntegerTok):
            raise InvalidConVal(ops[1].get_nm())
        else:
            if data_type == "b":
                if ops[1].get_val() >= 2 ** 8:
                    raise InvalidConVal(str(ops[1].get_val()))
            elif data_type == "w":
                if ops[1].get_val() >= 2 ** 16:
                    raise InvalidConVal(str(ops[1].get_val()))
            else:
                if ops[1].get_val() >= 2 ** 32:
                    raise InvalidConVal(str(ops[1].get_val()))
    else:
        raise InvalidArgument(ops[0].get_nm())

class Movb(Instruction):
    """
        <instr>
             movb
        </instr>
        <syntax>
            MOVB con, mem
        </syntax>
        <descr>
            Copies the value of op1 to the location mentioned in op2. 
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 2)
        check_constant_val(self.get_nm(), ops, 'b')
        ops[0].set_val(ops[1].get_val())

class Movw(Instruction):
    """
        <instr>
             movw
        </instr>
        <syntax>
            MOVW con, mem
        </syntax>
        <descr>
            Copies the value of op1 to the location mentioned in op2. 
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 2)
        check_constant_val(self.get_nm(), ops, 'w')
        ops[0].set_val(ops[1].get_val())

class Movl(Instruction):
    """
        <instr>
             movl
        </instr>
        <syntax>
            MOVL con, mem
        </syntax>
        <descr>
            Copies the value of op1 to the location mentioned in op2. 
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 2)
        check_constant_val(self.get_nm(), ops, 'l')
        ops[0].set_val(ops[1].get_val())