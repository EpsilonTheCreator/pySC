import sys

# Define opcodes
OPCODES = {
    'halt': '00000000',
    'addnum': '00000001',
    'subnum': '00000010',
    'mulnum': '00000011',
    'divnum': '00000100',
    'int': '00000101',
    'set': '00000110',
    'setstr': '00000111',  # New opcode for setting strings
    'memamount': '00001000',
    'memset': '00001001',
    'lfd': '00001101',
    'bootdev': '00001110',
    'if': '00001111',
    'section': '00010000'
}

# Helper function to convert binary string to byte
def bin_to_byte(binary_string):
    return int(binary_string, 2).to_bytes(1, byteorder='big')

# Compiler function
def compile_code(source_file, output_file):
    with open(source_file, 'r') as f:
        lines = f.readlines()

    binary_program = bytearray()

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # Ignore empty lines and comments

        parts = line.split(maxsplit=2)
        opcode = parts[0]

        if opcode in OPCODES:
            binary_program.append(bin_to_byte(OPCODES[opcode])[0])

            if opcode == 'set':
                if len(parts) < 3:
                    print(f"Error: 'set' instruction requires a register and a value. Line: {line}")
                    continue
                try:
                    reg = parts[1]
                    if reg.startswith('R'):
                        reg_num = int(reg[1:])
                    else:
                        reg_num = ord(reg) - 65
                    reg = reg_num + 10
                    binary_program.append(bin_to_byte(f'{reg:08b}')[0])
                    value = parts[2]
                    if not (value.startswith('"') and value.endswith('"')):
                        value = int(value)
                        binary_program.extend(value.to_bytes(2, byteorder='big'))
                    else:
                        print(f"Error: 'set' instruction does not support strings. Use 'setstr' for strings. Line: {line}")
                        continue
                except ValueError as e:
                    print(f"Error parsing 'set' instruction. Line: {line}. Error: {e}")
                    continue
            elif opcode == 'setstr':
                if len(parts) < 3:
                    print(f"Error: 'setstr' instruction requires a register and a string. Line: {line}")
                    continue
                try:
                    reg = parts[1]
                    if reg.startswith('R'):
                        reg_num = int(reg[1:])
                    else:
                        reg_num = ord(reg) - 65
                    reg = reg_num + 10
                    binary_program.append(bin_to_byte(f'{reg:08b}')[0])
                    value = parts[2]
                    if value.startswith('"') and value.endswith('"'):
                        string_value = value.strip('"')
                        binary_program.extend(string_value.encode('utf-8'))
                        binary_program.append(0)  # Null-terminate the string
                    else:
                        print(f"Error: 'setstr' instruction requires a string value. Line: {line}")
                        continue
                except ValueError as e:
                    print(f"Error parsing 'setstr' instruction. Line: {line}. Error: {e}")
                    continue
            elif opcode == 'int':
                if len(parts) < 2:
                    print(f"Error: 'int' instruction requires an interrupt code. Line: {line}")
                    continue
                try:
                    int_code = int(parts[1], 16)  # Parse hex value
                    binary_program.append(int_code)
                except ValueError as e:
                    print(f"Error parsing 'int' instruction. Line: {line}. Error: {e}")
                    continue
            elif opcode == 'memset':
                if len(parts) < 3:
                    print(f"Error: 'memset' instruction requires an address and a value. Line: {line}")
                    continue
                address = int(parts[1])
                data = int(parts[2])
                binary_program.extend(address.to_bytes(2, byteorder='big'))
                binary_program.append(data)
            elif opcode == 'if':
                if len(parts) < 3:
                    print(f"Error: 'if' instruction requires a condition and a value. Line: {line}")
                    continue
                condition = int(parts[1])
                value = int(parts[2])
                binary_program.append(bin_to_byte(f'{condition:08b}')[0])
                binary_program.append(value)
            else:
                pass  # Handle other opcodes if necessary

    with open(output_file, 'wb') as f:
        f.write(binary_program)

    print(f"Compiled {source_file} to {output_file}")

# Main function
def main():
    if len(sys.argv) != 3:
        print("Usage: python pySCcompiler.py <source_file> <output_file>")
        sys.exit(1)

    source_file = sys.argv[1]
    output_file = sys.argv[2]
    compile_code(source_file, output_file)

if __name__ == "__main__":
    main()
