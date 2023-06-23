import openai
import json
import random
import uuid
import requests
import openai_manager

openai_manager.append_auth_from_config(config_path='openai_config.yml')

def concurrent_manager(messages, model_='gpt-3.5-turbo'):
    '''
    并行的openai-api方法，可以支持多个api同时请求
    input: messages: list(list), 多个对话的集合
    example input:
    messages = [
        [{"role": "user", "content": "你好。"}],
        [{"role": "user", "content": "翻译这句话到英文：我爱你"}],
        [{"role": "user", "content": "Hello!"}, 
         {"role": "assistant", "content": "Hello there!"}, 
         {"role": "user", "content": "Who are you?"}],
        [{"role": "user", "content": "你能做什么？"}]
    ]
    return: responses
    '''
    if model_ != 'gpt-3.5-turbo':
        responses = openai_manager.Completion.create(
            model=model_,
            prompt=messages,
            max_tokens=256,
        )
        assert len(responses) == len(messages)
        res = [response["choices"][0]["text"] for response in responses]
        return res
    else:
        responses = openai_manager.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
        )
        assert len(responses) == len(messages)
        res = [response["choices"][0]["message"]['content'] for response in responses]
        return res
