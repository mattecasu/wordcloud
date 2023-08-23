import multidict


def flatten(nested):
    return [item for l in nested for item in l]


def to_multidict(d: dict):
    multi = multidict.MultiDict()
    for key in d:
        multi.add(key, d[key])
    return multi


def to_normal_dict(multi):
    return {k: v for k, v in multi.items()}


def splitBy(chunk, connectives):
    l = chunk.split()
    if any([x in connectives for x in l]):
        groupby(l, lambda x: x == "")
        lists = [list(group) for k, group in groupby(l, lambda x: x in connectives) if not k]
        return flatten(lists)
    else:
        return [chunk]


def strip_list(l, stopwords):
    while l and (l[-1] in stopwords or l[-1].isnumeric()):
        l.pop()
    l.reverse()
    while l and (l[-1] in stopwords or l[-1].isnumeric()):
        l.pop()
    l.reverse()
    return l
