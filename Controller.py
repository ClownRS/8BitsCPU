# 向ROM写入控制器指令

import os
from Pin import *
from Assembly import *

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Controller.bin')

micro = [CYC for _ in range(0x10000)] # 将所有指令初始化为CYC

CJMPS = [
    JMP,
    JO,
    JNO,
    JZ,
    JNZ,
    JP,
    JNP,
]

def get_cjmps_exec(exec, ins, psw):
    overflow = psw & 0x1
    zero = (psw >> 1) & 0x1
    parity = psw >> 2

    if ins == JMP:
        return exec
    if ins == JO and overflow:
        return exec
    if ins == JNO and not overflow:
        return exec
    if ins == JZ and zero:
        return exec
    if ins == JNZ and not zero:
        return exec
    if ins == JP and parity:
        return exec
    if ins == JNP and not parity:
        return exec
    return [CYC]

def compile_addr2(addr, ir, psw, index):
    global micro

    ins = ir >> 4 # 取高4位指令名

    if ins not in INSTRUCTIONS[2]:
        micro[addr] = CYC   # 如果指令不在指令集中，则将当前micro中的控制信号设为CYC
        return

    ins_dst = (ir >> 2) & 0x03 # 取目的操作数类型
    ins_src = ir & 0x03 # 取源操作数类型
    ins_ops = (ins_dst, ins_src) # 组合成一个元组
    if ins_ops not in INSTRUCTIONS[2][ins]:
        micro[addr] = CYC   # 如果操作数类型不是对应指令的合法操作数组合，则将当前micro中的控制信号设为CYC
        return

    # 将微操作序列中的微操作赋值给当前micro中的控制信号
    if index < len(INSTRUCTIONS[2][ins][ins_ops]):
        micro[addr] = INSTRUCTIONS[2][ins][ins_ops][index]

def compile_addr1(addr, ir, psw, index):
    global micro

    ins = (ir >> 2) # 取高6位指令名
    if ins not in INSTRUCTIONS[1]:
        micro[addr] = CYC
        return
    
    ins_op = ir & 0x03 # 取操作数类型
    if ins_op not in INSTRUCTIONS[1][ins]:
        micro[addr] = CYC
        return

    EXEC = INSTRUCTIONS[1][ins][ins_op]
    # 处理条件跳转指令，需要同时满足在OPS中和psw
    if ins in CJMPS:
        EXEC = get_cjmps_exec(EXEC, ins, psw)
    
    if index < len(EXEC):
        micro[addr] = EXEC[index]


def compile_addr0(addr, ir, psw, index):
    global micro

    ins = ir # 取全8位指令名
    if ins not in INSTRUCTIONS[0]:
        micro[addr] = CYC
        return
    
    if index < len(INSTRUCTIONS[0][ins]):
        micro[addr] = INSTRUCTIONS[0][ins][index]

with open(filename, 'wb') as file:
    for addr in range(0x10000):
        ir = addr >> 8 # 取高8位指令
        psw = (addr >> 4) & 0xF # 取低4位指令,这里要和0x0F相与去除高位
        cyc = addr & 0xF

        # 每一条指令的前六位都是取指操作
        if cyc < len(FETCH):
            micro[addr] = FETCH[cyc]
            continue

        # 如果cyc已经大于取指操作的长度，则进行指令操作
        ## 读取表示指令类型的位
        addr2 = ir >> 7
        addr1 = (ir >> 6) & 0x01

        # 获取去除取指操作后，当前micro位置的对应索引，方便编译时从微操作序列中获取微操作
        index = cyc - len(FETCH)

        if addr2:
            compile_addr2(addr, ir, psw, index)
        elif addr1:
            compile_addr1(addr, ir, psw, index)
        else:
            compile_addr0(addr, ir, psw, index)


    for var in micro:
        ins = var.to_bytes(4, byteorder='little') # 将micro的控制信号编码为2进制4字节数据
        file.write(ins)

print("Controller Compile Complete!")
