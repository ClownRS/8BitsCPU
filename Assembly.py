from Pin import *

FETCH = [
    PC_OUT | MAR_IN,
    MC_OUT | IR_IN | PC_INC,
    PC_OUT | MAR_IN,
    MC_OUT | DST_IN | PC_INC,
    PC_OUT | MAR_IN,
    MC_OUT | SRC_IN | PC_INC,
]

# 定义操作数类型
AM_IMM = 0b00  # 立即数寻址
AM_REG = 0b01  # 寄存器寻址
AM_DIR = 0b10  # 直接寻址
AM_IND = 0b11  # 间接寻址

# 定义指令类型
ADDR2 = 1 << 3
ADDR1 = 1 << 4

# 定义指令类型的偏移位数
ADDR2_SHIFT = 4
ADDR1_SHIFT = 2

# 定义指令操作
## 二地址指令
MOV = ADDR2 | 0x00
ADD = ADDR2 | 0x01

## 一地址指令

## 零地址指令
NOP = 0x00
HLT = 0x3F

INSTRUCTIONS = {
    # 二地址指令
    2: {
        ## 指令名
        MOV: {
            ### 操作数类型
            (AM_REG, AM_IMM): [
                SRC_OUT | DW,
            ],
            (AM_REG, AM_REG): [
                SR | DW,
            ],
            (AM_REG, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | DW,
            ],
            (AM_REG, AM_IND): [
                SR | MAR_IN,
                MC_OUT | DW,
            ],
            (AM_DIR, AM_IMM): [
                DST_OUT | MAR_IN,
                SRC_OUT | MC_IN,
            ],
            (AM_DIR, AM_REG): [
                DST_OUT | MAR_IN,
                SR | MC_IN
            ],
            (AM_DIR, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | T1_IN,
                DST_OUT | MAR_IN,
                T1_OUT | MC_IN
            ],
            (AM_DIR, AM_IND): [
                SR | MAR_IN,
                MC_OUT | T1_IN,
                DST_OUT | MAR_IN,
                T1_OUT | MC_IN
            ],
            (AM_IND, AM_IMM): [
                DR | MAR_IN,
                SRC_OUT | MC_IN
            ],
            (AM_IND, AM_REG): [
                DR | MAR_IN,
                SR | MC_IN
            ],
            (AM_IND, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | T1_IN,
                DR | MAR_IN,
                T1_OUT | MC_IN
            ],
            (AM_IND, AM_IND): [
                SR | MAR_IN,
                MC_OUT | T1_IN,
                DR | MAR_IN,
                T1_OUT | MC_IN
            ]
        }
    },
    # 一地址指令
    1: {
    },
    # 零地址指令
    0: {
        NOP: [
            CYC,
        ],
        HLT: [
            HALT,
        ],
    },
}