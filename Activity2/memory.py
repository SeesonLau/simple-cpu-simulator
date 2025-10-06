class Memory:
    def __init__(self, size=256):
        self.size = size
        self.data = [0] * size
        self.instructions = [""] * size
        self.is_instruction = [False] * size
    
    def clear(self):
        self.data = [0] * self.size
        self.instructions = [""] * self.size
        self.is_instruction = [False] * self.size
    
    def set_instruction(self, address, instruction):
        if 0 <= address < self.size:
            self.instructions[address] = instruction
            self.is_instruction[address] = True
    
    def set_data(self, address, value):
        if 0 <= address < self.size:
            self.data[address] = value
    
    def get_value(self, address):
        if 0 <= address < self.size:
            return self.data[address]
        return 0
    
    def get_instruction(self, address):
        if 0 <= address < self.size:
            return self.instructions[address]
        return ""
    
    def is_instruction_address(self, address):
        if 0 <= address < self.size:
            return self.is_instruction[address]
        return False
    
    def get_memory_dump(self, start=0, end=10):
        """Debug method to see memory contents"""
        result = []
        for addr in range(start, min(end, self.size)):
            if self.is_instruction[addr]:
                result.append(f"Address {addr}: INSTRUCTION = '{self.instructions[addr]}'")
            else:
                result.append(f"Address {addr}: DATA = {self.data[addr]}")
        return result
    