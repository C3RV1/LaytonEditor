MIi_CpuCopy32 = 0x0202092c;

FS_InitFile = 0x02023be8;
FS_OpenFile = 0x02023ec8;
FS_ReadFile = 0x0202401c;
FS_CloseFile = 0x02023f10;
FS_SeekFile = 0x0202402c;
FS_OpenFileFast = 0x02023e58;

OS_CreateThread = 0x0201ded0;
OS_WakeupThreadDirect = 0x0201e26c;
OS_SetTimer = 0x0201d564;
OS_SetIRQFunction = 0x0201d408;
OS_EnableIRQ = 0x0201d5d8;

OS_Malloc = 0x0203d6c4;
OS_Free = 0x0203d728;
OS_Malloc2 = 0x0203d73c;
OS_Free2 = 0x0203d728;

snd_setup = 0x0207fb54;
snd_stop = 0x0207fbcc;
snd_start = 0x0207fbdc;

sqm_load = 0x0207f780;
sqm_started = 0x0207fa78;
sqm_update_something = 0x0206ce18;
sqm_get_sfx_type = 0x0207f850;
sqm_play_sfx = 0x0207f8f0;

button_init = 0x0208003c;
button_update = 0x02080300;
button_draw = 0x020805e0;
button_pressed = 0x02080690;
button_destroy = 0x02080158;

sprite_set_animation = 0x02075d10;
sprite_find_animation = 0x02075c04;
sprite_init = 0x020758fc;
sprite_draw = 0x02075e50;
sprite_set_animation_name = 0x02075dd4;
sprite_destroy = 0x02075978;
sprite_sub_init = 0x02076324;
sprite_sub_draw = 0x02076534;
sprite_sub_draw2 = 0x020764a4;
sprite_sub_destroy = 0x02076364;
sprite_get_width = 0x02075cc0;
sprite_get_height = 0x02075c70;

load_background = 0x0206ffec;
load_background_sub = 0x0207064c;

update_graphics = 0x0206cfb8;

touch_update = 0x0206c7b4;
touch_is_pressed = 0x0206e1e4;
touch_is_down = 0x0206e20c;
touch_get_location = 0x0206e288;
touch_is_released = 0x0206e1f8;

point_in_area = 0x0206ae10;

text_show_centered = 0x02072e34;
text_show = 0x020731b8;
text_clear = 0x02072a2c;

plz_load_file = 0x0206c8b8;
plz_read_file = 0x0206bdd4;
load_file_compressed = 0x0206c230;

draw_box = 0x02070e8c;