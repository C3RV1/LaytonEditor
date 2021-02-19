#include <stdint.h>

#define REPL(addr, ...) \
extern "C" void __repl_##addr(__VA_ARGS__)

#define RT_REPL(returntype, addr, ...) \
extern "C" returntype __repl_##addr(__VA_ARGS__)

#define ESCP(addr, ...) \
extern "C" void __escp_##addr(__VA_ARGS__)

#define HOOK(addr, ...) \
extern "C" void __repl_##addr() { \
    asm("push {r0-r12,r14}"); \
    asm("bl __hook_" #addr); \
    asm("pop {r0-r12,r14}"); \
    asm("\n__org_" #addr ": .long 10"); \
} \
extern "C" void __hook_##addr(__VA_ARGS__)

typedef struct {
    uint32_t overlay: 6;
    uint32_t link;
    uint32_t * location;
    uint32_t function_location;
    uint32_t paste_org;
} ovpatch_t;

#define B_OPP(src, dest) ((((dest - src) >> 2) - 2) & 0xffffff) | 0xEA000000
#define BL_OPP(src, dest) ((((dest - src) >> 2) - 2) & 0xffffff) | 0xEB000000

#define OVREPL(ov, addr, ...) \
extern "C" void __ovrepl_##ov ##_ ##addr(__VA_ARGS__); \
ovpatch_t __ovpatch_##ov ##_ ##addr __attribute__((section(".ovpt"))) = \
    {ov, 1, addr, (uint32_t)&__ovrepl_##ov ##_ ##addr, 0}; \
extern "C" void __ovrepl_##ov ##_ ##addr(__VA_ARGS__)

#define RT_OVREPL(returntype, ov, addr, ...) \
extern "C" returntype __ovrepl_##ov ##_ ##addr(__VA_ARGS__); \
ovpatch_t __ovpatch_##ov ##_ ##addr __attribute__((section(".ovpt"))) = \
    {ov, 1, addr, (uint32_t)&__ovrepl_##ov ##_ ##addr, 0}; \
extern "C" returntype __ovrepl_##ov ##_ ##addr(__VA_ARGS__)

#define OVESCP(ov, addr, ...) \
extern "C" void __ovescp_##ov ##_ ##addr(__VA_ARGS__); \
ovpatch_t __ovpatch_##ov ##_ ##addr __attribute__((section(".ovpt"))) = \
    {ov, 0, addr, (uint32_t)&__ovescp_##ov ##_ ##addr, 0}; \
extern "C" void __ovescp_##ov ##_ ##addr(__VA_ARGS__)

#define OVHOOK(ov, addr, ...) \
extern "C" void __ovrepl_##ov ##_ ##addr() { \
    asm("push {r0-r12,r14}"); \
    asm("bl __ovhook_" #ov "_" #addr); \
    asm("pop {r0-r12,r14}"); \
    asm("\n__ovorg_" #ov "_" #addr ": .long 0"); \
} \
extern "C" void __ovorg_##ov ##_ ##addr(); \
ovpatch_t __ovpatch_##ov ##_ ##addr __attribute__((section(".ovpt"))) = \
    {ov, 1, (uint32_t*)addr, (uint32_t)&__ovrepl_##ov ##_ ##addr, (uint32_t) &__ovorg_##ov ##_ ##addr}; \
extern "C" void __ovhook_##ov ##_ ##addr(__VA_ARGS__)
