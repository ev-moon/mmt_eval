"""
Script to extract references for translations.
"""
from pathlib import Path

from translation_utils import wmt_languages, get_wmt14_sentences

references_dir = "references"


def get_reference_file(target):
    _, english = get_wmt14_sentences(wmt_languages[target])
    filename = f"{references_dir}/{target}_English_references.txt"
    open(filename, "w").write("\n".join(english))


def get_references():
    Path(references_dir).mkdir(exist_ok=True)  # create references/ directory
    for lang in wmt_languages:
        get_reference_file(lang)


if __name__ == "__main__":
    get_references()