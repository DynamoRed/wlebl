class BefungeInterpreter:
    def __init__(self, code):
        self.code = [list(line) for line in code.splitlines()]
        self.stack = []
        self.direction = (0, 1)
        self.position = (0, 0)
        self.output = ""

    def run(self):
        while True:
            x, y = self.position
            char = self.code[x][y]

            if char == '"':
                self.toggle_string_mode()
            elif char.isdigit():
                self.stack.append(int(char))
            elif char in "><v^":
                self.change_direction(char)
            elif char == "+":
                self.binary_op(lambda a, b: a + b)
            elif char == "-":
                self.binary_op(lambda a, b: b - a)
            elif char == "*":
                self.binary_op(lambda a, b: a * b)
            elif char == "/":
                self.binary_op(lambda a, b: b // a if a != 0 else 0)
            elif char == "%":
                self.binary_op(lambda a, b: b % a if a != 0 else 0)
            elif char == "!":
                self.stack.append(0 if self.pop_safe() else 1)
            elif char == "`":
                self.binary_op(lambda a, b: 1 if b > a else 0)
            elif char == "_":
                self.direction = (0, 1 if self.pop_safe() == 0 else -1)
            elif char == "|":
                self.direction = (1 if self.pop_safe() == 0 else -1, 0)
            elif char == ":":
                if len(self.stack) == 0:
                    self.stack.append(0)
                else:
                    self.stack.append(self.stack[-1])
            elif char == "\\":
                if len(self.stack) < 2:
                    self.stack.append(0)
                else:
                    a = self.pop_safe()
                    b = self.pop_safe()
                    self.stack.append(a)
                    self.stack.append(b)
            elif char == "$":
                self.pop_safe()
            elif char == ".":
                self.output += str(self.pop_safe())
            elif char == ",":
                self.output += chr(self.pop_safe())
            elif char == "#":
                self.move()
            elif char == "@":
                break
            else:
                pass

            self.move()

        return self.output

    def toggle_string_mode(self):
        self.move()
        while True:
            x, y = self.position
            char = self.code[x][y]
            if char == '"':
                break
            self.stack.append(ord(char))
            self.move()
        self.move()

    def change_direction(self, char):
        if char == ">":
            self.direction = (0, 1)
        elif char == "<":
            self.direction = (0, -1)
        elif char == "v":
            self.direction = (1, 0)
        elif char == "^":
            self.direction = (-1, 0)

    def binary_op(self, op):
        if len(self.stack) < 2:
            self.stack.append(0)
        else:
            a = self.pop_safe()
            b = self.pop_safe()
            self.stack.append(op(a, b))

    def pop_safe(self):
        return self.stack.pop() if len(self.stack) > 0 else 0

    def move(self):
        x, y = self.position
        dx, dy = self.direction
        self.position = (x + dx, y + dy)

def main(filename):
    with open(filename, 'r') as file:
        code = file.read()

    interpreter = BefungeInterpreter(code)
    output = interpreter.run()
    print(output)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: py interpreter.py <filename>")
    else:
        main(sys.argv[1])
