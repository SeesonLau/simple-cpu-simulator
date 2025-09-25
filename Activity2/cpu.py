from registers import Registers
from memory import Memory

class CPU:
    def __init__(self):
        self.registers = Registers()
        self.memory = Memory()
        self.halted = False
        self.execution_log = []
    
    def reset(self):
        self.registers.reset()
        self.memory.clear()
        self.halted = False
        self.execution_log = []
    
    def fetch(self):
        # MAR ← PC
        self.registers.MAR = self.registers.PC
        
        # MDR ← Memory[MAR] (get instruction)
        instruction = self.memory.get_instruction(self.registers.MAR)
        self.registers.MDR = instruction
        
        # IR ← MDR
        self.registers.IR = instruction
        
        # PC ← PC + 1
        self.registers.PC += 1
    
    def decode_execute(self):
        if not self.registers.IR or self.registers.IR.strip() == "" or self.halted:
            return

        instruction_parts = self.registers.IR.split()
        opcode = instruction_parts[0]

        if opcode == "HLT":
            self.halted = True
            self.execution_log.append(f"PC={self.registers.PC-1}\tIR={self.registers.IR}\tProgram Halted.")
            return

        if len(instruction_parts) < 2:
            self.execution_log.append(f"PC={self.registers.PC-1}\tIR={self.registers.IR}\tError: Missing operand")
            return

        try:
            address = int(instruction_parts[1])
        except ValueError:
            self.execution_log.append(f"PC={self.registers.PC-1}\tIR={self.registers.IR}\tError: Invalid address")
            return

        current_ac = self.registers.AC
        memory_value = self.memory.get_value(address)

        if opcode == "LOAD":
            self.registers.AC = memory_value
            self.execution_log.append(
                f"PC={self.registers.PC-1}\tIR={self.registers.IR}\tAC={current_ac}→{self.registers.AC}\t\t(loaded from memory[{address}]={memory_value})"
            )

        elif opcode == "STORE":
            old_value = self.memory.get_value(address)
            self.memory.set_data(address, self.registers.AC)
            new_value = self.memory.get_value(address)
            self.execution_log.append(
                f"PC={self.registers.PC-1}\tIR={self.registers.IR}\tMemory[{address}]={old_value}→{new_value}\t(stored from AC={self.registers.AC})"
            )

        elif opcode == "ADD":
            old_ac = self.registers.AC
            self.registers.AC += memory_value
            self.execution_log.append(
                f"PC={self.registers.PC-1}\tIR={self.registers.IR}\tAC={old_ac}→{self.registers.AC}\t\t(added memory[{address}]={memory_value})"
            )

        elif opcode == "SUB":
            old_ac = self.registers.AC
            self.registers.AC -= memory_value
            self.execution_log.append(
                f"PC={self.registers.PC-1}\tIR={self.registers.IR}\tAC={old_ac}→{self.registers.AC}\t\t(subtracted memory[{address}]={memory_value})"
            )

        else:
            self.execution_log.append(f"PC={self.registers.PC-1}\tIR={self.registers.IR}\tError: Unknown instruction")

    
    def run_cycle(self):
        if self.halted or self.registers.PC >= self.memory.size:
            return False
        
        self.fetch()
        self.decode_execute()
        return not self.halted
    
    def run_program(self):
        self.execution_log.clear()  # Clear previous logs
        self.execution_log.append("Starting program execution...")
        self.execution_log.append("=" * 60)
        
        while self.run_cycle():
            pass
        
        self.execution_log.append("=" * 60)
        self.execution_log.append("Program execution completed.")
        return self.execution_log
    