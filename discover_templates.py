import pickle
import re
from pprint import pprint

filename = "data.pkl"
outfile = "templates.csv"

template_format = re.compile(r'{{(ko-[-a-zA-Z]+)\|')


if __name__ == '__main__':
    with open(filename, 'rb') as f:
        data = pickle.load(f)

    found_templates = {}

    for _, content in data:
        for section_title, section_content in content:
            for template in template_format.findall(section_content):
                found_templates[template] = found_templates.get(template, 0) + 1

    print(found_templates)

    # write found_templates to outfile
    with open(outfile, 'w') as f:
        for template, count in found_templates.items():
            f.write(f"{template},{count}\n")

    liked_templates = []
    for template, count in found_templates.items():
        answer = input(f"Include {template}: {count}?")
        if answer.lower() == 'y':
            liked_templates.append(template)
    pprint(liked_templates)