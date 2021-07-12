#include <lt2.h>

void *operator new(std::size_t size)
{
    return OS_Malloc(size);
}

void operator delete(void *ptr)
{
    OS_Free(ptr);
}

void operator delete(void *ptr, std::size_t size)
{
    OS_Free(ptr);
}
