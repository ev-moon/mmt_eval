"""
Generates the request files(*.jsonl) needed for parallel API requests.
"""
import json

from datasets import load_dataset
import pandas as pd

from translation_utils import wmt_languages, ENGLISH
from query_chatgpt import get_request_message

def get_requests(l1, l2, t1, t2):
    _get_requests(l1, l2, t1)
    _get_requests(l2, l1, t2)

def _get_requests(l1, l2, text):
    filename = f"wmt14_{l1}_{l2}.jsonl"
    requests = [get_request_message(l1, l2, t) for t in text]
    with open(filename, "w") as f:
        for r in requests:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

for l in wmt_languages:
    data = load_dataset("wmt14", f"{wmt_languages[l]}-en", split="test")
    df = pd.DataFrame(data["translation"])
    translations = df[wmt_languages[l]].values
    english = df[ENGLISH].values
    get_requests(l, "English", translations, english)