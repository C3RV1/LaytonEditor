#ifndef UTIL_H
#define UTIL_H

#ifdef __cplusplus
extern "C"
{
#endif

void sprintf(char *buffer, const char *format, ...);
void printf(const char *format, ...);
void putc(char c);
void puts(const char *text);

#ifdef __cplusplus
}
#endif

#endif