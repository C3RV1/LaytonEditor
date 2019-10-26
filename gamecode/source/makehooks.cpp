#include "makehooks.h"

u32 makeBranchOpCode(void *src, void *dest, bool wLink)
{
    u32 res = 0xEA000000;
    if (wLink)
        res |= 0x01000000;
    u32 offs = (((u32)dest) >> 2) - (((u32)src) >> 2) - 2;
    offs &= 0xFFFFFF;
    res |= offs;
    return res;
}

u32 hookAddress(u32 *address, void *hook)
{
    u32 opcode = makeBranchOpCode(address, hook, false);
    *address = opcode;
    return opcode;
}