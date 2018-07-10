"""
control_flow.py: control flow instructions,
    plus Exceptions to signal break in flow.

"""

from assembler.errors import check_num_args, OutofBounds
from assembler.tokens import Instruction, Register, IntegerTok
from .argument_check import *



class FlowBreak(Exception):
    """
    Base class for all of our flow break exceptions.
    """
    def __init__(self, label):
        super().__init__("Flow break")
        self.label = label
        self.msg = "Unknown control flow exception."

def get_one_op(instr, ops):
    check_num_args(instr, ops, 1)
    return ops[0]

def get_two_ops(instr, ops):
    check_num_args(instr, ops, 2)
    return (ops[0], ops[1])

def get_three_ops(instr, ops):
    check_num_args(instr, ops, 3)
    check_reg_only(instr, ops)
    return (ops[0], ops[1], ops[2])

def get_three_ops_imm(instr, ops):
    check_num_args(instr, ops, 3)
    check_immediate_three(instr, ops)
    return (ops[0], ops[1], ops[2])

class Jump(FlowBreak):
    def __init__(self, label):
        super().__init__(label)
        self.msg = "Jump to " + label


class Slt(Instruction):
    """
        <instr>
             slt
        </instr>
        <syntax>
            SLT reg, reg, reg
        </syntax>
        <descr>
            Compares op2 and op3, and sets (right now) the SF and ZF flags.
            It is not clear at this moment how to 
            treat the OF and CF flags in Python,
            since Python integer arithmetic never carries or overflows!
            Store the result of SF flag into op1
        </descr>
    """
    def fhook(self, ops, vm):      
        (op1, op2, op3) = get_three_ops(self.get_nm(), ops)
        res = op2.get_val() - op3.get_val()
        # set the proper flags
        # zero flag:
        if res == 0:
            vm.flags['ZF'] = 1
        else:
            vm.flags['ZF'] = 0
        # sign flag:
        if res < 0:
            vm.flags['SF'] = 1
        else:
            vm.flags['SF'] = 0
        op1.set_val(vm.flags['SF'])

class Slti(Instruction):
    """
        <instr>
             slti
        </instr>
        <syntax>
            SLTI reg, con, reg
            SLTI reg, reg, con
        </syntax>
        <descr>
            Compares op2 and op3, and sets (right now) the SF and ZF flags.
            It is not clear at this moment how to 
            treat the OF and CF flags in Python,
            since Python integer arithmetic never carries or overflows!
            Store the result of SF flag into op1
        </descr>
    """
    def fhook(self, ops, vm):
        (op1, op2, op3) = get_three_ops_imm(self.get_nm(), ops)
        res = op2.get_val() - op3.get_val()
        # set the proper flags
        # zero flag:
        if res == 0:
            vm.flags['ZF'] = 1
        else:
            vm.flags['ZF'] = 0
        # sign flag:
        if res < 0:
            op1.set_val(1)
        else:
            op1.set_val(0)
    

class Jmp(Instruction):
    """
        <instr>
            jmp
        </instr>
        <syntax>
            JMP lbl
        </syntax>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        raise Jump(target.name)

class Beq(Instruction):
    """
        <instr>
             BEQ
        </instr>
        <syntax>
            BEQ con, reg, reg
        </syntax>
        <descr>
            Jumps if registers are equal.
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args("BEQ", ops, 3)
        disp = 0
        if isinstance(ops[0], IntegerTok):
            disp = ops[0].get_nm()
        else:
            raise InvalidArgument(ops[0].get_nm())
        val_one, val_two = (0, 0)
        if isinstance(ops[1], Register):
            val_one = ops[1].get_val()
            if isinstance(ops[2], Register):
                val_two = ops[2].get_val()
            else:
                InvalidArgument(ops[2].get_nm())
        else:
            InvalidArgument(ops[1].get_nm())
        if val_one == val_two:
            current_ip = vm.get_ip() 
            if current_ip + disp * 4 >= 0:
                vm.set_ip(current_ip + disp * 4)
            else:
                raise OutofBounds()

class Bne(Instruction):
    """
        <instr>
             BNE
        </instr>
        <syntax>
            BNE con, reg, reg
        </syntax>
        <descr>
            Jumps if registers are equal.
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args("BNE", ops, 3)
        disp = 0
        if isinstance(ops[0], IntegerTok):
            disp = ops[0].get_val()
        else:
            raise InvalidArgument(ops[0].get_nm())
        val_one, val_two = (0, 0)
        if isinstance(ops[1], Register):
            val_one = ops[1].get_val()
            if isinstance(ops[2], Register):
                val_two = ops[2].get_val()
            else:
                InvalidArgument(ops[2].get_nm())
        else:
            InvalidArgument(ops[1].get_nm())
        if val_one != val_two:
            current_ip = vm.get_ip()
            if current_ip + disp * 4 >= 0:
                vm.set_ip(current_ip + disp * 4)
            else:
                raise OutofBounds()

class Jne(Instruction):
    """
        <instr>
             jne
        </instr>
        <syntax>
            JNE lbl
        </syntax>
        <descr>
            Jumps if ZF is zero. <br>
            Equivalent name: JNZ
        </descr>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        if int(vm.flags['ZF']) == 0:
            raise Jump(target.name)

class Jg(Instruction):
    """
        <instr>
             jg
        </instr>
        <syntax>
            JG lbl
        </syntax>
        <descr>
            Jumps if SF == 0 and ZF == 0. <br>
            Equivalent name: JLNE
        </descr>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        if (int(vm.flags['SF']) == 0 
            and int(vm.flags['ZF']) == 0):
            raise Jump(target.name)

class Jge(Instruction):
    """
        <instr>
             jge
        </instr>
        <syntax>
            JGE lbl
        </syntax>
        <descr>
            Jumps if SF == 0.
        </descr>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        if int(vm.flags['SF']) == 0:
            raise Jump(target.name)
        return ''

class Jl(Instruction):
    """
        <instr>
             jl
        </instr>
        <syntax>
            JL lbl
        </syntax>
        <descr>
            Jumps if SF == 1. <br>
            Equivalent name: JGNE
        </descr>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        if int(vm.flags['SF']) == 1:
            raise Jump(target.name)
        return ''

class Jle(Instruction):
    """
        <instr>
             jle
        </instr>
        <syntax>
            JLE lbl
        </syntax>
        <descr>
            Jumps if SF == 1 or ZF == 1.
        </descr>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        if (int(vm.flags['SF']) == 1
            or int(vm.flags['ZF']) == 1):
            raise Jump(target.name)
        return ''

class Call(Instruction):
    """
        <instr>
             call
        </instr>
        <syntax>
            CALL lbl
        </syntax>
        <descr>
            Pushes value of EIP to stack and jumps to the internal subroutine.
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args("CALL", ops, 1)
        vm.dec_sp()
        vm.stack[hex(vm.get_sp() + 1).split('x')[-1].upper()] = vm.get_ip()
        target = get_one_op(self.get_nm(), ops)
        raise Jump(target.name)

class Ret(Instruction):
    """
        <instr>
             ret
        </instr>
        <syntax>
            RET
        </syntax>
        <descr>
            Pops value from stack to EIP and returns control to the 
            the line after the subroutine call.
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args("RET", ops, 0)
        vm.inc_sp()
        vm.set_ip(int(vm.stack[hex(vm.get_sp()).split('x')[-1].upper()]))
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = vm.empty_cell()
