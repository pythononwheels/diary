import re
import time

#
# (pattern, search, replace) regex english plural rules tuple
# taken from : http://www.daniweb.com/software-development/python/threads/70647
rule_tuple = (
    ('[ml]ouse$', '([ml])ouse$', '\\1ice'),
    ('child$', 'child$', 'children'),
    ('booth$', 'booth$', 'booths'),
    ('foot$', 'foot$', 'feet'),
    ('ooth$', 'ooth$', 'eeth'),
    ('l[eo]af$', 'l([eo])af$', 'l\\1aves'),
    ('sis$', 'sis$', 'ses'),
    ('man$', 'man$', 'men'),
    ('ife$', 'ife$', 'ives'),
    ('eau$', 'eau$', 'eaux'),
    ('lf$', 'lf$', 'lves'),
    ('[sxz]$', '$', 'es'),
    ('[^aeioudgkprt]h$', '$', 'es'),
    ('(qu|[^aeiou])y$', 'y$', 'ies'),
    ('$', '$', 's')
    )

def regex_rules(rules=rule_tuple):
    # also to pluralize
    for line in rules:
        pattern, search, replace = line
        yield lambda word: re.search(pattern, word) and re.sub(search, replace, word)


def plural(noun):
    #print noun
    # the final pluralisation method.
    for rule in regex_rules():
        result = rule(noun)
        #print result
        if result:
            return result

def pluralize(noun):
    return plural(noun)

def singularize(word):
    # taken from:http://codelog.blogial.com/2008/07/27/singular-form-of-a-word-in-python/
    sing_rules = [lambda w: w[-3:] == 'ies' and w[:-3] + 'y',
              lambda w: w[-4:] == 'ives' and w[:-4] + 'ife',
              lambda w: w[-3:] == 'ves' and w[:-3] + 'f',
              lambda w: w[-2:] == 'es' and w[:-2],
              lambda w: w[-1:] == 's' and w[:-1],
              lambda w: w,
              ]
    word = word.strip()
    singleword = [f(word) for f in sing_rules if f(word) is not False][0]
    return singleword

#
# uuid / dooco d helpers
# 
def get_posixtime_from_uuid(uuid1):
    """Convert the uuid1 timestamp to a standard posix timestamp
    """
    assert uuid1.version == 1, ValueError('only applies to type 1')
    t = uuid1.time
    t = t - 0x01b21dd213814000
    t = t / 1e7
    return t

def get_struct_time_from_uuid(uuid1, local=True):
    """ returns struct_time for the localtime from a uuid1.time 
        if local=True. If local=False gmtime is returned
    """
    if local:
        return time.localtime(get_posixtime_from_uuid(uuid1))
    else:
        return time.gmtime(get_posixtime_from_uuid(uuid1))



#
# relation decorators
#
# usage: 
# @has_many(["comments"])
# class Modelclass():
# 
class has_many(object):
    def __init__(self, arg):
        self.arg = arg
        print(str(arg))
    def __call__(self, cls):
        print(cls)
        class Wrapped(cls):
            has_many = self.arg
        return Wrapped

class belongs_to(object):
    def __init__(self, arg):
        self.arg = arg
        print(str(arg))
    def __call__(self, cls):
        print(cls)
        class Wrapped(cls):
            belongs_to = self.arg
        return Wrapped

class is_tree(object):
    def __init__(self, arg):
        self.arg = arg
        print(str(arg))
    def __call__(self, cls):
        print(cls)
        class Wrapped(cls):
            is_tree = true
        return Wrapped

