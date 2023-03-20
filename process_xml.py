import pickle
from pathlib import Path
import xml.etree.ElementTree as ET
import re

filename = r"C:\Users\david\Downloads\enwiktionary\data.xml"
file = Path(filename)

prefix = "{http://www.mediawiki.org/xml/export-0.10/}"

contains_korean = re.compile(r'[\uac00-\ud7a3]+')
contains_type = re.compile(r'^[A-Z][a-z]*:', re.MULTILINE)
section_filter = re.compile(r'^(=+[^=]+=+)(.+?)(?=^=+[^=]+=+)', re.MULTILINE | re.DOTALL)


def tag(x: str):
    return prefix + x


def count_equals(x: str):
    return len(x) - len(x.lstrip('='))


if __name__ == '__main__':
    print(file.exists())
    print(file.is_file())

    data = []
    counter = 0

    # get file into xml elementtree
    context = ET.iterparse(file, events=('end',))

    for event, element in context:

        if element.tag == tag('page'):
            if counter % 10000 == 0:
                print(counter)
            counter += 1

            title = element.find(tag('title')).text
            if contains_korean.search(title) is None or contains_type.search(title) is not None:
                element.clear()
                continue
            else:
                text = element.find(tag('revision')).find(tag('text')).text
                sections = section_filter.findall(text)
                relevant = []
                found = None
                for section in sections:
                    if found is not None:
                        if count_equals(section[0]) <= found:
                            break
                        relevant.append(section)
                    if section[0].strip('=') == 'Korean':
                        found = count_equals(section[0])
                        relevant.append(section)

                data.append((title, relevant))
    print(f"Finished with {counter} pages read and {len(data)} relevant pages.")
    pickle.dump(data, open('data.pkl', 'wb'))
