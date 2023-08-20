
any = [^\u0000];
newline = ("\r\n")|[\r\n\u2028\u2029\u000B\u000C\u0085];

ascii_letter = [A-Za-z];
digit = [0-9];

non_space = [^ \u00a0\u1680\u180e\u2000-\u200a\u202f\u3000\u0000-\u001f\u007f-\u009f];

single_quote = [\u0027];
double_quote = [\u0022];

letter = {letter_lower_chars}|{letter_upper_chars}|{letter_title_chars}|{letter_other_alpha_chars}|{hebrew_letter_chars};
latinish_letter = {letter_lower_chars}|{letter_upper_chars}|{letter_title_chars};

underscore = [_];

hyphen = [\-];
minus = [\u2212];
figure_dash = [\u2012];
ndash = [\u2013];
mdash = [\u2014\u2e3a\u2e3b\ufe31\ufe58];
hbar = [\u2015];
swung_dash = [\u2053];


other_non_breaking_dash = [\u058a\u05be\u1400\u1806\u2010-\u2013\u2212\u2e17\u2e1a\ufe32\ufe63\uff0d];

non_breaking_dash = (({hyphen}{1,1})|{other_non_breaking_dash});
breaking_dash = ({mdash}|{hbar}|{swung_dash}|({hyphen}{2,}));

// WB5
basic_word = {letter}+;
// WB6
word_non_breaking_mid_char = {letter}+(({mid_letter_chars}|{non_breaking_dash}|{mid_num_letter_chars}|{single_quote}){letter}+)+;
// WB7
word_end_single_quote = {letter}+(({mid_letter_chars}|{mid_num_letter_chars}){letter}+{single_quote});
// WB7a
hebrew_word_single_quote = ({hebrew_letter_chars}+{single_quote})+;
// WB7b and WB7c
hebrew_word_double_quote = ({hebrew_letter_chars}+{double_quote})+{hebrew_letter_chars}*;

// WB11 and WB12 (modified slightly)
possible_numeric_chars = ({numeric_chars}|{letter}|{non_breaking_dash}|{hyphen}|{mid_num_letter_chars}|{single_quote});
number = ({non_breaking_dash}?((({numeric_chars}|{number_or_digit_chars})+({mid_number_chars}|{mid_num_letter_chars}))*)({numeric_chars}|{number_or_digit_chars})+);
numeric = (({non_breaking_dash}|((({numeric_chars}|{number_or_digit_chars}|{letter})+{possible_numeric_chars}*)*))({numeric_chars}|{number_or_digit_chars})+({possible_numeric_chars}*({numeric_chars}|{number_or_digit_chars}|{letter})+)*);


// WB13
katakana = {katakana_chars}+;

// WB13a and WB13b
word_extend_num_letter = ({letter}|{numeric_chars}|{katakana}|{extend_num_letter_chars})+{extend_num_letter_chars}({letter}|{numeric_chars}|{katakana}|{extend_num_letter_chars})*;

possible_word_char = {letter}|{mark_spacing_combining_chars}|{mark_enclosing_chars}|{mark_nonspacing_chars}|{punct_connector_chars}|{currency_symbol_chars}|{symbol_modifier_chars}|{symbol_math_chars}|{digit};
any_word = (({possible_word_char}*{letter}+{possible_word_char}*{non_breaking_dash})*{possible_word_char}*{letter}+{possible_word_char}*);

// GB6, GB7 & GB8
hangul_syllable = (({hangul_syllable_class_L}(hangul_syllable_class_L|hangul_syllable_class_V|hangul_syllable_class_LV|hangul_syllable_class_LVT))|(({hangul_syllable_class_L}|{hangul_syllable_class_V})({hangul_syllable_class_V}{hangul_syllable_class_T}))|(({hangul_syllable_class_LVT}|{hangul_syllable_class_T}){hangul_syllable_class_T}));

apos_word = ("'"?({latinish_letter}+"'"){latinish_letter}+"'"?);

ellipsis = ("\."{2,}|"\u2026");

acronym = ({letter}"\."){2,}{letter}?;
multi_punct_abbreviation = ({letter}+"\.")+{letter}*;

abbrev_word = (({letter}|{possible_word_char})+"\.")+({letter}|{possible_word_char})*;

abbreviation_plus_hyphen = ((({abbrev_word}|{any_word})({hyphen}|{ndash}))+({any_word}));

word = ({basic_word})|({word_non_breaking_mid_char})|({word_end_single_quote})|({hebrew_word_single_quote})|({hebrew_word_double_quote})|({word_extend_num_letter});

