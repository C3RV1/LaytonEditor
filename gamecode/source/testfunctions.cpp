#include "proflayton.h"

u32 OV9_TEST = 0;


extern "C"
{
    extern void testHook_020eff3c();
    extern void testHook_020eff3c_end();
}

inline bool OV9_ispatched()
{
    return (*((u32*)0x020eff3c) == OV9_TEST);
}

void hook_0201c090()
{
    if ((*((u32 *)0x020efda0) == 0xe92d4078) & (not OV9_ispatched()))
    {
        OV9_TEST = hookAndBack((u32*) 0x020eff3c, (u32*) &testHook_020eff3c, (u32* ) &testHook_020eff3c_end);
        nocashMessage("Press A to continue...");
        waitForUserInput(KEY_A);
        nocashMessage("Patched Overlay 9!");
    }
    nocashMessage("Run from hook!");
}