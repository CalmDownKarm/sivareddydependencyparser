import regex_strings as rs
import html

def tokenise_recursively(text, re_list, depth=0):
    if depth >= len(re_list):
        return [text]
    regular_expr = re_list[depth]
    tokens = []
    pos = 0
    while pos < len(text):
        m = regular_expr.search(text, pos)
        if not m:
            tokens.extend(tokenise_recursively(text[pos:], re_list, depth+1))
            break
        else:
            startpos, endpos = m.span()
            if startpos > pos:
                tokens.extend(tokenise_recursively(text[pos:startpos], re_list, depth+1))
            tokens.append(text[startpos:endpos])
            pos = endpos
    return tokens

def tokenise(data, lsd, glue):
    '''
    Given some text and language data, aggregates a bunch of Regular expressions and runs tokenise_recursively
    :param data: list of strings to be tokenized
    :param lsd: list of clictics, abbreviations, word compiled regex objects
    :param glue: the glue character
    '''
    re_list = [rs.SGML_TAG]
    clictics, abbreviations, word = lsd
    if abbreviations:
        re_list += [abbreviations]
    if clictics:
        re_list += [clictics]
    re_list += [rs.WHITESPACE, rs.URL, rs.EMAIL, rs.IP_ADDRESS,
                rs.HTMLENTITY, rs.NUMBER_RE, rs.ACRONYM, rs.MULTICHAR_PUNCTUATION,
                rs.OPEN_CLOSE_PUNCTUATION, rs.ANY_SEQUENCE, word]
    data = html.unescape(data) # Remove HTML Entities can be replaced
    for regex, expression in [(rs.CONTROL_CHAR, ''), (rs.SPACE, ' ')]:
        data = regex.sub(expression, data)
    import re
    data = re.sub(r'।\s+|।|\'|,|‘', ' ', data)
    tokens = tokenise_recursively(data, re_list)
    return ''.join(tokens).split(' ')
    # Dataset doesn't have SGML tags for now, so ignoring all the glue tag stuff



def run_tokenize(data, language='English', encoding='utf-8', stream=False, quiet=False):
    '''
    passed a language, an encoding, and some text runs the tokenizer
    :param language: string, language of the text
    :param encoding: string, encoding type
    :param glue: boolean, use glue character
    :param stream: boolean, not sure
    returns newline seperated list of tokens
    '''
    # no_glue  = False
    lsd = [dict_.get(language, dict_.get('default'))
           for dict_ in [rs.clictics, rs.abbreviations, rs.word]]
    # lsd = LanguageData()
    tokens = tokenise(data, lsd)
    # tokens = '\n'.join(tokenise(data, lsd, glue))
    return tokens
