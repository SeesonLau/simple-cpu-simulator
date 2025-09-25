class Registers:
    def __init__(self):
        self.AC = 0  # Accumulator
        self.PC = 0  # Program Counter
        self.IR = ""  # Instruction Register
        self.MAR = 0  # Memory Address Register
        self.MDR = 0  # Memory Data Register
    
    def reset(self):
        self.AC = 0
        self.PC = 0
        self.IR = ""
        self.MAR = 0
        self.MDR = 0
    
    def __str__(self):
        return f"AC={self.AC}, PC={self.PC}, IR={self.IR}, MAR={self.MAR}, MDR={self.MDR}"
        