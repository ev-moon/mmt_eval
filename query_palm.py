import argparse
import os

from google.api_core import retry
import google.generativeai as palm

from translation_utils import get_wmt_2014_translations

parser = argparse.ArgumentParser()
parser.add_argument('-s', "--start_idx", type=int, default=0)
args = parser.parse_args()

palm.configure(api_key=os.getenv("PALM_KEY"))
API_COOLDOWN = 2


@retry.Retry()
def generate_text(*args, **kwargs):
    try:
        return palm.generate_text(*args, **kwargs)
    except Exception as e:
        print(e)
        raise RuntimeError("API exception")


def query_palm(l1, l2, sentence):
    # model = [
    #     m for m in palm.list_models() if "generateText" in m.supported_generation_methods
    # ]
    # model = models[0].name
    # print(models)

    prompt = f"Translate the following text from {l1} to {l2}: {sentence}"
    try:
        completion = generate_text(
            model="models/text-bison-001",
            prompt=prompt,
            max_output_tokens=100,
        )
        result = completion.candidates[0]["output"]
        return result
    except Exception as e:
        print("Exception occurred: Received ")
        print(completion)
        raise e


get_wmt_2014_translations(API_COOLDOWN, query_palm, args.start_idx)