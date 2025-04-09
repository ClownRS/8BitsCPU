    MOV SS, 0x02
    MOV CS, 0
    MOV SP, 0xFF
    MOV C, 255
    MOV D, 100

    PUSH [0xEE]
    PUSH [C]

    POP [0xFE]
    POP [D]

    HLT