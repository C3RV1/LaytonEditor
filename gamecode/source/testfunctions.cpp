#include "proflayton.h"

typedef struct arm9data
{
    u32 *data_start_spr;
    u32 *data_continue_spr;
    u32 *data_secret_spr;
    u32 *unk_c;
    u32 *data_waku_spr;
    u32 *data_train_spr;
    u32 *data_senro_spr;
    u32 *data_load_save_backup;
    u32 waku_offs;
} arm9data_t;

arm9data_t *dataptr;
bool go_left = 0;

extern "C"
{
    extern u32 bushspeed;
}

void ovhook_9_020f0360()
{
    short *bgspd = PTR_TITLESCREEN_BG_SPEED;
    *bgspd = 2;
}

void ovhook_9_020efda8() // Not in ov9 but the right ov is loaded anyway
{
    register u32 r4 asm("r4");
    dataptr = (arm9data_t *)r4;
    printf("dataptr: %x", (u32)dataptr);
}

void ovhook_9_020f036c()
{
    myScanKeys();
    if (myKeysDown() & LEFT)
    {
        if (not go_left)
        {
            go_left = true;
            short *bgspd = PTR_TITLESCREEN_BG_SPEED;
            *bgspd = 2;
            bushspeed = 1;
        }
    }
    else if (myKeysDown() & RIGHT)
    {
        if (go_left)
        {
            go_left = false;
            *(PTR_TITLESCREEN_BG_SPEED) = -2;
            bushspeed = -1;
        }
    }
}