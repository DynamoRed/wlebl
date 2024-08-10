class BrainfuckInterpreter:
    def __init__(self, code):
        self.code = code
        self.tape = [0] * 30000
        self.pointer = 0
        self.code_pointer = 0
        self.loop_stack = []
        self.output = ""

    def run(self):
        while self.code_pointer < len(self.code):
            char = self.code[self.code_pointer]

            if char == '>':
                self.pointer += 1
            elif char == '<':
                self.pointer -= 1
            elif char == '+':
                self.tape[self.pointer] = (self.tape[self.pointer] + 1) % 256
            elif char == '-':
                self.tape[self.pointer] = (self.tape[self.pointer] - 1) % 256
            elif char == '.':
                self.output += chr(self.tape[self.pointer])
            elif char == ',':
                # Assuming input is handled here; in practice, you'd get it from the user
                self.tape[self.pointer] = ord(input("Input: ")[0])
            elif char == '[':
                if self.tape[self.pointer] == 0:
                    self.jump_forward()
                else:
                    self.loop_stack.append(self.code_pointer)
            elif char == ']':
                if self.tape[self.pointer] != 0:
                    self.code_pointer = self.loop_stack[-1]
                else:
                    self.loop_stack.pop()

            self.code_pointer += 1

        return self.output

    def jump_forward(self):
        open_brackets = 1
        while open_brackets != 0:
            self.code_pointer += 1
            if self.code[self.code_pointer] == '[':
                open_brackets += 1
            elif self.code[self.code_pointer] == ']':
                open_brackets -= 1

def main(filename):
    with open(filename, 'r') as file:
        code = file.read()

    interpreter = BrainfuckInterpreter(code)
    output = interpreter.run()
    print(output)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <filename>")
    else:
        main(sys.argv[1])
