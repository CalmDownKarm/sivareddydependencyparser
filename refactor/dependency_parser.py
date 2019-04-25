import re
import json
import html
import regex_strings as rs


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
    return [''.join(map(lambda x: vowels_to_replace.get(x, x), token)) for token in tokens]


def get_pos_tags(filepath):
    '''The POS Tagger that Sivareddy uses is a something binary that takes input from files
    Not sure if it can take input straight from memory
    :param filepath: contains the filepath of the tokenized and normalized files.
    relative to hindi-pos-tagger directory
    '''
    import os
    import subprocess
    args = [
        './hindi-pos-tagger/bin/tnt',
        '-v0',
        '-H',
        'hindi-pos-tagger/models/hindi',
        filepath
    ]
    sub = subprocess.run(args=args, capture_output=True,
                         cwd=os.path.abspath('..'))
    tags = sub.stdout.decode('utf-8').split('\n')
    multi_tabs = re.compile(r'\t+')
    return [multi_tabs.sub('\t', tokens) for tokens in tags]


def lemmatise(tagged_tokens, lemma):
    '''given a list of tokens and POS tags, lemmatizes them
    :param lemma: string, filepath of the lemma or filepath of lemma stored as a JSON
    expects input to be 2 columns, word\ttag
    :param text: list of strings to lemmatise.
    '''
    if isinstance(lemma, str):
        with open(lemma) as f:
            lemma = json.load(f)
    return [lemmatise_helper(line, lemma) for line in tagged_tokens]


def lemmatise_helper(line, lemma):
        line = line.strip()  # Could probably remove this
        if not line or line.startswith('<'):
            return line
        else:
            cols = line.split()
            if len(cols) != 2:
                return line
            else:
                if cols[0] in lemma and cols[1] in lemma[cols[0]]:
                    return "%s\t%s" % (line, lemma[cols[0]][cols[1]])
                else:
                    return "%s\t%s" % (line, cols[0]+".")


def tag2letter(tag):
    if re.match("NEG", tag):
        return "x"
    elif re.match("^[JNV]", tag):
       return tag[0].lower()
    elif re.match("RB", tag):
       return "r"
    elif re.match("PRP", tag):
       return "d"
    elif re.match("PSP", tag):
       return "p"
    elif re.match("XC", tag):
        return "n"
    elif re.match("CC", tag):
       return "c"
    elif re.match("INJ", tag):
       return "i"
    else:
       return "x"


def tag2vert(lemmatized_tokens):
    return [tag2vert_helper(line) for line in lemmatized_tokens]


def tag2vert_helper(line):
    '''Takes the output of the lemmatizer and creates vertical columns for some reason.'''
    if line == "" or line[0] == "<":
        return line
    else:
        fields = line.split("\t")
        if len(fields) == 3:
            word = fields[0]
            tag = re.findall(r"^(.*)\.(.*?)\.(.*?)\.(.*?)\.(.*?)\.(.*?)$", fields[1])
            if tag == []:
               tagSplit = ['UNK', '', '', '', '', '']
            else:
               tagSplit = tag[0]
            lemma, suffix = re.findall(r"^(.*)\.(.*?)$", fields[2])[0]
            if lemma == "":
                lemma = word
            lempos = lemma + "-" + tag2letter(tagSplit[0])
            return "%s\t%s\t%s\t%s\t%s\n" % (word, tagSplit[0], lempos, suffix, "\t".join(tagSplit[1:]))
        else:
            return line

def modify_pos_tags(vert_tags):
    '''
    I honestly don't know what this function does, or why it's needed, but it's here.
    '''
    return [modify_pos_tags_helper(line) for line in vert_tags]

def modify_pos_tags_helper(line):
    if line.startswith('<'):
        return line
    cols= line[:-1].split('\t')
    if len(cols)<2:
        return line
    if cols[1] in ["PSP", "CC"]:
        cols[1]+= ":" + cols[2][:-2]
    elif cols[1]=="SYM":
        if cols[0]=="।":
            cols[1]="."
        else:
            cols[1]= cols[0]
    return '\t'.join(cols)
