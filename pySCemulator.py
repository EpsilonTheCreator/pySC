import sys
import pygame

# Define the number of registers
NUM_REGISTERS = 4

# Helper function to convert byte to binary string
def byte_to_bin(byte):
    return f'{byte:08b}'

# Load program into memory
def load_program(filename):
    with open(filename, 'rb') as f:
        program = f.read()
    return bytearray(program)

# Emulator class
class Emulator:
    def __init__(self, memory, memory_size):
        self.registers = [0] * NUM_REGISTERS
        self.memory = memory + bytearray(memory_size - len(memory))  # Allocate memory size
        self.pc = 0  # Program counter
        self.running = True
        self.display = None
        self.display_resolution = (640, 480)
        self.text_position = [10, 10]  # Initial text position
        pygame.init()
        self.font = pygame.font.SysFont("Courier", 24)  # Monospaced font, size 24
        self.init_display()

    def fetch(self):
        if self.pc < len(self.memory):
            opcode = self.memory[self.pc]
            self.pc += 1
            return opcode
        return None

    def execute(self, opcode):
        print(f"Executing opcode: {opcode:02X}")  # Debug statement
        if opcode == 0x00:  # halt
            self.running = False
        elif opcode == 0x06:  # set
            reg = self.memory[self.pc]
            value = int.from_bytes(self.memory[self.pc + 1:self.pc + 3], byteorder='big')
            self.pc += 3
            self.registers[reg - 10] = value
            print(f"Set register {reg - 10} to {value}")  # Debug statement
        elif opcode == 0x07:  # setstr
            reg = self.memory[self.pc]
            address = self.pc + 1
            string = ''
            while self.memory[address] != 0:
                string += chr(self.memory[address])
                address += 1
            self.pc = address + 1
            self.registers[reg - 10] = string
            print(f"Set register {reg - 10} to string: {string}")  # Debug statement
        elif opcode == 0x05:  # int
            int_code = self.memory[self.pc]
            self.pc += 1
            print(f"Interrupt with code: {int_code:02X}")  # Debug statement
            self.interrupt(int_code)
        else:
            print(f"Unknown opcode: {opcode:02X}")  # Debug statement

    def interrupt(self, code):
        if code == 0x01:  # Shut down
            self.running = False
            print("Shut down")  # Debug statement
        elif code == 0x06:  # Set resolution
            self.display_resolution = (self.registers[0], self.registers[1])
            print(f"Set resolution to {self.display_resolution}")  # Debug statement
            self.init_display()
        elif code == 0x07:  # Print string
            reg = self.registers[0]
            if isinstance(reg, str):
                print(f"Printing string from register: {reg}")  # Debug statement
                self.print_to_screen(reg)
            else:
                print(f"Register does not contain a string: {reg}")  # Debug statement
        else:
            print(f"Unknown interrupt code: {code:02X}")  # Debug statement

    def init_display(self):
        print(f"Initializing display with resolution: {self.display_resolution}")  # Debug statement
        # Ensure resolution is within reasonable bounds
        if not (0 < self.display_resolution[0] <= 1920 and 0 < self.display_resolution[1] <= 1080):
            print("Invalid resolution, resetting to default (640, 480)")
            self.display_resolution = (640, 480)
        self.display = pygame.display.set_mode(self.display_resolution)
        pygame.display.set_caption('pySC Emulator')
        self.display.fill((0, 0, 0))  # Clear the screen
        self.text_position = [10, 10]  # Reset text position

    def print_to_screen(self, string):
        print(f"Displaying string on screen: {string}")  # Debug statement
        lines = self.wrap_text(string, self.font, self.display_resolution[0] - 20)  # Adjust for margins
        for line in lines:
            text_surface = self.font.render(line, True, (255, 255, 255))
            self.display.blit(text_surface, self.text_position)
            self.update_text_position(text_surface.get_size())
        pygame.display.update()

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            test_width, test_height = font.size(test_line)
            if test_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)  # Append the last line
        return lines

    def update_text_position(self, text_size):
        x, y = self.text_position
        y += text_size[1]
        if y > self.display_resolution[1]:
            y = 10
            self.display.fill((0, 0, 0))  # Clear screen if text overflows
        self.text_position = [x, y]
        print(f"Updated text position to: {self.text_position}")  # Debug statement

    def run(self):
        while True:  # Keep the window open
            if self.running and self.pc < len(self.memory):
                opcode = self.fetch()
                if opcode is not None:
                    self.execute(opcode)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()

# Main function to load and run the emulator
def main():
    if len(sys.argv) != 3:
        print("Usage: py pySCemulator.py <binary_file> <memory_size>")
        sys.exit(1)

    binary_file = sys.argv[1]
    memory_size = int(sys.argv[2])
    memory = load_program(binary_file)
    emulator = Emulator(memory, memory_size)
    emulator.run()

if __name__ == "__main__":
    main()
