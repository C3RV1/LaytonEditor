#include "proflayton.h"
#include "string.h"

u32 Overlay = 0;
u32 OVChange_Offset = 0xDEADBEAF;

extern "C"
{
    extern void testHook_020eff3c();
    extern void testHook_020eff3c_end();
}

void arm9hook_0202492c()
{
    register u32 r1 asm("r1");
    Overlay = r1;
}

void patchoverlays()
{

    printf("Loaded Overlay %d", Overlay);
    u32 data0;
    u32 data1;
    u32 *original_ptr;
    u32 *ptr = (u32 *)OVChange_Offset;
    while ((data0 = *ptr++) != 0)
    {
        data1 = *ptr++;
        if (Overlay == (data0 >> 24))
        {
            original_ptr = (u32 *)((data0 & 0xffffff) | 0x02000000);
            *original_ptr = data1;
        }
    }
}

void ovnsub_43_020f78a8()
{
    register u32 r14 asm("r14");
    register u32 r0 asm("r0");
    register u32 r1 asm("r1");
    register u32 r2 asm("r2");
    register u32 r3 asm("r3");
    u32 r0str = r0;
    u32 r1str = r1;
    u32 r2str = r2;
    u32 r3str = r3;
    u32 r14str = r14;
    printf("ran function 1 from %x, r0: %x, r1: %x, r2: %x, r3: %x", r14str, r0str, r1str, r2str, r3str);
    for (;;)
        swiWaitForVBlank();
}

// FS_LoadOverlay End
void arm9hook_0202496c()
{
    patchoverlays();
}

// FS_LoadOverlay End
void arm9hook_0202495c()
{
    patchoverlays();
}

void arm9hook_02024980()
{
    register u32 r1 asm("r1");
    Overlay = r1;
    printf("Unloaded Overlay %d", Overlay);
}