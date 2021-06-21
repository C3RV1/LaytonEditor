#include <lt2.h>

/* Example Code Hack for the patcher */

OVHOOK(2, 0x02068ca4) {
    puts("Hello, World!\n");
}

// A hack that allows you to use the D-Pad to change the direction of the train

#define BG_SPEED *((s16*) 0x02088c90)

typedef struct
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
} ov9_data_t;

ov9_data_t *ov9_data;
bool direction = 1; // 0: left | 1: right
int bushspeed = 1;
int keys, keys_down;

void scan_keys()
{
	keys_down = (~REG_KEYINPUT) & ~keys;
	keys = ~REG_KEYINPUT;
}

OVHOOK(9, 0x020f0360)
{
    BG_SPEED = 2;
}

OVHOOK(2, 0x020efda8)
{
    register u32 r4 asm("r4");
    ov9_data = (ov9_data_t *)r4;
    printf("PDB: OV9 Data Addr: %x\n", (u32)ov9_data);
    scan_keys(); // Initialize
}

OVHOOK(9, 0x020f036c)
{
    scan_keys();
    if (keys_down & LEFT)
    {
        if (!direction)
        {
            direction = true;
            BG_SPEED = 2;
            bushspeed = 1;
        }
    }
    else if (keys_down & RIGHT)
    {
        if (direction)
        {
            direction = false;
            BG_SPEED = -2;
            bushspeed = -1;
        }
    }
}


OVREPL(9, 0x020f01b0) {
    asm("push {r1}");
    asm("mov r1, %0" :: "r" (bushspeed));
    asm("add r2, r0, r1");
    asm("pop {r1}");
}

OVREPL(9, 0x020eff94) {
    asm("mov r3, #0x90000000");
}