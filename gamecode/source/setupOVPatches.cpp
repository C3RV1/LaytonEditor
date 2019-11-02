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