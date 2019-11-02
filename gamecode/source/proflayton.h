#include <nds.h>
#include "someptrs.h"

#ifndef _NSMB_H
#define _NSMB_H

#ifdef __cplusplus
extern "C"
{
#endif
	//Printing

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

//Usefull things
void sprintf(char *buffer, const char *format, ...);
void printf(const char *format, ...);

#endif
