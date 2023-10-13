from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

from translation_utils import wmt_languages, get_wmt14_sentences, ENGLISH

LANGUAGE_CODES = {
    "German": "de_DE",
    "English": "en_XX",
    "French": "fr_XX",
    "Russian": "ru_RU",
    "Czech": "cs_CZ",
    "Hindi": "hi_IN",
}


def _get_mbart_translation(model, tokenizer, source, target, text, batch_size=10):
    tokenizer.src_lang = LANGUAGE_CODES[source]
    for i in range(0, len(text), batch_size):
        encoded = tokenizer(
            text[i : min(i + batch_size, len(text))].tolist(),
            return_tensors="pt",
            padding=True,
        )
        generated_tokens = model.generate(
            **encoded,
            forced_bos_token_id=tokenizer.lang_code_to_id[LANGUAGE_CODES[target]],
        )
        translations = tokenizer.batch_decode(
            generated_tokens, skip_special_tokens=True
        )
        open(f"mbart_wmt14_{source}_{target}.txt", "a").write(
            "\n".join(translations) + "\n"
        )


def get_mbart_translations():
    model = MBartForConditionalGeneration.from_pretrained(
        "facebook/mbart-large-50-many-to-many-mmt"
    )
    tokenizer = MBart50TokenizerFast.from_pretrained(
        "facebook/mbart-large-50-many-to-many-mmt"
    )
    for l in wmt_languages:
        other, english = get_wmt14_sentences(wmt_languages[l])
        _get_mbart_translation(
            model,
            tokenizer,
            l,
            "English",
            other,
        )
        _get_mbart_translation(model, tokenizer, "English", l, english)


if __name__ == "__main__":
    get_mbart_translations()
