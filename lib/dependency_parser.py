import regex_strings as rs


def tokenise(data, lsd, glue):
    '''
    '''


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
    lsd = [dict_.get(language, dict_.get('default')) for dict_ in [rs.clictics, rs.abbreviations, rs.word]]
    # lsd = LanguageData()
    tokens = '\n'.join(tokenise(data, lsd, glue))
    return tokens