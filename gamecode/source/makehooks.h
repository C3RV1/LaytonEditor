#include <nds.h>

u32 makeBranchOpCode(void *src, void *dest, bool wLink);

u32 hookAddress(u32 *address, void *hook);

inline u32 hookAndBack(u32 * original_address, u32 * hook, u32 * hook_end)
{
    hookAddress(hook_end, original_address+1); // +1 = four bytes because it's an u32
    return hookAddress(original_address, hook); // For testing
}

inline u32 hookAndBack(u32 * original_address, u32 * hook, u32 * hook_end, int offset)
{
    hookAddress(hook_end, original_address+1+offset); // +1 = four bytes because it's an u32
    return hookAddress(original_address, hook); // For testing
}