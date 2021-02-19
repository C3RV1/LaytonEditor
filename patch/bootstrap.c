#include <stdint.h>

void* patch_address = (void*) CODEADDR;
uint32_t patch_lenght = CODELEN + 4;
extern void * _end;

void MIi_CpuCopy32(void *src, void *dest, uint32_t len);

void bootstrap()
{
    // Copy the patch to the correct address.
    MIi_CpuCopy32(&_end, patch_address, patch_lenght);
    asm(".long 0xe3a0c301 "); // mov %r12, #0x04000000: The replaced instruction at 0x02000800
}