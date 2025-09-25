class Validator:
    @staticmethod
    def validate_instruction_count(count, max_memory=256):
        try:
            count = int(count)
            if count <= 0 or count > max_memory:
                return False, f"Instruction count must be between 1 and {max_memory}"
            return True, count
        except ValueError:
            return False, "Instruction count must be a valid integer"
    
    @staticmethod
    def validate_address(address, max_memory=256):
        try:
            address = int(address)
            if address < 0 or address >= max_memory:
                return False, f"Address must be between 0 and {max_memory-1}"
            return True, address
        except ValueError:
            return False, "Address must be a valid integer"
    
    @staticmethod
    def validate_data_value(value):
        try:
            value = int(value)
            return True, value
        except ValueError:
            return False, "Data value must be a valid integer"
    
    @staticmethod
    def check_duplicate_instructions(instructions):
        used_addresses = set()
        duplicates = []
        
        for addr, instr in instructions.items():
            if instr and addr in used_addresses:
                duplicates.append(addr)
            elif instr:
                used_addresses.add(addr)
        
        return len(duplicates) == 0, duplicates
    