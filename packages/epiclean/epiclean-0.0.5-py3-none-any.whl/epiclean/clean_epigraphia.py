import re

# This file contains the actual functionality of the processor
def processor(input, lang, a, e, o, u, s, sri, n, jn, m):
    consonants_regex_expr = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZḍṭr̥ṟḷḻṣśḌṬR̥ṞḶḺṢŚ'
    if lang == 'kn':
        output = input
        if a:
            output = re.sub('[âàá]', 'ā', output)
        if e:
            output = re.sub('é', 'ē', output)
        if o:
            output = re.sub('[ôó]', 'ō', output)
        if u:
            output = re.sub('ü', 'ū', output)
            output = re.sub('([{consonants_regex_expr}])ti([{consonants_regex_expr}])', r'\1ū\2', output)
        if s:
            output = re.sub('[$&]', 'ś', output)
            output = re.sub('S\'', 'Ś', output)
        if sri:
            output = re.sub('[sśS$&géē]ri', 'śrī', output)
        if n:
            output = re.sub('n([kg])', r'ṅ\1', output)

            output = re.sub('n([cj])', r'ñ\1', output)

            output = re.sub('n([ṭḍ])', r'ṇ\1', output)

            output = re.sub('m([yrlvśṣh])', r'ṁ\1', output)
        if jn:
            output = re.sub('fi([cj])', r'ñ\1', output)
        if m:
            output = re.sub('m([-\s+])([{consonants_regex_expr}])', r'ṁ\1\2', output)
        return output
    else:
        return None
