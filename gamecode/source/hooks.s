.text
.global testHook_020eff3c
.global testHook_020eff3c_end

ovrepl_9_020eff3c:
    mov r3, #0x0
    mov r1, pc       @ Aweful code to get the right address
    add r1, #string 
    sub r1, #12
    bx lr

string:
    .string "title/title_sub.bgx"