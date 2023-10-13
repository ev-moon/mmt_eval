import time

from datasets import load_dataset
import pandas as pd
from tqdm import tqdm

ENGLISH = "en"

wmt_languages = {
    "German": "de",
    "French": "fr",
    "Hindi": "hi",
    "Czech": "cs",
    "Russian": "ru",
}


def get_translations(dataset_name, l1, l2, t1, t2, cooldown, query_func, start_idx):
    _get_translation(dataset_name, l1, l2, t1, cooldown, query_func, start_idx) # unsupported in PALM
    _get_translation(dataset_name, l2, l1, t2, cooldown, query_func, start_idx)
    print("Finished translating all sentences")


def query_api(l1, l2, sentence, query_func):
    return query_func(l1, l2, sentence)


def _get_translation(dataset_name, l1, l2, text, cooldown, query_func, start_idx):
    translations = []
    failed_idxs = []
    filename = f"{query_func.__name__.split('_')[1]}_{dataset_name}_{l1}_{l2}_from_{start_idx}.txt"
    failed_idx_filename = (
        f"{query_func.__name__.split('_')[1]}_{dataset_name}_{l1}_{l2}_failed_idxs.txt"
    )
    for idx in tqdm(range(len(text))):
        try:
            response = query_api(l1, l2, text[idx], query_func)
        except Exception:
            print(f"Unable to process sentence {start_idx+idx}")
            time.sleep(cooldown)
            failed_idxs.append(str(start_idx + idx))
            continue
        translations.append(response)
        time.sleep(cooldown)
    open(filename, "w").write("\n".join(translations))
    open(failed_idx_filename, "w").write("\n".join(failed_idxs))


def get_wmt_2014_translations(cooldown, query_func, start_idx):
    for l in wmt_languages:
        print(f"Start translations between {l} and English")
        data = load_dataset("wmt14", f"{wmt_languages[l]}-en", split="test")
        df = pd.DataFrame(data["translation"])[start_idx:]
        translations = df[wmt_languages[l]].values
        english = df[ENGLISH].values
        get_translations(
            "wmt14",
            l,
            "English",
            translations,
            english,
            cooldown,
            query_func,
            start_idx,
        )


# Download data
def get_wmt14_dataset():
    for l in wmt_languages:  # download_mode="force_redownload" for cache errors
        load_dataset("wmt14", f"{wmt_languages[l]}-en", split="test")


def get_wmt14_sentences(target, start_idx=0):
    data = load_dataset("wmt14", f"{target}-en", split="test")
    df = pd.DataFrame(data["translation"])[start_idx:]
    translations = df[target].values
    english = df[ENGLISH].values
    return translations, english