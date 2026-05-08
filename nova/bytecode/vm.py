"""
Virtual Machine (VM) untuk Nova Bytecode
Menjalankan instruksi bytecode yang dihasilkan Compiler
"""

from .compiler import Instruction


class VM:
    """Stack-based Virtual Machine"""

    def __init__(self):
        self.stack: list = []  # Operand stack
        self.vars: dict = {}  # Variabel lokal/global
        self.output: list = []  # Output seperti print
        self.pc: int = 0  # Program counter

    def run(self, instructions: list, consts: list) -> list:
        """Jalankan bytecode hingga selesai atau RETURN"""
        self.pc = 0
        self.output = []

        while self.pc < len(instructions):
            instr = instructions[self.pc]
            self.pc += 1

            op = instr.op
            arg = instr.arg

            try:
                if op == 'LOAD_CONST':
                    self.stack.append(consts[arg])

                elif op == 'LOAD_VAR':
                    if arg in self.vars:
                        self.stack.append(self.vars[arg])
                    else:
                        raise Exception(f"Variabel '{arg}' tidak ditemukan")

                elif op == 'STORE_VAR':
                    value = self.stack.pop()
                    self.vars[arg] = value

                elif op == 'ADD':
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a + b)

                elif op == 'SUB':
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a - b)

                elif op == 'MUL':
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a * b)

                elif op == 'DIV':
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a / b if b != 0 else 0)

                elif op == 'MOD':
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a % b)

                elif op == 'EQ':
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a == b)

                elif op == 'NEQ':
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a != b)

                elif op == 'LT':
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a < b)

                elif op == 'GT':
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a > b)

                elif op == 'LTE':
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a <= b)

                elif op == 'GTE':
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(a >= b)

                elif op == 'PRINT':
                    value = self.stack.pop()
                    self.output.append(str(value))

                elif op == 'JUMP':
                    self.pc = arg

                elif op == 'JUMP_IF_FALSE':
                    condition = self.stack.pop()
                    if not condition:
                        self.pc = arg

                elif op == 'RETURN':
                    break  # Berhenti menjalankan

                elif op == 'NOT':
                    value = self.stack.pop()
                    self.stack.append(not value)

                else:
                    raise Exception(f"Unknown opcode: {op}")

            except Exception as e:
                raise Exception(f"Runtime error at instruction {self.pc-1} ({op}): {e}")

        return self.output

    def get_vars(self) -> dict:
        """Ambil status variabel (untuk debugging)"""
        return self.vars.copy()
