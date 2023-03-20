import csv
import pickle
from collections import defaultdict

from utility.filters import template_filter, style_filter, replace_links
from utility.lists import tracked_templates, include_context, consider_sentence

filename = "data.pkl"
template_content_file = "template_content.pkl"
sentence_file = "examples.csv"


def nested_defaultdict():
    return defaultdict(list)


if __name__ == '__main__':
    sent_counter = 0
    template_counter = 0
    entries_counter = 0
    with open(filename, 'rb') as f:
        data = pickle.load(f)

    template_contents = defaultdict(nested_defaultdict)
    sentences = []
    for title, content in data:
        for section_title, section_content in content:
            for category, rest in template_filter.findall(section_content):
                if category in tracked_templates:
                    if category in include_context:
                        template_contents[category][title].append((rest, section_content))
                    elif category in consider_sentence:
                        style_filtered = style_filter.sub('', rest)
                        processed_sentence = replace_links(style_filtered).split('|')
                        processed_sentence = [_ for _ in processed_sentence if
                                              '=' not in processed_sentence and not _ == '{{w']
                        if len(processed_sentence) > 2 or len(processed_sentence[0]) <= len("석 잔"):
                            continue
                        sentences.append([title] + processed_sentence)
                        sent_counter += 1
                    template_counter += 1
        entries_counter += 1

    print(f"Found {template_counter} templates and {sent_counter} sentences in {entries_counter} entries.")
    with open(sentence_file, 'w', encoding="utf8", newline='') as sf:
        csv_writer = csv.writer(sf)
        for sentence in sentences:
            csv_writer.writerow(sentence)
    pickle.dump(template_contents, open(template_content_file, 'wb'))
