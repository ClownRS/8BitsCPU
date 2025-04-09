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
SUB = ADDR2 | 0x02
AND = ADDR2 | 0x03
OR = ADDR2 | 0x04
XOR = ADDR2 | 0x05
CMP = ADDR2 | 0x06

## 一地址指令
INC = ADDR1 | 0x00
DEC = ADDR1 | 0x01
NOT = ADDR1 | 0x02
JMP = ADDR1 | 0x03
JO = ADDR1 | 0x04
JNO = ADDR1 | 0x05
JZ = ADDR1 | 0x06
JNZ = ADDR1 | 0x07
JP = ADDR1 | 0x08
JNP = ADDR1 | 0x09
PUSH = ADDR1 | 0x0A
POP = ADDR1 | 0x0B
CALL = ADDR1 | 0x0C

## 零地址指令
NOP = 0x00
RET = 0x01
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
        },
        ADD: {
            (AM_REG, AM_IMM): [
                SRC_OUT | A_IN,
                DR | B_IN,
                ALU_OUT | ADD_OP | PSW_OUT | DW,
            ],
            (AM_REG, AM_REG): [
                SR | A_IN,
                DR | B_IN,
                ALU_OUT | ADD_OP | PSW_OUT | DW,
            ],
            (AM_REG, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | A_IN,
                DR | B_IN,
                ALU_OUT | ADD_OP | PSW_OUT | DW,
            ],
            (AM_REG, AM_IND): [
                SR | MAR_IN,
                MC_OUT | A_IN,
                DR | B_IN,
                ALU_OUT | ADD_OP | PSW_OUT | DW,
            ],
            (AM_DIR, AM_IMM): [
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                SRC_OUT | A_IN,
                ALU_OUT | ADD_OP | PSW_OUT | MC_IN,
            ],
            (AM_DIR, AM_REG): [
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                SR | A_IN,
                ALU_OUT | ADD_OP | PSW_OUT | MC_IN,
            ],
            (AM_DIR, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | A_IN,
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | ADD_OP | PSW_OUT | MC_IN,
            ],
            (AM_DIR, AM_IND): [
                SR | MAR_IN,
                MC_OUT | A_IN,
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | ADD_OP | PSW_OUT | MC_IN,
            ],
            (AM_IND, AM_IMM): [
                SRC_OUT | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | ADD_OP | PSW_OUT | MC_IN,
            ],
            (AM_IND, AM_REG): [
                SR | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | ADD_OP | PSW_OUT | MC_IN,
            ],
            (AM_IND, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | ADD_OP | PSW_OUT | MC_IN,
            ],
            (AM_IND, AM_IND): [
                SR | MAR_IN,
                MC_OUT | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | ADD_OP | PSW_OUT | MC_IN,
            ]

        },
        SUB: {
            (AM_REG, AM_IMM): [
                SRC_OUT | B_IN,
                DR | A_IN,
                ALU_OUT | SUB_OP | PSW_OUT | DW,
            ],
            (AM_REG, AM_REG): [
                SR | B_IN,
                DR | A_IN,
                ALU_OUT | SUB_OP | PSW_OUT | DW,
            ],
            (AM_REG, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | B_IN,
                DR | A_IN,
                ALU_OUT | SUB_OP | PSW_OUT | DW,
            ],
            (AM_REG, AM_IND): [
                SR | MAR_IN,
                MC_OUT | B_IN,
                DR | A_IN,
                ALU_OUT | SUB_OP | PSW_OUT | DW,
            ],
            (AM_DIR, AM_IMM): [
                DST_OUT | MAR_IN,
                MC_OUT | A_IN,
                SRC_OUT | B_IN,
                ALU_OUT | SUB_OP | PSW_OUT | MC_IN,
            ],
            (AM_DIR, AM_REG): [
                DST_OUT | MAR_IN,
                MC_OUT | A_IN,
                SR | B_IN,
                ALU_OUT | SUB_OP | PSW_OUT | MC_IN,
            ],
            (AM_DIR, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | B_IN,
                DST_OUT | MAR_IN,
                MC_OUT | A_IN,
                ALU_OUT | SUB_OP | PSW_OUT | MC_IN,
            ],
            (AM_DIR, AM_IND): [
                SR | MAR_IN,
                MC_OUT | B_IN,
                DST_OUT | MAR_IN,
                MC_OUT | A_IN,
                ALU_OUT | SUB_OP | PSW_OUT | MC_IN,
            ],
            (AM_IND, AM_IMM): [
                SRC_OUT | B_IN,
                DR | MAR_IN,
                MC_OUT | A_IN,
                ALU_OUT | SUB_OP | PSW_OUT | MC_IN,
            ],
            (AM_IND, AM_REG): [
                SR | B_IN,
                DR | MAR_IN,
                MC_OUT | A_IN,
                ALU_OUT | SUB_OP | PSW_OUT | MC_IN,
            ],
            (AM_IND, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | B_IN,
                DR | MAR_IN,
                MC_OUT | A_IN,
                ALU_OUT | SUB_OP | PSW_OUT | MC_IN,
            ],
            (AM_IND, AM_IND): [
                SR | MAR_IN,
                MC_OUT | B_IN,
                DR | MAR_IN,
                MC_OUT | A_IN,
                ALU_OUT | SUB_OP | PSW_OUT | MC_IN,
            ]
        },
        AND: {
            (AM_REG, AM_IMM): [
                SRC_OUT | A_IN,
                DR | B_IN,
                ALU_OUT | AND_OP | DW,
            ],
            (AM_REG, AM_REG): [
                SR | A_IN,
                DR | B_IN,
                ALU_OUT | AND_OP | DW,
            ],
            (AM_REG, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | A_IN,
                DR | B_IN,
                ALU_OUT | AND_OP | DW,
            ],
            (AM_REG, AM_IND): [
                SR | MAR_IN,
                MC_OUT | A_IN,
                DR | B_IN,
                ALU_OUT | AND_OP | DW,
            ],
            (AM_DIR, AM_IMM): [
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                SRC_OUT | A_IN,
                ALU_OUT | AND_OP | MC_IN,
            ],
            (AM_DIR, AM_REG): [
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                SR | A_IN,
                ALU_OUT | AND_OP | MC_IN,
            ],
            (AM_DIR, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | A_IN,
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | AND_OP | MC_IN,
            ],
            (AM_DIR, AM_IND): [
                SR | MAR_IN,
                MC_OUT | A_IN,
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | AND_OP | MC_IN,
            ],
            (AM_IND, AM_IMM): [
                SRC_OUT | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | AND_OP | MC_IN,
            ],
            (AM_IND, AM_REG): [
                SR | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | AND_OP | MC_IN,
            ],
            (AM_IND, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | AND_OP | MC_IN,
            ],
            (AM_IND, AM_IND): [
                SR | MAR_IN,
                MC_OUT | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | AND_OP | MC_IN,
            ]
        },
        OR: {
            (AM_REG, AM_IMM): [
                SRC_OUT | A_IN,
                DR | B_IN,
                ALU_OUT | OR_OP | DW,
            ],
            (AM_REG, AM_REG): [
                SR | A_IN,
                DR | B_IN,
                ALU_OUT | OR_OP | DW,
            ],
            (AM_REG, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | A_IN,
                DR | B_IN,
                ALU_OUT | OR_OP | DW,
            ],
            (AM_REG, AM_IND): [
                SR | MAR_IN,
                MC_OUT | A_IN,
                DR | B_IN,
                ALU_OUT | OR_OP | DW,
            ],
            (AM_DIR, AM_IMM): [
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                SRC_OUT | A_IN,
                ALU_OUT | OR_OP | MC_IN,
            ],
            (AM_DIR, AM_REG): [
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                SR | A_IN,
                ALU_OUT | OR_OP | MC_IN,
            ],
            (AM_DIR, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | A_IN,
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | OR_OP | MC_IN,
            ],
            (AM_DIR, AM_IND): [
                SR | MAR_IN,
                MC_OUT | A_IN,
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | OR_OP | MC_IN,
            ],
            (AM_IND, AM_IMM): [
                SRC_OUT | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | OR_OP | MC_IN,
            ],
            (AM_IND, AM_REG): [
                SR | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | OR_OP | MC_IN,
            ],
            (AM_IND, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | OR_OP | MC_IN,
            ],
            (AM_IND, AM_IND): [
                SR | MAR_IN,
                MC_OUT | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | OR_OP | MC_IN,
            ]
        },
        XOR: {
            (AM_REG, AM_IMM): [
                SRC_OUT | A_IN,
                DR | B_IN,
                ALU_OUT | XOR_OP | DW,
            ],
            (AM_REG, AM_REG): [
                SR | A_IN,
                DR | B_IN,
                ALU_OUT | XOR_OP | DW,
            ],
            (AM_REG, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | A_IN,
                DR | B_IN,
                ALU_OUT | XOR_OP | DW,
            ],
            (AM_REG, AM_IND): [
                SR | MAR_IN,
                MC_OUT | A_IN,
                DR | B_IN,
                ALU_OUT | XOR_OP | DW,
            ],
            (AM_DIR, AM_IMM): [
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                SRC_OUT | A_IN,
                ALU_OUT | XOR_OP | MC_IN,
            ],
            (AM_DIR, AM_REG): [
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                SR | A_IN,
                ALU_OUT | XOR_OP | MC_IN,
            ],
            (AM_DIR, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | A_IN,
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | XOR_OP | MC_IN,
            ],
            (AM_DIR, AM_IND): [
                SR | MAR_IN,
                MC_OUT | A_IN,
                DST_OUT | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | XOR_OP | MC_IN,
            ],
            (AM_IND, AM_IMM): [
                SRC_OUT | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | XOR_OP | MC_IN,
            ],
            (AM_IND, AM_REG): [
                SR | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | XOR_OP | MC_IN,
            ],
            (AM_IND, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | XOR_OP | MC_IN,
            ],
            (AM_IND, AM_IND): [
                SR | MAR_IN,
                MC_OUT | A_IN,
                DR | MAR_IN,
                MC_OUT | B_IN,
                ALU_OUT | XOR_OP | MC_IN,
            ]
        },
        CMP: {
            (AM_REG, AM_IMM): [
                SRC_OUT | B_IN,
                DR | A_IN,
                SUB_OP | PSW_OUT,
            ],
            (AM_REG, AM_REG): [
                SR | B_IN,
                DR | A_IN,
                SUB_OP | PSW_OUT,
            ],
            (AM_REG, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | B_IN,
                DR | A_IN,
                SUB_OP | PSW_OUT,
            ],
            (AM_REG, AM_IND): [
                SR | MAR_IN,
                MC_OUT | B_IN,
                DR | A_IN,
                SUB_OP | PSW_OUT,
            ],
            (AM_DIR, AM_IMM): [
                DST_OUT | MAR_IN,
                MC_OUT | A_IN,
                SRC_OUT | B_IN,
                SUB_OP | PSW_OUT,
            ],
            (AM_DIR, AM_REG): [
                DST_OUT | MAR_IN,
                MC_OUT | A_IN,
                SR | B_IN,
                SUB_OP | PSW_OUT,
            ],
            (AM_DIR, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | B_IN,
                DST_OUT | MAR_IN,
                MC_OUT | A_IN,
                SUB_OP | PSW_OUT,
            ],
            (AM_DIR, AM_IND): [
                SR | MAR_IN,
                MC_OUT | B_IN,
                DST_OUT | MAR_IN,
                MC_OUT | A_IN,
                SUB_OP | PSW_OUT,
            ],
            (AM_IND, AM_IMM): [
                SRC_OUT | B_IN,
                DR | MAR_IN,
                MC_OUT | A_IN,
                SUB_OP | PSW_OUT,
            ],
            (AM_IND, AM_REG): [
                SR | B_IN,
                DR | MAR_IN,
                MC_OUT | A_IN,
                SUB_OP | PSW_OUT,
            ],
            (AM_IND, AM_DIR): [
                SRC_OUT | MAR_IN,
                MC_OUT | B_IN,
                DR | MAR_IN,
                MC_OUT | A_IN,
                SUB_OP | PSW_OUT,
            ],
            (AM_IND, AM_IND): [
                SR | MAR_IN,
                MC_OUT | B_IN,
                DR | MAR_IN,
                MC_OUT | A_IN,
                SUB_OP | PSW_OUT,
            ]
        }
    },
    # 一地址指令
    1: {
        INC: {
            AM_REG: [
                DR | A_IN,
                ALU_OUT | PSW_OUT | INC_OP | DW,
            ],
            AM_DIR: [
                DST_OUT | MAR_IN,
                MC_OUT | A_IN,
                ALU_OUT | PSW_OUT | INC_OP | MC_IN,
            ],
            AM_IND: [
                DR | MAR_IN,
                MC_OUT | A_IN,
                ALU_OUT | PSW_OUT | INC_OP | MC_IN,
            ]
        },
        DEC: {
            AM_REG: [
                DR | A_IN,
                ALU_OUT | PSW_OUT | DEC_OP | DW,
            ],
            AM_DIR: [
                DST_OUT | MAR_IN,
                MC_OUT | A_IN,
                ALU_OUT | PSW_OUT | DEC_OP | MC_IN,
            ],
            AM_IND: [
                DR | MAR_IN,
                MC_OUT | A_IN,
                ALU_OUT | PSW_OUT | DEC_OP | MC_IN,
            ]
        },
        NOT: {
            AM_REG: [
                DR | A_IN,
                ALU_OUT | NOT_OP | DW,
            ],
            AM_DIR: [
                DST_OUT | MAR_IN,
                MC_OUT | A_IN,
                ALU_OUT | NOT_OP | MC_IN,
            ],
            AM_IND: [
                DR | MAR_IN,
                MC_OUT | A_IN,
                ALU_OUT | NOT_OP | MC_IN,
            ]
        },
        JMP: {
            AM_IMM: [
                DST_OUT | PC_IN,
            ]
        },
        JO: {
            AM_IMM: [
                DST_OUT | PC_IN,
            ]
        },
        JNO: {
            AM_IMM: [
                DST_OUT | PC_IN,
            ]
        },
        JZ: {
            AM_IMM: [
                DST_OUT | PC_IN,
            ]
        },
        JNZ: {
            AM_IMM: [
                DST_OUT | PC_IN,
            ]
        },
        JP: {
            AM_IMM: [
                DST_OUT | PC_IN,
            ]
        },
        JNP: {
            AM_IMM: [
                DST_OUT | PC_IN,
            ]
        },
        PUSH: {
            AM_IMM: [
                SS_OUT | MSR_IN,
                SP_OUT | MAR_IN,
                DST_OUT | MC_IN,
                SP_OUT | A_IN,
                ALU_OUT | DEC_OP | SP_IN,
                CS_OUT | MSR_IN,
            ],
            AM_REG: [
                SS_OUT | MSR_IN,
                SP_OUT | MAR_IN,
                DR | MC_IN,
                SP_OUT | A_IN,
                ALU_OUT | DEC_OP | SP_IN,
                CS_OUT | MSR_IN,
            ],
            AM_DIR: [
                DST_OUT | MAR_IN,
                MC_OUT | T1_IN,
                SS_OUT | MSR_IN,
                SP_OUT | MAR_IN,
                T1_OUT | MC_IN,
                SP_OUT | A_IN,
                ALU_OUT | DEC_OP | SP_IN,
                CS_OUT | MSR_IN,
            ],
            AM_IND: [
                DR | MAR_IN,
                MC_OUT | T1_IN,
                SS_OUT | MSR_IN,
                SP_OUT | MAR_IN,
                T1_OUT | MC_IN,
                SP_OUT | A_IN,
                ALU_OUT | DEC_OP | SP_IN,
                CS_OUT | MSR_IN,
            ]
        },
        POP: {
            AM_REG: [
                SP_OUT | A_IN,
                ALU_OUT | INC_OP | SP_IN,
                SS_OUT | MSR_IN,
                SP_OUT | MAR_IN,
                MC_OUT | DW,
                CS_OUT | MSR_IN,
            ],
            AM_DIR: [
                SP_OUT | A_IN,
                ALU_OUT | INC_OP | SP_IN,
                SS_OUT | MSR_IN,
                SP_OUT | MAR_IN,
                MC_OUT | T1_IN,
                CS_OUT | MSR_IN,
                DST_OUT | MAR_IN,
                T1_OUT | MC_IN,
            ],
            AM_IND: [
                SP_OUT | A_IN,
                ALU_OUT | INC_OP | SP_IN,
                SS_OUT | MSR_IN,
                SP_OUT | MAR_IN,
                MC_OUT | T1_IN,
                CS_OUT | MSR_IN,
                DR | MAR_IN,
                T1_OUT | MC_IN,
            ]
        },
        CALL: {
            AM_IMM: [
                SS_OUT | MSR_IN,
                SP_OUT | MAR_IN,
                PC_OUT | MC_IN,
                DST_OUT | PC_IN,
                SP_OUT | A_IN,
                ALU_OUT | DEC_OP | SP_IN,
                CS_OUT | MSR_IN,
            ]
        }
    },
    # 零地址指令
    0: {
        NOP: [
            CYC,
        ],
        RET: [
            SP_OUT | A_IN,
            ALU_OUT | INC_OP | SP_IN,
            SS_OUT | MSR_IN,
            SP_OUT | MAR_IN,
            MC_OUT | PC_IN,
            CS_OUT | MSR_IN,
        ],
        HLT: [
            HALT,
        ],
    },
}