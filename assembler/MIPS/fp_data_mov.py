"""
data_mov.py: data movement instructions.
"""
from assembler.errors import check_num_args, InvalidArgument, TooBigForSingle
from assembler.tokens import Instruction, Register, RegAddress, Symbol

class Loadc(Instruction):
    """
        <instr>
             LWC
        </instr>
        <syntax>
            LWC reg, reg
            LWC reg, disp(reg)
        </syntax>
        <descr>
            Copies the value of op2 to the location mentioned in op1. 
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 2)
        if isinstance(ops[0], Register):
            if isinstance(ops[1], RegAddress):
                print("val",ops[1].get_val())
                print("fv", float(ops[1].get_val()))
                if (float(ops[1].get_val()) > float(2 ** 22)):
                    raise TooBigForSingle(str(float(ops[1].get_val())))
                ops[0].set_val(float(ops[1].get_val()))
                vm.changes.add(ops[0].get_nm())
            else:
                raise InvalidArgument(ops[1].get_nm())
        else: 
            raise InvalidArgument(ops[0].get_nm())

class Storec(Instruction):
    """
        <instr>
             SWC
        </instr>
        <syntax>
            SWC reg, reg
            SWC reg, disp(reg)
        </syntax>
        <descr>
            Copies the value of op2 to the location mentioned in op1. 
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 2)
        if isinstance(ops[0], Register):
            if isinstance(ops[1], RegAddress):
                if (float(ops[0].get_val()) > float(2 ** 22)):
                    raise TooBigForSingle(str(float(ops[0].get_val())))
                ops[1].set_val(float(ops[0].get_val()))
            else:
                InvalidArgument(ops[1].get_nm())
        else: 
            raise InvalidArgument(ops[0].get_nm())