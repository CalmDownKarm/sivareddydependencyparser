from io import open
import os
import re
import sys
import glob
import json
import html
import subprocess
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
    args = [
        'hindi-pos-tagger/bin/tnt',
        '-v0',
        '-H',
        'hindi-pos-tagger/models/hindi',
        filepath
    ]
    sub = subprocess.run(args=args, capture_output=True)
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
            tag = re.findall(
                r"^(.*)\.(.*?)\.(.*?)\.(.*?)\.(.*?)\.(.*?)$", fields[1])
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
    cols = line[:-1].split('\t')
    if len(cols) < 2:
        return line
    if cols[1] in ["PSP", "CC"]:
        cols[1] += ":" + cols[2][:-2]
    elif cols[1] == "SYM":
        if cols[0] == "।":
            cols[1] = "."
        else:
            cols[1] = cols[0]
    return '\t'.join(cols)


def to_conll(listoftokens, filename):
    '''
    expects a list of lists - inner list is line.split('\t')[:3] of the modified POS tags
    writes to a temporary conll file.
    '''
    index = 1
    with open(filename, 'w+', encoding='utf-8') as f:
        for tokens in listoftokens:
            if len(tokens) > 2:
                j = [str(index), tokens[0], tokens[2][:-2], '_',
                     tokens[1], '_|_|_|_|_', '_', '_', '_', '_']
                f.write('\t'.join(j)+"\n")
                index = index + 1
            else:
                index = 1
                f.write("\n")


def run_malt_parser(input_filename, jar_path):
    '''
    take an input file and a jar path to the malt parser and run from there.

    '''
    args = [
        'java',
        '-jar',
        jar_path,
        '-c',
        'test_complete',
        '-i',
        input_filename,
        '-m',
        'parse'
        # java -jar bin/malt.jar -c test_complete -i $@.tmp.tag.conll -o $@.tmp.output -m parse
    ]
    sub = subprocess.run(args=args, capture_output=True)
    print(sub.stderr)
    return [parse_malt_output_helper(token) for token in sub.stdout.decode('utf-8').split('\n')]

def parse_malt_output_helper(token):
    list_ = token.split('\t')
    if len(list_) > 2:
        return '\t'.join((list_[0], list_[1], list_[2], list_[4], list_[6], list_[7]))
    else:
        return ''


def run_pipe(input_file):
    output_file = input_file + '-parsed'
    ''' Runs everything '''
    # Start doing this
    with open(input_file, encoding='utf-8') as f:
        source_text = f.readlines()
    remove_starting_num = re.compile(r'^[0-9]+')
    source_text = [remove_starting_num.sub('', line) for line in source_text]
    tokenized = [normalize(tokenise(x, language='Hindi')) for x in source_text]
    flat = [x for y in tokenized for x in y if x!='\n']
    new_tokens = [pattern.sub(lambda m: rep[re.escape(m.group(0))], text) for text in flat]
    sentence_splits = [tokens.split('\n') for tokens in new_tokens]
    flatten_sentence_splits = [x for y in sentence_splits for x in y if x]
    temporary_tokenized_normalized_filepath = input_file+ '-temp'
    with open(temporary_tokenized_normalized_filepath, 'w', encoding='utf-8')as f:
        f.writelines((f'{x}\n' for x in flatten_sentence_splits))

    for var in [tokenized, flat, new_tokens, sentence_splits, flatten_sentence_splits]:
        del var

    lemma_input = [multi_tabs.sub('\t', tokens) for tokens in get_pos_tags(temporary_tokenized_normalized_filepath)]
    lemma_input = lemmatise(lemma_input, loaded_lemma)
    lemma_input = tag2vert(lemma_input)
    lemma_input = modify_pos_tags(lemma_input)
    lemma_input = [token.split('\t')[:3] for token in lemma_input]
    temporary_conll_filepath = input_file + '-temp.conll'
    to_conll(lemma_input, temporary_conll_filepath)
    del lemma_input
    sub = run_malt_parser(temporary_conll_filepath, jarpath)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines((f'{x}\n' for x in sub))
    for file in [temporary_tokenized_normalized_filepath, temporary_conll_filepath]:
        if os.path.exists(file):
            os.unlink(file)

if __name__ == "__main__":
    Subs = {
    ',':'\n,\n',
    '(': '\n(\n',
    ')': '\n)\n',
    '‘': '\n‘\n',
    '’': '\n’\n',
    '"': '\n"\n',
    "'": "\n'\n",
    '+': '\n+\n',
    '!': '\n!\n',
    }
    rep = dict((re.escape(k), v) for k, v in Subs.items())
    pattern = re.compile("|".join(rep.keys()))
    jarpath = 'malt.jar'
    multi_tabs = re.compile('\t+')
    with open('hindi.lemma.json', encoding='utf-8') as lemmafile:
        loaded_lemma = json.load(lemmafile)
    input_file = sys.argv[1]
    run_pipe(input_file)
