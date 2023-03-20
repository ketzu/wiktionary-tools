import csv
import pickle
from collections import defaultdict

from utility.filters import meanings, replace_unwanted

collected_templates = "template_content.pkl"
vocab_file = "vocab.csv"


def nested_defaultdict():
    return defaultdict(list)


def find_meaning(content: str):
    for rest, section_content in content:
        for meaning in meanings.findall(section_content):
            yield replace_unwanted(meaning)


if __name__ == '__main__':
    with open(collected_templates, 'rb') as f:
        data = pickle.load(f)

    with open(vocab_file, 'w', encoding="utf8", newline='') as vf:
        vocab_csv = csv.writer(vf)
        for title, templates in data.items():
            for template_type, content in templates.items():
                for translation in find_meaning(content):
                    if len(translation) > 0:
                        vocab_csv.writerow([title, template_type, translation])