us_phone_number = ("\+"?"1"[\-\. ]?)?"\("?([2-9][0-8][0-9])"\)"?[\-\. ]?([2-9][0-9]{2})[\-\. ]?([0-9]{4});
international_phone_number = "\+"("9"[976][0-9]|"8"[987530][0-9]|"6"[987][0-9]|"5"[90][0-9]|"420-9"|"3"[875][0-9]|"2"[98654321][0-9]|"9"[8543210]|"8"[6421]|"6"[6543210]|"5"[87654321]|"4"[987654310]|"3"[9643210]|"2"[70]|"7"|"1"){space}*(([()\.\-/ ]{0,1}[0-9]){9}[0-9]{1,2});

url = ('http''s'?":"("/"{1,3}|[A-Za-z0-9%]))([^\u0000 \t\u00A0\u2000-\u200A\u3000\r\n\f<>{}\[\]]+);

email = ([a-zA-Z0-9\._%+\-]+"@"([a-zA-Z0-9]+([\-][a-zA-Z0-9]+)*[\.])+[a-zA-Z0-9]{2,3});

invalid_chars = ({control_chars}|{other_format_chars}|{other_private_use_chars});

"\u0000"                        { return TOKEN_TYPE_END; }
{invalid_chars}                 { return TOKEN_TYPE_INVALID_CHAR; }
{space}+                        { return TOKEN_TYPE_WHITESPACE; }

{email}                         { return TOKEN_TYPE_EMAIL; }
{url}                           { return TOKEN_TYPE_URL; }

{emoji}                         { return TOKEN_TYPE_EMOJI; }

{ellipsis}                      { return TOKEN_TYPE_ELLIPSIS; }

{us_phone_number}               { return TOKEN_TYPE_US_PHONE; }
{international_phone_number}    { return TOKEN_TYPE_INTL_PHONE; }

{abbreviation_plus_hyphen}      { return TOKEN_TYPE_WORD; }
{acronym}                       { return TOKEN_TYPE_ACRONYM; }

{number}                        { return TOKEN_TYPE_NUMERIC; }
{numeric}                       { return TOKEN_TYPE_NUMERIC; }
{apos_word}                     { return TOKEN_TYPE_WORD; }
{hangul_syllable}               { return TOKEN_TYPE_HANGUL_SYLLABLE; }
{ideographic_chars}             { return TOKEN_TYPE_IDEOGRAPHIC_CHAR; }
{ideographic_numeric_chars}     { return TOKEN_TYPE_IDEOGRAPHIC_NUMBER; }
{word}                          { return TOKEN_TYPE_WORD; }
{katakana}                      { return TOKEN_TYPE_WORD; }
{any_word}                      { return TOKEN_TYPE_WORD; }

{newline}                       { return TOKEN_TYPE_NEWLINE; }
"\."                            { return TOKEN_TYPE_PERIOD; }
"!"                             { return TOKEN_TYPE_EXCLAMATION; }
"?"                             { return TOKEN_TYPE_QUESTION_MARK; }
{hyphen}{1}                     { return TOKEN_TYPE_HYPHEN; }
","                             { return TOKEN_TYPE_COMMA; }
":"                             { return TOKEN_TYPE_COLON; }
";"                             { return TOKEN_TYPE_SEMICOLON; }
{punct_open_chars}              { return TOKEN_TYPE_PUNCT_OPEN; }
{punct_close_chars}             { return TOKEN_TYPE_PUNCT_CLOSE; }
"/"                             { return TOKEN_TYPE_SLASH; }
"\\"                            { return TOKEN_TYPE_BACKSLASH; }
"\""                            { return TOKEN_TYPE_DOUBLE_QUOTE; }
"'"                             { return TOKEN_TYPE_SINGLE_QUOTE; }
{punct_initial_quote_chars}     { return TOKEN_TYPE_OPEN_QUOTE; }
{punct_final_quote_chars}       { return TOKEN_TYPE_CLOSE_QUOTE; }
"&"                             { return TOKEN_TYPE_AMPERSAND; }
">"                             { return TOKEN_TYPE_GREATER_THAN; }
"<"                             { return TOKEN_TYPE_LESS_THAN; }
"@"                             { return TOKEN_TYPE_AT_SIGN; }
"+"                             { return TOKEN_TYPE_PLUS; }
"#"                             { return TOKEN_TYPE_POUND; }
{other_non_breaking_dash}       { return TOKEN_TYPE_DASH; }
{breaking_dash}                 { return TOKEN_TYPE_BREAKING_DASH; }
{other_surrogate_chars}         { return TOKEN_TYPE_INVALID_CHAR; }
{any}                           { return TOKEN_TYPE_OTHER; }
