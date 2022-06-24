import os

class Buffer():
    def __init__(self, endianess: str, architecture: str):
        self.executed = False
        self.stack = []
        self.buf = []
        self.input = ""
        self.endianess = endianess
        self.architecture = architecture

        ip = []
        bp = []
        if architecture == "x32":
            ip = ["ca", "fe", "f0", "0d"]
            bp = ["de", "ad", "be", "ef"]
        elif architecture == "x64":
            ip = ["ca", "fe", "ba", "be", "ca", "5s", "ad", "ed"]
            bp = ["de", "ad", "be", "ef", "ba", "1d", "fa", "ce"]

        if endianess == "little":
            self.stack.extend(ip)
            self.stack.extend(bp)
        elif endianess == "big":
            for i in range(len(ip) - 1, -1, -1):
                self.stack.append(ip[i])
            for i in range(len(bp) - 1, -1, -1):
                self.stack.append(bp[i])
        self.set_buf(1)

    def add_to_buf(self, byte):
        self.buf.append(byte)

    def set_buf(self, buf_size):
        self.buf.clear()
        stack_save = 0
        if self.architecture == "x32":
            stack_save = 7
        elif self.architecture == "x64":
            stack_save = 15
        for i in range(len(self.stack) - 1, stack_save, -1):
            if i is not stack_save:
                self.stack.pop(i)
        for j in range(0, buf_size):
            self.buf.append("90")
        self.stack.extend(self.buf)

    def set_input(self, input):
        self.input = input

    def buffer_overflow(self):
        self.executed = True
        input_len = len(self.input)
        if self.endianess == "big":
            for a in range(0, input_len):
                index = (len(self.stack) - 1) - a
                if index == -1:
                    break
                hx = hex(ord(self.input[a]))
                hx = hx[2:]
                self.stack[index] = hx
        elif self.endianess == "little":
            char_index = input_len - 1
            for a in range(0, len(self.input)):
                index = (len(self.stack) - 1) - a
                if index == -1:
                    break
                hx = hex(ord(self.input[char_index]))
                char_index -= 1
                hx = hx[2:]
                self.stack[index] = hx

    def get_registers(self):  
        ip = ""
        bp = ""
        if self.architecture == "x32":
            ip = "EIP = "
            bp = "EBP = "
            if self.endianess == "little":
                for i in range(0, 4):
                    ip += self.stack[i]
                for i in range(4, 8):
                    bp += self.stack[i]
            elif self.endianess == "big":
                for i in range(3, -1, -1):
                    ip += self.stack[i]
                for i in range(7, 3, -1):
                    bp += self.stack[i]
        elif self.architecture == "x64":
            ip = "RIP = "
            bp = "RBP = "
            if self.endianess == "little":
                for i in range(0, 8):
                    ip += self.stack[i]
                for i in range(8, 16):
                    bp += self.stack[i]
            elif self.endianess == "big":
                for i in range(7, -1, -1):
                    ip += self.stack[i]
                for i in range(15, 7, -1):
                    bp += self.stack[i]
        return ip + "\n" + bp

    def get_stack(self):
        s = ""
        mem_addr = 0
        if self.architecture == "x32":
            mem_addr = 0xf7fb5870
        elif self.architecture == "x64":
            mem_addr = 0x0000000000fb5870
        s += "Object   Value   Memory \n"
        
        r = self.get_registers().split()
        if r:
            r.pop(0)
            r.pop(0)
            r.pop(1)
            r.pop(1)

            if self.architecture == "x32":
                s += f"EIP   {r[0]}   {hex(mem_addr)} \n"
                mem_addr -= 4
                s += f"EBP   {r[1]}   {hex(mem_addr)} \n"
                mem_addr -= 4
            elif self.architecture == "x64":
                s += f"RIP   {r[0]}   {format(mem_addr, '#018x')} \n"
                mem_addr -= 8
                s += f"RBP   {r[1]}   {format(mem_addr, '#018x')} \n"
                mem_addr -= 8

        b = len(self.stack) - len(self.buf) - 1
        for a in range((len(self.stack) - 1) - (len(self.stack) - len(self.buf)), -1, -1):
            b += 1
            if self.architecture == "x32":
                s += f"Buf[{a}]   {self.stack[b]}   {hex(mem_addr)} \n"
            elif self.architecture == "x64":
                s += f"Buf[{a}]   {self.stack[b]}   {format(mem_addr, '#018x')} \n"
            mem_addr -= 4
        return s

    def get_program_view(self):
        s = ""
        user = os.environ.get('USER', os.environ.get('USERNAME'))
        if self.executed == False:
            s += f"{user}@machine: ~/home$ \n" 
        else:
            s += f"{user}@machine: ~/home$ ./program\n"
            s += "Hello :D\n"
            s += "Enter Value: "
            s += self.input + "\n"
        
        if self.executed == True and len(self.input) > len(self.buf):
            s += "Segmentation fault (core dumped)\n"
            s += f"{user}@machine: ~/home$"
        elif self.executed == True:
            s += "Goodbye :)\n"
            s += f"{user}@machine: ~/home$"
        return s

    def get_code_view(self):
        s = ""
        s += "# include <stdio.h>\n\n"
        s += "int main()\n"
        s += "{\n"
        s += "    int bufSize = " + str(len(self.buf)) + ";\n\n"
        s += '    printf("Hello :D");\n'
        s += '    printf("Enter value: ");\n\n'
        s += "    char buf[bufSize];\n"
        s += "    gets(buf);\n\n"
        s += '    printf("Goodbye :)");\n'
        s += "}"
        return s