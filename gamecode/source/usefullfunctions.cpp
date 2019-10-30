#include "proflayton.h"
#include <string.h>

#define PRINTF_BUFFER_SIZE 50

void sprintf(char *buffer, const char *format, ...)
{
    char **arg = (char **)&format;
    int c;
    char buf[20];
    arg++;

    while ((c = *format++) != 0)
    {
        if (c != '%')
            *buffer++ = c;
        else
        {
            char *p, *p2;
            int pad0 = 0, pad = 0;

            c = *format++;
            if (c == '0')
            {
                pad0 = 1;
                c = *format++;
            }

            if (c >= '0' && c <= '9')
            {
                pad = c - '0';
                c = *format++;
            }

            switch (c)
            {
            case 'd':
                itoa(*((int *)arg++), buf, 10);
                goto number;
            case 'u':
                itoa(*((u32 *)arg++), buf, 10);
                goto number;
            case 'x':
                itoa(*((int *)arg++), buf, 16);
            number:
                p = buf;
                goto string;
                break;

            case 's':
                p = *arg++;
                if (!p)
                    strcpy(p, "(null)");

            string:
                for (p2 = p; *p2; p2++)
                    ;
                for (; p2 < p + pad; p2++)
                    *buffer++ = pad0 ? '0' : ' ';
                while (*p)
                    *buffer++ = *p++;
                break;

            default:
                *buffer++ = *((int *)arg++);
                break;
            }
        }
    }
}

void printf(const char * format, ...)
{
    char buffer[PRINTF_BUFFER_SIZE];
    char *bufferptr = buffer;
    char **arg = (char **)&format;
    int c;
    char buf[20];
    arg++;

    while ((c = *format++) != 0)
    {
        if (c != '%')
            *bufferptr++ = c;
        else
        {
            char *p, *p2;
            int pad0 = 0, pad = 0;

            c = *format++;
            if (c == '0')
            {
                pad0 = 1;
                c = *format++;
            }

            if (c >= '0' && c <= '9')
            {
                pad = c - '0';
                c = *format++;
            }

            switch (c)
            {
            case 'd':
                itoa(*((int *)arg++), buf, 10);
                goto number;
            case 'u':
                itoa(*((u32 *)arg++), buf, 10);
                goto number;
            case 'x':
                itoa(*((int *)arg++), buf, 16);
            number:
                p = buf;
                goto string;
                break;

            case 's':
                p = *arg++;
                if (!p)
                    strcpy(p, "(null)");

            string:
                for (p2 = p; *p2; p2++)
                    ;
                for (; p2 < p + pad; p2++)
                    *bufferptr++ = pad0 ? '0' : ' ';
                while (*p)
                    *bufferptr++ = *p++;
                break;

            default:
                *bufferptr++ = *((int *)arg++);
                break;
            }
        }
    }
    *bufferptr++ = 0;
    nocashMessage(buffer);
}