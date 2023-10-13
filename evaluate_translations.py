import argparse

import pandas as pd
from datasets import load_dataset
from sacrebleu.metrics import BLEU


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-tf", "--translations", help="Translations filename", required=True
    )
    parser.add_argument(
        "-m", "--missing-idxs", help="Index of missing translations"
    )  # argument for PALM
    parser.add_argument("-d", "--dataset", help="Name of dataset", required=True)
    parser.add_argument(
        "-s", "--source-language", help="Source Language e.g. en", required=True
    )
    parser.add_argument(
        "-t", "--target-language", help="Target Language e.g. de", required=True
    )
    return parser.parse_args()


def main():
    args = get_arguments()
    bleu = BLEU()
    translations = [l.strip() for l in open(args.translations).readlines()]
    if args.missing_idxs:
        missing_idxs = [int(l.strip()) for l in open(args.missing_idxs).readlines()]
    if args.dataset == "wmt14":
        if args.source_language != "en" and args.target_language != "en":
            raise ValueError("WMT14 dataset only supports translations to/from English")
        language_pair = (
            args.source_language + "-" + args.target_language
            if args.target_language == "en"
            else args.target_language + "-" + args.source_language
        )
    else:
        raise ValueError("Dataset not supported")

    reference = pd.DataFrame(
        load_dataset(args.dataset, language_pair, split="test")["translation"]
    )[args.target_language].values.tolist()
    if args.missing_idxs:
        if len(translations) == len(reference):
            translations = [
                translations[idx]
                for idx in range(len(translations))
                if idx not in missing_idxs
            ]
        reference = [
            reference[idx] for idx in range(len(reference)) if idx not in missing_idxs
        ]
    if len(reference) != len(translations):
        raise RuntimeError("Reference and translation files have different lengths")
    print(bleu.corpus_score(translations, [reference]))


if __name__ == "__main__":
    main()