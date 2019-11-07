.text
.global bushspeed

ovrepl_9_020eff3c:
    mov r3, #0x0
    mov r1, pc       @ Aweful code to get the right address
    add r1, #string 
    sub r1, #12
    bx lr

string:
    .string "title/title.bgx"

ovrepl_9_020f01b0:
    push {r1}
    ldr r1, #bushspeed
    add r2,r0,r1
    pop {r1}
    bx lr

bushspeed:
    .word 0x1

@ fixes bug with track not looping
ovrepl_9_020eff94:
    mov r3, #0x90000000
    bx lr
