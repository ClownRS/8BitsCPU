INIT:
    MOV SS, 0x02
    MOV CS, 0
    MOV SP, 0xFF
    MOV C, 1
    JMP START

FUNC:
    MOV D, 255
    IRET
    
START:
    MOV D, C
    INC C
    CLI
    INT FUNC
    CMP C, 0x8
    JZ END
    JMP START

END:
    HLT