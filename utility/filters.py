import re
from functools import reduce

# #: {{ko-usex|공항까지 지하철을 타면 될 것 같은데 혹시 지하철이 '''어디''' 있는지 아세요?|I think I can take the subway to the airport. Do you know '''where''' the subway is?}}
# {{ko-usex|HANGUL|TRANSLATION}}

# {{ko-verb}} {{lb|ko|more often|_|intransitive|see Usage notes}}
# -> 가다 • (gada) (infinitive 가, sequential 가니) (more often intransitive, see Usage notes)

# {{ko-noun|hanja=女子}}
# -> 여자 • (yeoja) (hanja 女子)

# {{ko-pos|particle}}
# -> 에 • (-e)

prefix = r'ko-'

template_filter = re.compile(r'{{' + prefix + r'([-a-zA-Z]+)\|([^}]*)}}')
style_filter = re.compile(r'\'\'+')
named_link = re.compile(r'\[\[[^\]]*\|([^\]]*)\]\]')
link_filter = re.compile(r'\[\[([^\]]*)\]\]')

meanings = re.compile(r'^# (.*)$', re.MULTILINE)
l_template_filter = re.compile(r'{{lb?\|[^\|]*\|([^}]*)}}')
empty_brackets = re.compile(r'\(+[^a-zA-Z\}]*\)+')
ascii_filter = re.compile(r'[^\u0000-\u00FF]+')
non_gloss = re.compile(r'{{non-gloss definition\|([^}]*)}}')

noshow_templates = re.compile(r'{{[^}]*noshow[^}]*}}')
n_g_template = re.compile(r'{{n-g\|([^}]*)}}')
gloss_templates = re.compile(r'{{gloss\|([^}]*)}}')
vern_templates = re.compile(r'{{vern\|([^}]*)}}')

remaining_templates = re.compile(r'{{[^}]*}}')

too_many_spaces = re.compile(r' {2,}')

double_punctuation = re.compile(r'[,.?!;:\s]+([,.?!;:])')
short_for_filter = re.compile(r'{{(short for)\|ko\|[^\|]*\|t=([^|}]*)}}')
alternative_filter = re.compile(r'{{(alternative[a-zA-Z\s]*)\|ko\|[^\|]*\|t=([^|}]*)(?:\|[^\}]*)*}}')
synonym_filter = re.compile(r'{{(syn[a-zA-Z\s]*)\|ko\|[^\|]*\|t=([^|}]*)}}')
q_templates = re.compile(r'{{q\|([^}]*)}}')

senseid_filter = re.compile(r'{{senseid\|([^}]*)}}')
gl_filter = re.compile(r'{{gl\|([^}]*)}}')
category_template = re.compile(r'{{[Cc]\|ko\|([^}]*)}}')

html_comments_filter = re.compile(r'<!--.*?-->')

def replace_space(text: str):
    return too_many_spaces.sub(' ', text.replace('_', ' ').replace('|', ' '))


def replace_links(text):
    return link_filter.sub(r'\1', named_link.sub(r'\1', text))


def replace_l_templates(text):
    return l_template_filter.sub(r'\1', text)


def filter_l_templates(text):
    return l_template_filter.sub(r'(\1)', text)


def remove(template):
    def rr(text):
        return template.sub('', text)

    return rr


def replace(template):
    def rr(text):
        return template.sub(r'\1', text)

    return rr

def replace2(template):
    def rr(text):
        return template.sub(r'\1 \2', text)

    return rr


def bracketed(template):
    def rr(text):
        return template.sub(r'(\1)', text)

    return rr


def apply_all(funcs, text):
    for function in funcs:
        text = function(text)
    return text


def replace_unwanted(text):
    return apply_all(
        [
            remove(html_comments_filter),
            bracketed(non_gloss),
            remove(style_filter),
            replace(named_link),
            replace(link_filter),
            filter_l_templates,
            remove(noshow_templates),
            replace(vern_templates),
            replace(gloss_templates),
            replace(n_g_template),
            replace2(short_for_filter),
            replace2(alternative_filter),
            replace2(synonym_filter),
            bracketed(q_templates),
            bracketed(category_template),
            # cleanup
            remove(senseid_filter),
            bracketed(gl_filter),
            remove(remaining_templates),
            replace_space,
            remove(empty_brackets),
            replace(double_punctuation),
        ],
        text
    ).strip()
