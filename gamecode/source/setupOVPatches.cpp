#include "proflayton.h"
#include "string.h"

u32 Overlay = 0;
u32 OVChange_Offset = 0xDEADBEAF;
u32 LoadedOverlays0 = 0x0;
u32 LoadedOverlays1 = 0x0;

extern "C"
{
    extern void testHook_020eff3c();
    extern void testHook_020eff3c_end();
}

void set_overlay_enabled(int ov)
{
    if (ov < 32)
    {
        LoadedOverlays0 |= 1 << ov;
    }
    else
    {
        LoadedOverlays1 |= 1 << (ov - 32);
    }
}

void set_overlay_disabled(int ov)
{
    if (ov < 32)
    {
        LoadedOverlays0 &= ~(1 << ov);
    }
    else
    {
        LoadedOverlays1 &= ~(1 << (ov - 32));
    }
}

void print_enabled_overlays()
{
    char final[200] = "Overlays loaded: ";
    char *finalptr = final;
    finalptr += strlen(final);
    char buffer[20];
    int ov = 0;
    while (ov < 32)
    {
        if (LoadedOverlays0 & (1 << ov))
        {
            sprintf(buffer, "%d ", ov);
            strcpy(finalptr, buffer);
            finalptr += strlen(buffer);
        }
        ov++;
    }
    while (ov < 64)
    {
        if (LoadedOverlays0 & (1 << ov))
        {
            sprintf(buffer, "%d ", ov);
            strcpy(finalptr, buffer);
            finalptr += strlen(buffer);
        }
        ov++;
    }
    *finalptr++ = 0;
    printf(final);
}

void arm9hook_0202492c(u32 param1, u32 param2)
{
    Overlay = param2;
}

void patchoverlays()
{

    printf("Loaded Overlay %d", Overlay);
    set_overlay_enabled(Overlay);
    print_enabled_overlays();
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

void arm9hook_02024980(u32 param1, u32 param2)
{
    // register u32 r1 asm("r1");
    // Overlay = r1;
    printf("Unloaded Overlay %d", param2);
    set_overlay_disabled(param2);
    print_enabled_overlays();
}