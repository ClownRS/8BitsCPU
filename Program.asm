    MOV SS, 2
    MOV CS, 0
    MOV SP, 255
    MOV C, 255
    MOV D, 100

    PUSH [100]
    PUSH [C]

    POP [250]
    POP [D]

    HLT