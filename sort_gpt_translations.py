"""
Sort aysnchronous GPT translations by their order in the dataset.
Creates a new file with the sorted translations.
"""
import argparse
import json
import re

import pandas as pd
from datasets import load_dataset

from translation_utils import wmt_languages, ENGLISH


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="Path to the input file."
    )
    return parser.parse_args()


def main():
    args = parse_args()
    _tokens = re.split("[_.]+", args.input)
    source = ENGLISH if _tokens[2] == "English" else wmt_languages[_tokens[2]]
    target = ENGLISH if _tokens[3] == "English" else wmt_languages[_tokens[3]]
    if source == "en":
        data = load_dataset("wmt14", f"{target}-en", split="test")
    else:
        data = load_dataset("wmt14", f"{source}-en", split="test")
    source_sentences = pd.DataFrame(data["translation"])[source].values.tolist()
    source_idxs = {idx: sentence for idx, sentence in enumerate(source_sentences)}
    translation_dict = dict()
    for line in open(args.input).readlines():
        message = json.loads(line.strip())
        source = message[0]["messages"][0]["content"].split("```")[1]
        translation = message[1]["choices"][0]["message"]["content"]
        translation_dict[source] = translation
    with open(f"{args.input.split('.')[0]}_sorted.txt", "w") as f:
        for idx in range(len(source_sentences)):
            f.write(translation_dict[source_idxs[idx]] + "\n")


if __name__ == "__main__":
    main()