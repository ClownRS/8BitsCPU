MAIN:
    MOV C, 1
    MOV D, 2

    CMP C, D
    JO MAX
    JMP STOP
MAX:
    MOV A, 3

STOP:
    HLT