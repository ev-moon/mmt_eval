# Comparison of Languages Models for Machine Translation

Contains scripts to compare the performance of different language models for multilingual machine translation.

Currently supports ChatGPT(GPT-3.5), PALM, and MBART.

## Results

Below is the performance(BLEU) gained with the WMT14 dataset for different language models.

|          | en-de | en-fr | en-cs | en-hi | en-ru |
| -------- | ----- | ----- | ----- | ----- | ----- |
| PALM2    | 28.84 | 38.69 | 26.05 | 23.26 | 36.46 |
| GPT-3.5  | 28.51 | 41.31 | 25.84 | 17.90 | 36.33 |
| mBART-50 | 24.95 | 35.36 | 24.09 | 17.43 | 32.05 |

Refer to the report for more details on implementation and prompting(for PALM2 and GPT-3.5).
