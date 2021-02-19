#include <nds.h>

#ifndef _NSMB_H
#define _NSMB_H

typedef u8 FSFile[0x48];
typedef u8 OSThread[0xC0];
typedef unsigned char undefined;
typedef unsigned char undefined1;
typedef unsigned short undefined2;
typedef unsigned int undefined4;

struct sprite_t
{
	int field_0x0;
	int field_0x4;
	int field_0x8;
	undefined field_0xc;
	undefined field_0xd;
	undefined field_0xe;
	undefined field_0xf;
	undefined field_0x10;
	undefined field_0x11;
	undefined field_0x12;
	undefined field_0x13;
	short x;
	short y;
	undefined field_0x18;
	undefined field_0x19;
	undefined field_0x1a;
	undefined field_0x1b;
	undefined field_0x1c;
	undefined field_0x1d;
	undefined field_0x1e;
	undefined field_0x1f;
};

struct button_t
{
	int x;
	int y;
	int width;
	int height;
	int sfx;
	undefined field_0x14;
	undefined field_0x15;
	undefined field_0x16;
	undefined field_0x17;
	undefined field_0x18;
	undefined field_0x19;
	undefined field_0x1a;
	undefined field_0x1b;
	struct sprite_t *sprite;
	undefined field_0x20;
	undefined field_0x21;
	undefined field_0x22;
	undefined field_0x23;
	undefined field_0x24;
	undefined field_0x25;
	undefined field_0x26;
	undefined field_0x27;
	int animation_off; /* Created by retype action */
	int animation_on;  /* Created by retype action */
	undefined field_0x30;
	undefined field_0x31;
	undefined field_0x32;
	undefined field_0x33;
	undefined field_0x34;
	undefined field_0x35;
	undefined field_0x36;
	undefined field_0x37;
};

typedef struct
{
	u8 unk[0x30];
} sprite_sub_t;

#ifdef __cplusplus
extern "C"
{
#endif
	// Allocating and freeing
	void FreeSomething(void *ptr);
	void *AllocSomething(u32 size);

	void *AllocBytes(u32 size);
	void FreeBytes(void *ptr);

	// Files
	void FS_InitFile(FSFile *p_file);
	void FS_CloseFile(FSFile *p_file);
	s32 FS_ReadFile(FSFile *p_file, void *dst, s32 len);
	s32 FS_OpenFile(FSFile *p_file, const char *filename);
	bool FS_SeekFile(FSFile *p_file, s32 offset, int origin);
	bool FS_OpenFileFast(FSFile *p_file, u32 archivePtr, int file_id);

	//Threading funcs
	void OS_CreateThread(OSThread *thread, void (*func)(void *), void *arg, void *stack, u32 stackSize, u32 prio);
	void OS_WakeupThreadDirect(OSThread *thread);

	// Sound
	void setupsound(void *ptr_sounddata, u32 p2unki, u32 stream_n, s32 p4ni, u32 p5ni);
	void stopsound(void *ptr_sounddata, u32 p2unki);
	void startsound(void *ptr_sounddata, u32 p2unki);

	// Irq
	void enableIRQ(u32 irq);

	// Buttons
	void button_init(button_t *button_data, u32 x, u32 y, const char *imagename, int soundfx, const char *variable);
	void button_update(button_t *button_data);
	void button_draw(button_t *button_data);
	u32 button_pressed(button_t *button_data);
	void button_destroy(button_t *button_data);

	// Sprites
	void sprite_init(sprite_t *sprite_data, const char *imagename, u32 x, u32 y, u32 animation);
	void sprite_draw(sprite_t *sprite_data, u32 brightness_maybe);
	void sprite_set_animation_name(sprite_t *sprite_data, const char *animation_name);
	void sprite_destroy(sprite_t *sprite_data);
	void sprite_set_animation(sprite_t *sprite_data, u32 animation);
	u32 sprite_find_animation(sprite_t *sprite_data, const char *animation_name);
	int sprite_get_width(sprite_t *sprite_data);
	int sprite_get_height(sprite_t *sprite_data);

	void sprite_sub_init(sprite_sub_t *sprite_data, const char *imagename, u32 x, u32 y, u32 animation);
	void sprite_sub_draw(sprite_sub_t *sprite_data);
	void sprite_sub_draw2(sprite_sub_t *sprite_data);
	void sprite_sub_destroy(sprite_sub_t *sprite_data);

	// Sequenced Music Stuff and soundfx stuff
	void sqm_load(u32 music_data_ptr, u32 music_id, u32 always1);
	u32 sqm_started(u32 music_data_ptr);
	void sqm_update_something(u32 other_data_ptr, u32 amount);
	u32 sqm_get_sfx_type(u32 sfx_id);
	u32 sqm_play_sfx(u32 music_data_ptr, u32 sfx_type, u32 sfx_id);

	// Graphics Stuff
	void load_background(u32 some_data_ptr, const char *background_name, u32 always3, u32 always0);
	void load_background_sub(u32 some_data_ptr, const char *background_name, u32 always3, u32 always0);
	void update_graphics(u32 other_data_ptr);

	// Touch
	void touch_update(u32 some_data_ptr);
	bool touch_is_down(u32 touch_data);
	bool touch_is_released(u32 touch_data);
	bool touch_is_pressed(u32 touch_data);
	bool touch_get_location(u32 touch_data, u32 *out_x, u32 *out_y);

	bool point_in_area(int point_x, int point_y, int area_x, int area_y, int area_width, int area_height);

	// Plz Files
	char *plz_load_file(u32 ptr_plz, u32 ptr_unk, const char *filename, u32 unk);
	char *plz_read_file(const char *file);
	void load_file_compressed(u32 ptr_plz, const char *filename, u32 ptr_unk);

	// Screen Text
	void text_show_centered(u32 ptr_texthandler, s32 y, const char *text, s32 line_offset, s32 middle_x, bool is_small);
	void text_show(u32 ptr_texthandler, s32 x, s32 y, const char *text, s32 characters_end, u32 characters_start, s32 line_offset);
	void text_clear(u32 ptr_texthandler);

#ifdef __cplusplus
}
#endif

#define KEYS_CR *((u32 *)0x04000130)

#define A 0x0001
#define B 0x0002
#define SELECT 0x0004
#define START 0x0008
#define LEFT 0x0010
#define RIGHT 0x0020
#define UP 0x0040
#define DOWN 0x0080
#define SRIGHT 0x0100
#define SLEFT 0x0200
#define X 0x0400
#define Y 0x0800
#define TOUCH 0x2000
#define HINGE 0x8000

//Custom key reading funcs.
void myScanKeys();
int myKeysHeld();
int myKeysDown();
void waitForUserInput(u32 input);
void waitForUserPress(u32 keys);
void waitForVBlankIrqLess();

// Usefull things:
// String Formatting
void sprintf(char *buffer, const char *format, ...);
void printf(const char *format, ...);


#define TEXT_DATA 0x02088b44
#define SQM_DATA 0x02088ca8
#define BIG_DATA 0x02088a60
#define PLZ_DATA *(u32 *)0x020889fc
#define GRAPHICS_DATA 0x02088b98
#define SAVE_DATA *(u32 *)(0x020889f4)
#define TOUCH_DATA 0x02088ad4
#define BG_DATA 0x02088c14

// Video functions
void FadeIn(s8 screen, s8 start);
void FadeOut(s8 screen, s8 start);

#endif
