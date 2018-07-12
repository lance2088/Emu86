#!/usr/bin/env python3
import sys
sys.path.append(".")
import random
import string

import operator as opfunc
import functools
from assembler.virtual_machine import mips_machine

from unittest import TestCase, main

from assembler.assemble import assemble
NUM_TESTS=1000

"""
Test entire programs.

tests/arithmetic_shift.asm  tests/data.asm  tests/gt.asm  tests/key_test.asm  tests/loop.asm  tests/power.asm  tests/test.asm  tests/test_control_flow.asm  tests/test_interrupt.asm
"""

class TestPrograms(TestCase):

    def read_test_code(self, filenm):
        with open (filenm, "r") as prog:
            return prog.read()

    def run_mips_test_code (self, filnm):
        mips_machine.re_init()
        test_code = self.read_test_code(filnm)
        assemble(test_code, 'mips', mips_machine)

    def test_loop(self):
        self.run_mips_test_code("tests/MIPS/loop.asm")
        self.assertEqual(mips_machine.registers["R11"], 16)

    # def test_power(self):
    #     self.run_intel_test_code("tests/Intel/power.asm")
    #     self.assertEqual(intel_machine.registers["EDX"], 65536)

    def test_gt(self):
        self.run_mips_test_code("tests/MIPS/gt.asm")
        self.assertEqual(mips_machine.registers["R8"], 17)
        self.assertEqual(mips_machine.registers["R9"], 16)
        self.assertEqual(mips_machine.registers["R13"], 16)
        self.assertEqual(mips_machine.registers["R14"], 19)

    # def test_interrupt(self):
    #     self.run_intel_test_code("tests/Intel/test_interrupt.asm")
    #     self.assertEqual(intel_machine.registers["EAX"], 71)
    #     self.assertEqual(intel_machine.registers["EBX"], 6)
    #     self.assertEqual(intel_machine.registers["ECX"], 1)
    #     self.assertEqual(intel_machine.registers["ESP"], 511)
    #     self.assertEqual(intel_machine.memory["6"], 71)

    # def test_key(self):
    #     self.run_intel_test_code("tests/Intel/key_test.asm")
    #     self.assertEqual(intel_machine.registers["EAX"], 71)
    #     self.assertEqual(intel_machine.registers["EBX"], 71)
    #     self.assertEqual(intel_machine.registers["ECX"], 1)
    #     self.assertEqual(intel_machine.registers["ESP"], 511)
    #     self.assertEqual(intel_machine.memory["9"], 83)

    # def test_arithmetic_shift(self):
    #     self.run_intel_test_code("tests/Intel/arithmetic_shift.asm")
    #     self.assertEqual(intel_machine.registers["EAX"], 4)
    #     self.assertEqual(intel_machine.registers["EBX"], 10)
    #     self.assertEqual(intel_machine.registers["ECX"], 8)
    #     self.assertEqual(intel_machine.registers["EDX"], 8)
    #     self.assertEqual(intel_machine.memory["4"], 4)

    def test_jump(self):
        self.run_mips_test_code("tests/MIPS/test_jump.asm")
        self.assertEqual(mips_machine.registers["R8"], 3)

    # def test_data(self):
    #     self.run_intel_test_code("tests/Intel/data.asm")
    #     self.assertEqual(intel_machine.registers["EAX"],  8)
    #     self.assertEqual(intel_machine.registers["EBX"], 16)
    #     self.assertEqual(intel_machine.registers["ECX"], 32)

    # def test_array(self):
    #     self.run_intel_test_code("tests/Intel/array.asm")
    #     self.assertEqual(intel_machine.registers["EAX"],  3)
    #     self.assertEqual(intel_machine.registers["EBX"], -50)
    #     self.assertEqual(intel_machine.registers["ECX"], ord ('l'))
    #     self.assertEqual(intel_machine.registers["EDX"], 5)
    #     list_x = [3, 8, 5, 2]
    #     string_z = "hello"
    #     for position in range(0, 4):
    #         self.assertEqual(intel_machine.memory[str(position)], list_x[position])
    #     for position in range(4, 17):
    #         self.assertEqual(intel_machine.memory[(hex(position).split('x')
    #                                          [-1]).upper()], -50)
    #     for position in range(17, 22):
    #         self.assertEqual(intel_machine.memory[(hex(position).split('x')
    #                                          [-1]).upper()], 
    #                          ord(string_z[position - 17]))
    #     self.assertEqual(intel_machine.memory[hex(22).split('x')[-1]], 0)

    def test_sum_calculation(self):
        self.run_mips_test_code("tests/MIPS/sum_test.asm")
        self.assertEqual(mips_machine.registers["R8"],  53)
        self.assertEqual(mips_machine.memory["1"], 53)

    def test_arithmetic_expression(self):
        self.run_mips_test_code("tests/MIPS/arithmetic_expression.asm")
        self.assertEqual(mips_machine.registers["R8"], -31)
        self.assertEqual(mips_machine.registers["R10"], 52)

    def test_area(self):
        self.run_mips_test_code("tests/MIPS/area.asm")
        self.assertEqual(mips_machine.registers["R8"], 35)
        self.assertEqual(mips_machine.registers["R9"], 27)
        self.assertEqual(mips_machine.registers["R10"], 35 * 27)
        self.assertEqual(mips_machine.registers["LO"], 35 * 27)
        self.assertEqual(mips_machine.registers["HI"], 0)

    def test_celsius_conversion(self):
        self.run_mips_test_code("tests/MIPS/cel_to_fah.asm")
        self.assertEqual(mips_machine.registers["R8"], 95)
        self.assertEqual(mips_machine.memory["1"], 95)
        self.assertEqual(mips_machine.registers["HI"], 2)
        self.assertEqual(mips_machine.registers["R9"], 5)

    def test_log(self):
        self.run_mips_test_code("tests/MIPS/log.asm")
        self.assertEqual(mips_machine.registers["R9"], 1024)
        self.assertEqual(mips_machine.registers["R8"], 9)

    # def test_mem_register(self):
    #     self.run_intel_test_code("tests/Intel/mem_register_test.asm")
    #     self.assertEqual(intel_machine.registers["EAX"], 6)
    #     self.assertEqual(intel_machine.memory["6"], 3)
    #     self.assertEqual(intel_machine.memory["8"], 8)
    #     self.assertEqual(intel_machine.memory["0"], 50)
    #     self.assertEqual(intel_machine.memory["1"], 32)

    def test_array_avg(self):
        self.run_mips_test_code("tests/MIPS/array_average_test.asm")
        self.assertEqual(mips_machine.registers["R16"], 10)
        self.assertEqual(mips_machine.registers["R8"], 89)
        self.assertEqual(mips_machine.registers["R9"], 10)
        self.assertEqual(mips_machine.registers["R10"], 10)
        self.assertEqual(mips_machine.registers["R12"], 8)
        self.assertEqual(mips_machine.registers["R13"], 9)

    def test_int_square_root(self):
        self.run_mips_test_code("tests/MIPS/int_square_root.asm")
        self.assertEqual(mips_machine.registers["R8"], 10)

    def test_add_to_array_elem_test(self):
        self.run_mips_test_code("tests/MIPS/change_array_elem_test.asm")
        self.assertEqual(mips_machine.registers["R8"], 361)
        self.assertEqual(mips_machine.registers["R13"], 361)
        self.assertEqual(mips_machine.registers["R17"], 10)
        self.assertEqual(mips_machine.registers["R9"], 10)

if __name__ == '__main__':
    main()
