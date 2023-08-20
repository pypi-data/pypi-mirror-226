#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "scanner.h"


uint16_t scan_token(scanner_t *s)
{
    s->start = s->cursor;
    unsigned char *marker = s->cursor;

#define YYCTYPE     unsigned char
#define YYCURSOR    s->cursor
#define YYMARKER    marker
#define YYLIMIT     (s->end)
/*!re2c
re2c:yyfill:enable = 0;
!include "unicode_categories/unicode_categories.re";
!include "word_breaks/unicode_word_breaks.re";
!include "emoji_sequences/emoji_sequences.re";

// Start rules
