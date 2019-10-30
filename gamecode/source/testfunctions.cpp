#include "proflayton.h"
#include "string.h"

u32 OV9_TEST = 0;
u32 Overlay = 0;
u32 OVChange_Offset = 0xDEADBEAF;

extern "C"
{
    extern void testHook_020eff3c();
    extern void testHook_020eff3c_end();
}

inline bool OV9_ispatched()
{
    return (*((u32 *)0x020eff3c) == OV9_TEST);
}

// void hook_0201c090()
// {
//     if ((*((u32 *)0x020efda0) == 0xe92d4078) & (not OV9_ispatched()))
//     {
//         OV9_TEST = hookAndBack((u32 *)0x020eff3c, (u32 *)&testHook_020eff3c, (u32 *)&testHook_020eff3c_end);
//         nocashMessage("Press A to continue...");
//         waitForUserInput(KEY_A);
//         nocashMessage("Patched Overlay 9!");
//     }
//     nocashMessage("Run from hook!");
// }

void arm9hook_0202492c()
{
    register u32 r1 asm("r1");
    Overlay = r1;
    //asm ("mov %%r1, %0" : "=r" (Overlay) );
}

void patchoverlays()
{

    printf("Loaded Overlay %d", Overlay);
    u32 data0;
    u32 data1;
    u32*original_ptr;
    u32*ptr = (u32*) OVChange_Offset;
    while((data0 = *ptr++) != 0)
    {
        data1 = *ptr++;
        if (Overlay == (data0 >> 24))
        {
            original_ptr = (u32*)((data0&0xffffff)|0x02000000);
            *original_ptr = data1;
        }
    }
}

void ovhook_9_020eff18()
{
    printf("hooked!");
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