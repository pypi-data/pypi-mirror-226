# -*- coding: utf-8 -*-
import json
from typing import Optional, Sequence, List
import openai
import anthropic
from pydantic import BaseModel
from abc import ABC, abstractmethod
import sys
import os
from typing import Callable, Optional, Sequence, List
import tiktoken
import asyncio
import transformers
import logging
from openai.openai_object import OpenAIObject
sys.path.append(os.path.normpath(f"{os.path.dirname(os.path.abspath(__file__))}/.."))
from oneapi.one_api import batch_chat, OneAPITool

def print_special_token(tokenizer_hf: transformers.PreTrainedTokenizer):
    print(f"""tokenizer:\n 
          vocab_size:{len(tokenizer_hf)},
          eos:{tokenizer_hf.eos_token},{tokenizer_hf.eos_token_id},
          bos:{tokenizer_hf.bos_token},{tokenizer_hf.bos_token_id},
          pad:{tokenizer_hf.pad_token},{tokenizer_hf.pad_token_id},
          unk:{tokenizer_hf.unk_token},{tokenizer_hf.unk_token_id},
          mask:{tokenizer_hf.mask_token},{tokenizer_hf.mask_token_id},
          cls:{tokenizer_hf.cls_token},{tokenizer_hf.cls_token_id},
          sep:{tokenizer_hf.sep_token},{tokenizer_hf.sep_token_id},
          all_special:{tokenizer_hf.all_special_tokens},{tokenizer_hf.all_special_ids},
          """)



if __name__ == "__main__":
    claude_config = '../ant/config/anthropic_config_personal.json'
    openai_config = '../ant/config/openapi_official_chenghao.json'
    azure_config = '../ant/config/openapi_azure_config_xiaoduo_dev5.json'
    config_file = claude_config
    msgs = [
       [dict(role='system',content='现在你是一个天气预报助手'), dict(role='user',content='今天天气不错？'), dict(role='assistant',content='抱歉，我不知道你在说什么'),  dict(role='human',value='告诉我明天的天气')],
    #    [dict(role='system',content='现在你是一个天气预报助手'), dict(role='user',content='今天天气不错？'), dict(role='assistant',content='抱歉，我不知道你在说什么')],
       [dict(role='system',content='现在你是一个天气预报助手'), dict(role='human',value='告诉我明天的天气')],
    #    [dict(role='system',content='现在你是一个天气预报助手')],
       [{'from': 'human', 'value': 'hello'}, {'from': 'assistant', 'value': 'Hello, how can i assistant you today?'}, {'from': 'human', 'value': 'I want to know the weather of tomorrow'}, {'from': 'assistant', 'value': 'The weather of tomorrow is sunny'}],
       '你好',
    #    ['你好', '你好啊'],
       ['你好', '你好啊', '你好你叫啥啊'],
    #    ['你好', '你好啊', '你好你叫啥啊', '我叫小明，你呢']
    ]
    tool = OneAPITool.from_config_file(config_file)
    for msg in msgs:
        print(f'Fromat OpenAI prompt {"*"*50}')
        print(tool._preprocess_openai_prompt(msg))
        print(f'Fromat Claude prompt {"*"*50}')
        try:
            print(tool._preprocess_claude_prompt(msg))
        except AssertionError as e:
            print(f'failed preprocess msg: {msg}')
            pass

    conversations_sharegpt_style = [{"from": "human", "value": "hello"}, {"from": "assistant", "value": "Hello, how can i assistant you today?"}, {"from": "human", "value": "I want to know the weather of tomorrow"}]
    conversations_openai_style = [{"role": "user", "content": "hello"}, {"role": "assistant", "content": "Hello, how can i assistant you today?"}, {"role": "user", "content": "I want to know the weather of tomorrow"}]
    conversation_with_system_msg = [{"role": "system", "content": "Now you are a weather forecast assistant."},{"role": "user", "content": "hello"}, {"role": "assistant", "content": "Hello, how can i assistant you today?"}, {"role": "user", "content": "I want to know the weather of tomorrow"}]
    string_message = "Hello AI!"
    list_of_string_messages = ["Hello AI!", "Hello, how can i assistant you today?", "I want to know the weather of tomorrow"]

    # for msg in [conversations_sharegpt_style, conversations_openai_style, conversation_with_system_msg, string_message, list_of_string_messages]:
    #     res = tool.simple_chat(msg)
    #     print(res)

    # Pass system message independently
    # res = tool.simple_chat("I want to know the weather of tomorrow", system="Now you are a weather forecast assistant.")

    # Async chat 
    res = asyncio.run(tool.asimple_chat("How\'s the weather today?", stream=False))
    print(res)

    # Get embeddings of some sentences for further usage, e.g., clustering
    # embeddings = tool.get_embeddings(["Hello AI!", "Hello world!"])
    # print(len(embeddings))

    # Count the number of tokens
    print(tool.count_tokens(["Hello AI!", "Hello world!"]))
    # print(asyncio.run(batch_chat([claude_config, openai_config, azure_config] , msgs)))  
    # print(tool.simple_chat(['今天天气不错？','抱歉，我不知道你在说什么', '高血压吃什么药']))
    # print(tool.simple_chat([dict(role='user',content='今天天气不错？')]))
