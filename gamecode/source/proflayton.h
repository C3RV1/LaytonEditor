#include <nds.h>
#include "someptrs.h"

#ifndef _NSMB_H
#define _NSMB_H

typedef u8 FSFile[0x48];
typedef u8 OSThread[0xC0];

#ifdef __cplusplus
extern "C"
{
#endif
	// Allocating and freeing
	void FreeSomething(void *ptr);
	void* AllocSomething(u32 size);

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
    void setupsound(void* ptr_sounddata, u32 p2unki, u32 stream_n, s32 p4ni, u32 p5ni);
    void stopsound(void* ptr_sounddata, u32 p2unki);
    void startsound(void* ptr_sounddata, u32 p2unki);

	// Irq
    void enableIRQ(u32 irq);

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
void waitForVBlankIrqLess();

// Usefull things:
// String Formatting
void sprintf(char *buffer, const char *format, ...);
void printf(const char *format, ...);

#endif
