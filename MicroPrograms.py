import os

### 本脚本用于为微程序编码。

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'MicroPrograms.bin')

# Register A(input) Control
WE_A = 2 ** 0
CS_A = 2 ** 1

# Register B(input) Control
WE_B = 2 ** 2
CS_B = 2 ** 3

# ALU Control
ALU_ADD = 0
ALU_SUB = 2 ** 4
ALU_OUT = 2 ** 5

# Register C(output) Control
WE_C = 2 ** 6
CS_C = 2 ** 7

# Memory Address Control
WE_PC = 2 ** 8
CS_PC = 2 ** 9
EN_PC = 2 ** 10

# Memory Controller Control
WE_M = 2 ** 11
CS_M = 2 ** 12

# Halt Control
HLT = 2 ** 15

# Microprograms

# 将A寄存器和B寄存器的值存入内存中，再将相加的结果C寄存器存入内存中
micro = [
    WE_A | CS_A | WE_PC | CS_PC | EN_PC | CS_M,  #从内存中读出第一个数字A
    WE_B | CS_B | WE_PC | CS_PC | EN_PC | CS_M,  #从内存中读出第二个数字B 
    ALU_ADD | WE_C | CS_C,  #将相加的结果存入C寄存器
    CS_C | WE_PC | CS_PC | EN_PC | CS_M | WE_M,  #将C寄存器的值存入内存中
    HLT  #停止执行
]

with open(filename, 'wb') as file:
    for value in micro:
        binary = value.to_bytes(2, byteorder='little')  #将整数转换为2字节的二进制数据(编码)
        file.write(binary)
        print(binary)
print("Compile Complete!")