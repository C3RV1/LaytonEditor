#include "proflayton.h"

static int keys, oldKeys, keysDw;
static bool first = true;

void myScanKeys()
{
	first = false;
	int keys = ~REG_KEYINPUT;
	if (first)
		oldKeys = keys;
	keysDw = keys & ~oldKeys;
	oldKeys = keys;
}

int myKeysHeld()
{
	return keys;
}
int myKeysDown()
{
	return keysDw;
}

void waitForUserInput(u32 input)
{
	while ((REG_KEYINPUT & input) == input)
	{
		swiWaitForVBlank();
	}
}