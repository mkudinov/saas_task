__author__ = 'mkudinov'
import re
import urllib
from random import randint

def get_company_names(data_source):
    names = set()
    separate_punct = re.compile(ur'(\w)([!,.?&\(\)"])')
    for i, line in enumerate(open(data_source, 'r')):
        line = unicode(line.strip(), 'utf-8').lower()
        name = separate_punct.sub(ur'\1 \2', line)
        name = re.sub('\s+', '_ _', name)
        name = re.sub(r"\d+", 'N', name)
        name = u'_' + name.strip() + u'_'
        if name is not None:
            names.add(name)
    return names


def get_db_pedia_names(data_source):
    names = set()
    get_name_code = re.compile('<http://dbpedia.org/resource/(.+?)>')
    separate_punct = re.compile(ur'(\w)([!,.?&\(\)])')
    for i, line in enumerate(open(data_source, 'r')):
        line = unicode(line.strip(), 'utf-8').lower()
        name = get_name_code.match(line)
        if name is not None:
            name = name.groups(1)[0]
            if name.find(',') != -1:
                continue
            name=unicode(urllib.unquote(name.encode('utf-8')), 'utf-8')
            name = re.sub(r"\"", '', name)
            name = separate_punct.sub(ur'\1_\2', name)
            name = u'_' + re.sub(r"_", "_ _", name).strip() + u'_'
            name = re.sub(r"\d+", 'N', name)
            name = re.sub('_+', '_', name)
            name = re.sub('\s+_\s+', '', name)
            if len(name) > 0:
                names.add(name)
    names = set([re.sub('_[,(].+', '', name) for name in names])
    return names


def make_random_phrases(data_source, number):
    vocab = []
    ngrams = []
    for line in open(data_source, 'r'):
        vocab.append(unicode(line, 'utf-8').strip())
    for i in range(number):
        rn = randint(0, 9)
        if rn < 5:
            length = 2
        elif rn < 7:
            length = 3
        elif rn < 8:
            length = 1
        else:
            length = 4
        ngram = []
        for j in range(length):
            rn = randint(0, len(vocab) - 1)
            ngram.append(vocab[rn])
        ngram = u'_' + u'_ _'.join(ngram) + u'_'
        ngrams.append(ngram)
    return ngrams


def create_data():
    geo_source='/home/mkudinov/Data/geonames_links_en.ttl'
    proper_names_source='/home/mkudinov/Data/persondata_en.nt'
    vocab_source = '/home/mkudinov/Data/vocab2'
    proper_names = get_db_pedia_names(proper_names_source)
    company_names = get_company_names('/home/mkudinov/Data/companies')
    geo_names = get_db_pedia_names(geo_source)
    random_phrases = make_random_phrases(vocab_source, 200000)

    with open('random_phrases.txt', 'w') as out:
        for phrase in random_phrases:
            out.write((u'%s\n' % phrase).encode('utf-8'))

    with open('proper_names.txt', 'w') as out:
       for name in proper_names:
           out.write((u'%s\n' % name).encode('utf-8'))

    with open('company_names.txt', 'w') as out:
       for name in company_names:
           out.write((u'%s\n' % name).encode('utf-8'))

    with open('geo_names.txt', 'w') as out:
       for name in geo_names:
           out.write((u'%s\n' % name).encode('utf-8'))


create_data()

pass
