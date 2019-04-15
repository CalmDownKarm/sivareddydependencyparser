import regex_strings as rs
import html

def tokenise_recursively(data, re_list):

    return ...

def replace_html_entities(data):
    return ...

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
    data = rs.CONTROL_CHAR.sub('', data)
    data = [html.unescape(str_) for str_ in data]
    data = rs.SPACE.sub(' ',data)
    tokens = tokenise_recursively(data, re_list)

def run_tokenize(data, language='English', encoding='utf-8', glue='<g/>', stream=False, quiet=False):
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
    tokens = '\n'.join(tokenise(data, lsd, glue))
    return tokens
