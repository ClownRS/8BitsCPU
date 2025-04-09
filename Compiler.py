# 汇编指令编译器。

import os
import re

from Assembly import *
from Pin import *
from Controller import *

dirname = os.path.dirname(__file__)
sourceFile = os.path.join(dirname, 'Program.asm')
outputFile = os.path.join(dirname, 'Program.bin')

program = []
codes = []
marks = {}

OPS = {
    'MOV': MOV,
    'ADD': ADD,
    'SUB': SUB,
    'INC': INC,
    'DEC': DEC,
    'AND': AND,
    'OR': OR,
    'XOR': XOR,
    'NOT': NOT,
    'HLT': HLT,
    'NOP': NOP,
    'JMP': JMP,
    'JO': JO,
    'JNO': JNO,
    'JZ': JZ,
    'JNZ': JNZ,
    'JP': JP,
    'JNP': JNP,
    'CMP': CMP,
}

# 获取所有寻址类型
AMS = {
    'AM_IMM': AM_IMM,
    'AM_REG': AM_REG,
    'AM_DIR': AM_DIR,
    'AM_IND': AM_IND,
}

REGISTERS = {
    'A': A,
    'B': B,
    'C': C,
    'D': D,
}

class SyntaxError(Exception):
    def __init__(self, line_num, source, *args, **kwargs):
        self.line_num = line_num
        self.source = source

    def print_error(self):
        print(f"Syntax Error at line {self.line_num}: {self.source}")

class Code(object):
    CODE = 0
    LABEL = 1

    def __init__(self, line_num, source):
        self.line_num = line_num
        self.source = source
        self.op_type = 2
        self.type = None
        self.op = None
        self.dst = None
        self.src = None
        self.name = None
        self.prepare_source()

    # 定义toString()
    def __repr__(self):
        return f"[{self.line_num}] - {self.source}"

    # 获取指令名的机器编码
    def get_op(self):
        return OPS[self.op]

    # 获取操作数类型的机器编码
    def get_am_type(self, am):
        # 立即数判断
        if re.match(r'^\d+$', am):
            return AM_IMM

        # 寄存器判断
        elif re.match(r'^[a-zA-Z]$', am):
            return AM_REG

        # 直接寻址判断
        elif re.match(r'^\[\d+\]$', am):
            return AM_DIR

        # 间接寻址判断
        elif re.match(r'^\[[a-zA-Z]\]$', am):
            return AM_IND
        else:
            raise SyntaxError(self.line_num, self.source)

    # 获取操作数的机器编码
    def get_am(self, am_type, am):
        if am_type == AM_IMM:
            return int(am, 10)
        elif am_type == AM_REG:
            return REGISTERS[am]

        elif am_type == AM_DIR:
            return int(re.search(r'\[(.+)\]', am).group(1), 10)

        elif am_type == AM_IND:
            return REGISTERS[re.search(r'\[(.+)\]', am).group(1)]
        else:
            raise SyntaxError(self.line_num, self.source)

    def prepare_source(self):
        if self.source.endswith(':'):
            self.type = self.LABEL
            self.name = self.source.split(':')[0]
        else:
            self.type = self.CODE
            # 取指令三部分
            # 判断是否有源操作数
            matches = re.split(r', ', self.source)
            # 若matches等于source，分割失败，说明操作数小于等于1
            if matches[0] == self.source:
                self.src = None
                self.op_type = 1
            else:
                self.src = matches[1]

            rest = matches[0]
            matches = re.split(r' ', rest)
            # 判断是否有目的操作数
            if matches[0] == self.source:
                self.dst = None
                self.op_type = 0
            else:
                self.dst = matches[1]

            self.op = matches[0]
            if self.op not in OPS:
                raise SyntaxError(self.line_num, self.source)
    
    # 将汇编指令编译成机器码
    def compile(self):
        if self.type == self.CODE:
            op = self.get_op()
            dst_type, src_type = 0b00, 0b00
            dst, src = 0x00, 0x00
            if op in CJMPS:
                # 检查操作数是否合法
                if self.src != None or self.dst == None:
                    raise SyntaxError(self.line_num, self.source)

                dst = marks[self.dst]
                dst_type = AM_IMM
                ins_type = (op << ADDR1_SHIFT) | dst_type
            else:
                # 前8位指令
                ins_type = 0x00
                # 获取目的操作数类型的机器编码
                if self.op_type != 0:
                    dst_type = self.get_am_type(self.dst)
                    dst = self.get_am(dst_type, self.dst)
                if self.op_type == 2:
                    src_type = self.get_am_type(self.src)
                    src = self.get_am(src_type, self.src)

                # 检查操作数组合是否合法
                if self.op_type == 2:
                    ams_type = (dst_type, src_type)
                    if ams_type not in INSTRUCTIONS[self.op_type][op]:
                        raise SyntaxError(self.line_num, self.source)
                elif self.op_type == 1:
                    am_type = dst_type
                    if am_type not in INSTRUCTIONS[self.op_type][op]:
                        raise SyntaxError(self.line_num, self.source)
                elif self.op_type == 0:
                    if op not in INSTRUCTIONS[self.op_type]:
                        raise SyntaxError(self.line_num, self.source)
                else:
                    raise SyntaxError(self.line_num, self.source)

                # 转换为机器编码
                if self.op_type == 2:
                    ins_type = (op << ADDR2_SHIFT) | (dst_type << ADDR1_SHIFT) | src_type
                elif self.op_type == 1:
                    ins_type = (op << ADDR1_SHIFT) | dst_type
                elif self.op_type == 0:
                    ins_type = op
                else:
                    raise SyntaxError(self.line_num, self.source)
                
            program.append(ins_type)
            program.append(dst)
            program.append(src)

def compile_program():
    with open(sourceFile, 'r', encoding='UTF-8') as file:
        lines = file.readlines()

        for index, line in enumerate(lines):
            source = line.strip()
            # 获取非空行
            if not source:
                continue

            # 去掉注释
            if ';' in source:
                source = source.split(';')[0].strip()
                # 如果该行只有注释，跳过
                if not source:
                    continue

            code = Code(index + 1, source)
            codes.append(code)

    # 当前最近一个还未找到标记地址的标记
    current_label = None
    # 当前代码对应的索引
    current_index = 0
    for code in codes:
        # 如果是标记地址，那么该标记地址当前未找到对应地址
        if code.type == code.LABEL:
            current_label = code
        elif code.type == code.CODE:
            if current_label != None:
                marks[current_label.name] = current_index
                current_label = None
            current_index += 3

    # 编译
    for code in codes:
        code.compile()

    # 写入
    with open(outputFile, 'wb') as file:
        for val in program:
            bin = val.to_bytes(1, byteorder='little')
            file.write(bin)

def main():
    try:
        compile_program()
    except SyntaxError as e:
        e.print_error()
        return
    print("Assembly Compile Complete!")

if __name__ == "__main__":
    main()