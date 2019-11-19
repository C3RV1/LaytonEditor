typedef unsigned int u32;

extern u32 _end;
u32 PatchCodeOffset = 0xDEADBEAF;
u32 CustomCodeLenght = 0xDEADBEAF;

extern "C"
{
    void MIi_CpuCopy32(void *src, void *dest, u32 len);
}

void setupcustomcode()
{
    MIi_CpuCopy32((void *)(&_end), (void *)PatchCodeOffset, CustomCodeLenght);
}