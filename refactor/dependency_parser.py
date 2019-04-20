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
                tokens.extend(tokenise_recursively(
                    text[pos:startpos], re_list, depth+1))
            tokens.append(text[startpos:endpos])
            pos = endpos
    return tokens


def tokenise(data, language='English'):
    '''
    passed a language, an encoding, and some text runs the tokenizer
    :param data: string, assumes a single sentence of text.
    if it sees a । followed by 1 or more whitespaces, it adds a fullstop and a </s><s> tag.
    Depending on how these sentences chain together, could change the </s><s> combination.
    :param language: string, language of the text
    returns list of tokens
    '''
    clictics, abbreviations, word = [dict_.get(language, dict_.get('default'))
                                     for dict_ in [rs.clictics, rs.abbreviations, rs.word]]
    re_list = [rs.SGML_TAG]
    if abbreviations:
        re_list += [abbreviations]
    if clictics:
        re_list += [clictics]
    re_list += [rs.WHITESPACE, rs.URL, rs.EMAIL, rs.IP_ADDRESS,
                rs.HTMLENTITY, rs.NUMBER_RE, rs.ACRONYM, rs.MULTICHAR_PUNCTUATION,
                rs.OPEN_CLOSE_PUNCTUATION, rs.ANY_SEQUENCE, word]
    data = html.unescape(data)  # Remove HTML Entities can be replaced
    for regex, expression in [(rs.CONTROL_CHAR, ''), (rs.SPACE, ' ')]:
        data = regex.sub(expression, data)

    data = rs.HINDI_SENTENCE_ENDS.sub(' . </s> <s> ', data)
    tokens = tokenise_recursively(data, re_list)
    return list(filter(None, ''.join(tokens).split(' ')))
    # return ''.join(tokens).split(' ')


def normalize(tokens):
    ''' Takes a list of tokens, and normalizes them
    तृष्णा -> तृष्णा
    भागता -> भागता
    '''
    vowels_to_replace = {
        chr(0x0901): chr(0x0902),
        '': 'न',
        'ऩ': 'न',
        'ऱ': 'र',
        'ऴ': 'ळ',
        'क़': 'क',
        'ख़': 'ख',
        'ग़': 'ग',
        'ज़': 'ज',
        'ड़': 'ड',
        'ढ़': 'ढ',
        'फ़': 'फ',
        'य़': 'य',
        'ॠ': 'ऋ',
        'ॡ': 'ऌ',
    }
    return [map(lambda x: vowels_to_replace.get(x, x), token) for token in tokens]



