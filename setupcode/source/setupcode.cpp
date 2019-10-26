typedef unsigned int u32;
typedef unsigned char u8;
typedef void calladdr(void);

extern u32 _end;
u32 PatchCodeOffset = 0xDEADBEAF;
u32 CustomCodeLenght = 0xDEADBEAF;
u32 TestAddress = 0xDEADBEAF;
char text[] = "Hello World!";

void setupcustomcode()
{
    u8 *startCustomCode = (u8 *)(&_end);
    u8 *arenaLo = (u8 *)PatchCodeOffset;
    for (u32 i = 0; i < CustomCodeLenght; i++)
        arenaLo[i] = startCustomCode[i];
}