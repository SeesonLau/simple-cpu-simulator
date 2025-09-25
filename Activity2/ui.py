import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QTableWidget, QTableWidgetItem, 
                             QTextEdit, QMessageBox, QGroupBox, QSpinBox,
                             QHeaderView, QScrollArea)
from PyQt5.QtCore import Qt

class CPUApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cpu = None
        self.instruction_addresses = []
        self.data_addresses = set()
        self.data_inputs = {}  # Store references to data input widgets
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Simple Sison CPU Simulator")
        self.setGeometry(100, 100, 1000, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Setup phase
        setup_group = QGroupBox("Program Setup")
        setup_layout = QVBoxLayout(setup_group)
        
        # Instruction count input
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Number of Instructions:"))
        self.instruction_count = QSpinBox()
        self.instruction_count.setRange(1, 256)
        self.instruction_count.setValue(4)
        count_layout.addWidget(self.instruction_count)
        count_layout.addStretch()
        
        setup_btn_layout = QHBoxLayout()
        self.setup_btn = QPushButton("Setup Instructions")
        self.setup_btn.clicked.connect(self.setup_instructions)
        setup_btn_layout.addWidget(self.setup_btn)
        
        setup_layout.addLayout(count_layout)
        setup_layout.addLayout(setup_btn_layout)
        
        # Instructions table
        self.instructions_table = QTableWidget()
        self.instructions_table.setColumnCount(3)
        self.instructions_table.setHorizontalHeaderLabels(["Address", "Instruction", "Operand"])
        setup_layout.addWidget(self.instructions_table)
        
        # Data values input
        self.data_group = QGroupBox("Data Values")
        self.data_layout = QVBoxLayout(self.data_group)
        setup_layout.addWidget(self.data_group)
        self.data_group.hide()
        
        # Execution phase
        execution_group = QGroupBox("Execution")
        execution_layout = QVBoxLayout(execution_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.run_btn = QPushButton("Run Program")
        self.run_btn.clicked.connect(self.run_program)
        self.step_btn = QPushButton("Step")
        self.step_btn.clicked.connect(self.step_program)
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_program)
        
        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.step_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addStretch()
        
        execution_layout.addLayout(btn_layout)
        
        # Output
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        execution_layout.addWidget(self.output_text)
        
        layout.addWidget(setup_group)
        layout.addWidget(execution_group)
        
        self.step_btn.setEnabled(False)
        self.run_btn.setEnabled(False)
        self.reset_btn.setEnabled(False)
    
    def clear_data_inputs(self):
        """Safely clear all data input widgets"""
        # Remove all widgets from data layout
        for i in reversed(range(self.data_layout.count())):
            item = self.data_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
        
        self.data_inputs.clear()
    
    def setup_instructions(self):
        from validator import Validator
        
        count = self.instruction_count.value()
        
        # Clear previous setup
        self.instruction_addresses = list(range(count))
        self.data_addresses.clear()
        self.clear_data_inputs()
        
        # Setup instructions table
        self.instructions_table.setRowCount(count)
        
        instruction_types = ["", "LOAD", "STORE", "ADD", "SUB", "HLT"]
        
        for row, address in enumerate(self.instruction_addresses):
            # Address column
            addr_item = QTableWidgetItem(str(address))
            addr_item.setFlags(addr_item.flags() & ~Qt.ItemIsEditable)
            self.instructions_table.setItem(row, 0, addr_item)
            
            # Instruction combobox
            instr_combo = QComboBox()
            instr_combo.addItems(instruction_types)
            instr_combo.currentTextChanged.connect(lambda text, r=row: self.on_instruction_change(r, text))
            self.instructions_table.setCellWidget(row, 1, instr_combo)
            
            # Operand input
            operand_edit = QLineEdit()
            operand_edit.setPlaceholderText("Address")
            operand_edit.textChanged.connect(lambda text, r=row: self.on_operand_change(r, text))
            self.instructions_table.setCellWidget(row, 2, operand_edit)
            operand_edit.setEnabled(False)
        
        self.instructions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.step_btn.setEnabled(True)
        self.run_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)
    
    def on_instruction_change(self, row, instruction):
        operand_edit = self.instructions_table.cellWidget(row, 2)
        if instruction in ["LOAD", "STORE", "ADD", "SUB"]:
            operand_edit.setEnabled(True)
            operand_edit.setPlaceholderText("Data Address")
        else:
            operand_edit.setEnabled(False)
            operand_edit.clear()
            self.update_data_inputs()
    
    def on_operand_change(self, row, operand):
        # Update data addresses set
        old_addresses = self.data_addresses.copy()
        self.data_addresses.clear()
        
        # Collect all valid operands
        for r in range(self.instructions_table.rowCount()):
            instr_combo = self.instructions_table.cellWidget(r, 1)
            instruction = instr_combo.currentText()
            if instruction in ["LOAD", "STORE", "ADD", "SUB"]:
                operand_edit = self.instructions_table.cellWidget(r, 2)
                operand_text = operand_edit.text().strip()
                if operand_text:
                    try:
                        address = int(operand_text)
                        self.data_addresses.add(address)
                    except ValueError:
                        pass
        
        # Only update if addresses changed
        if self.data_addresses != old_addresses:
            self.update_data_inputs()
    
    def update_data_inputs(self):
        """Update data input fields based on current data addresses"""
        self.clear_data_inputs()
        
        if not self.data_addresses:
            self.data_group.hide()
            return
        
        self.data_group.show()
        self.data_group.setTitle(f"Data Values (Addresses: {sorted(self.data_addresses)})")
        
        sorted_addresses = sorted(self.data_addresses)
        for address in sorted_addresses:
            layout = QHBoxLayout()
            layout.addWidget(QLabel(f"Address {address}:"))
            data_edit = QLineEdit()
            data_edit.setPlaceholderText("Value")
            data_edit.setText("0")
            data_edit.setProperty("address", address)
            self.data_inputs[address] = data_edit
            layout.addWidget(data_edit)
            layout.addStretch()
            
            # Create container widget for the layout
            container = QWidget()
            container.setLayout(layout)
            self.data_layout.addWidget(container)
    
    def get_program_data(self):
        from validator import Validator
        
        # Get instructions
        instructions = {}
        data_addresses_used = set()  # Track addresses used in instructions
        
        for row in range(self.instructions_table.rowCount()):
            instr_combo = self.instructions_table.cellWidget(row, 1)
            instruction = instr_combo.currentText()
            address = int(self.instructions_table.item(row, 0).text())
            
            if instruction:
                if instruction in ["LOAD", "STORE", "ADD", "SUB"]:
                    operand_edit = self.instructions_table.cellWidget(row, 2)
                    operand = operand_edit.text().strip()
                    if not operand:
                        QMessageBox.warning(self, "Error", f"Missing operand for instruction at address {address}")
                        return None, None
                    
                    valid, operand_val = Validator.validate_address(operand)
                    if not valid:
                        QMessageBox.warning(self, "Error", f"Invalid operand at address {address}: {operand_val}")
                        return None, None
                    
                    instructions[address] = f"{instruction} {operand_val}"
                    data_addresses_used.add(operand_val)  # Track this data address
                else:
                    instructions[address] = instruction
        
        # Check for duplicates
        valid, duplicates = Validator.check_duplicate_instructions(instructions)
        if not valid:
            QMessageBox.warning(self, "Error", f"Duplicate instructions at addresses: {duplicates}")
            return None, None
        
        # Get data values - only for addresses that are actually used
        data_values = {}
        for address in data_addresses_used:
            if address in self.data_inputs:
                data_edit = self.data_inputs[address]
                value = data_edit.text().strip()
                if value:
                    valid, value_val = Validator.validate_data_value(value)
                    if not valid:
                        QMessageBox.warning(self, "Error", f"Invalid data value at address {address}: {value_val}")
                        return None, None
                    data_values[address] = value_val
                else:
                    data_values[address] = 0  # Default value
            else:
                # If no input field exists, use default value
                data_values[address] = 0
        
        # Debug: Show what we're loading
        print(f"Instructions: {instructions}")
        print(f"Data values: {data_values}")
        
        return instructions, data_values
    
    def run_program(self):
        from cpu import CPU
        from memory import Memory
        
        instructions, data_values = self.get_program_data()
        if instructions is None:
            return
        
        # Initialize CPU and memory
        self.cpu = CPU()
        
        # Load instructions into memory
        for address, instruction in instructions.items():
            self.cpu.memory.set_instruction(address, instruction)
        
        # Load data into memory
        for address, value in data_values.items():
            self.cpu.memory.set_data(address, value)
        
        # Run program
        self.cpu.run_program()
        
        # Display results
        self.output_text.clear()
        for line in self.cpu.execution_log:
            self.output_text.append(line)
    
    def step_program(self):
        from cpu import CPU
        from memory import Memory
        
        if self.cpu is None:
            instructions, data_values = self.get_program_data()
            if instructions is None:
                return
            
            self.cpu = CPU()
            
            for address, instruction in instructions.items():
                self.cpu.memory.set_instruction(address, instruction)
            
            for address, value in data_values.items():
                self.cpu.memory.set_data(address, value)
        
        if not self.cpu.halted:
            self.cpu.run_cycle()
            self.output_text.clear()
            for line in self.cpu.execution_log:
                self.output_text.append(line)
    
    def reset_program(self):
        self.cpu = None
        self.output_text.clear()
        self.setup_instructions()