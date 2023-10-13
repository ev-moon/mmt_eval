#!/bin/bash
# Script to run asynchronous OpenAI API requests.

search_dir=$(pwd)
for entry in "$search_dir"/*
do
    ext="${entry##*.}"
    if [ "$ext" == "jsonl" ];then
        simple_name=$(basename $entry .jsonl)
        save_filename="gpt_${simple_name}.txt"
        echo $save_filename
        python query_chatgpt_parallel.py --requests_filepath $entry --save_filepath $save_filename --request_url https://api.openai.com/v1/chat/completions --max_requests_per_minute 60 --max_tokens_per_minute 60000 --max_attempts 5 --logging_level 20
    fi
done