from get_response import *
import os
import sys
import io
import json
from datetime import datetime
from utils import *
import random
import argparse
import textwrap
import re
from local_llm import ChatGLM
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

SINGLE_CHOICE_PROMPT = "本题为单选题，请务必以[[]]形式给出答案，比如[[A]]。"
MULTI_CHOICE_PROMPT = "本题为多选题，请务必以[[]]形式给出答案，并用'/'分隔答案，比如[[A/B/C]]。"

PROMPT_TEMPLATE = textwrap.dedent(
    """\
    {few_shot}

    问题：{question}
    选项：{options}
    {cprompt}
    回答：
    """
)

COT_PROMPT_TEMPLATE = textwrap.dedent(
    """\
    {few_shot}

    问题：{question}
    选项：{options}
    请你一步步思考并回答。{cprompt}
    回答：
    """
)

SELF_CONS_EVAL_TEMPLATE = textwrap.dedent(
    """\
    {few_shot}
    问题：{question}
    选项：{options}

    以下是5个针对本题的回答：
    回答1：{alter_answer1}
    回答2：{alter_answer2}
    回答3：{alter_answer3}
    回答4：{alter_answer4}
    回答5：{alter_answer5}

    请结合这些回答和对本题的分析给出你认为正确的答案，{cprompt}
    回答：
    """
)

ITERATION_TEMPLATE = textwrap.dedent(
    """\
    {few_shot}
    问题：{question}
    选项：{options}

    以下是1个针对本题的回答：
    回答：{alter_answer}

    请判断该回答的正确性，并针对本题一步一步思考，重新给出你完整的推理和答案。{cprompt}
    回答：
    """
)

def extract_answer(response):
    '''
    通过正则表达式匹配获取最后的结果
    '''
    pattern = r"\[\[([A-Fa-f/]+)\]\]"
    match = re.search(pattern, response)
    if match != None:
        return match.group(1).split('/')
    else:
        return []


def constructPrompt(question):
    problem = question['question']
    options = '；'.join(question['options'])
    if args.cot:
        return COT_PROMPT_TEMPLATE.format(few_shot=few_shot, question=problem, options=options, cprompt=SINGLE_CHOICE_PROMPT if question['type']=='CQ' else MULTI_CHOICE_PROMPT)
    else:
        return PROMPT_TEMPLATE.format(few_shot=few_shot, question=problem, options=options, cprompt=SINGLE_CHOICE_PROMPT if question['type']=='CQ' else MULTI_CHOICE_PROMPT)

def constructPromptForSCE(question, alter_answers):
    problem = question['question']
    options = '；'.join(question['options'])
    return SELF_CONS_EVAL_TEMPLATE.format(few_shot=few_shot, question=problem, options=options, alter_answer1=alter_answers[0], alter_answer2=alter_answers[1], alter_answer3=alter_answers[2], alter_answer4=alter_answers[3], alter_answer5=alter_answers[4], cprompt=SINGLE_CHOICE_PROMPT if question['type']=='CQ' else MULTI_CHOICE_PROMPT)

def constructPromptForIterationStudy(question, alter_answer):
    problem = question['question']
    options = '；'.join(question['options'])
    return ITERATION_TEMPLATE.format(few_shot=few_shot, question=problem, options=options, alter_answer=alter_answer, cprompt=SINGLE_CHOICE_PROMPT if question['type']=='CQ' else MULTI_CHOICE_PROMPT)


def writeFinal(responses, queryList, gtList, idxList, save_dir):
    res = []
    for i, response in enumerate(responses):
        isCorrect = -1
        response_answer = extract_answer(response)
        if response_answer != []:
            isCorrect = 1 if response_answer == gtList[i] else 0
        res.append({
            'idx': idxList[i],
            'query': queryList[i],
            'response': response,
            'gpt_answer': response_answer,
            'gt': gtList[i],
            'isCorrect': isCorrect
        })
    if start_index != 0:
        res = responded + res
    write_new(res, save_dir)
    return

def webChat(questionList, idxList):
    queryList = []
    gtList = []
    for idx, ques in enumerate(questionList):
        if args.self_cons_cot:
            content = constructPrompt(ques)
            for i in range(5):
                queryList.append([
                    {"role": "user", "content": content}
                ] if args.web_LLM == 'gpt-3.5-turbo' else content)
                gtList.append(ques['answer'])
        elif args.self_cons_eval:
            content = constructPromptForSCE(ques, alternative_answer_lists[idx])
            queryList.append([
                {"role": "user", "content": content}
            ] if args.web_LLM == 'gpt-3.5-turbo' else content)
            gtList.append(ques['answer'])
        elif args.iteration_study:
            content = constructPromptForIterationStudy(ques, iteration_ans_list[idx])
            queryList.append([
                {"role": "user", "content": content}
            ] if args.web_LLM == 'gpt-3.5-turbo' else content)
            gtList.append(ques['answer'])
        else:
            content = constructPrompt(ques)
            queryList.append([
                {"role": "user", "content": content}
            ] if args.web_LLM == 'gpt-3.5-turbo' else content)
            gtList.append(ques['answer'])
    responses = concurrent_manager(queryList, args.web_LLM)
    writeFinal(responses, queryList, gtList, idxList, args.save_dir)
    return

def localChat(questionList, idxList):
    llm = ChatGLM()
    queryList = []
    gtList = []
    responses = []
    for idx, ques in tqdm(enumerate(questionList), total=args.num):
        if args.self_cons_cot:
            content = constructPrompt(ques)
            for i in range(5):
                queryList.append(content)
                gtList.append(ques['answer'])
                responses.append(llm.get_response(content))
        elif args.self_cons_eval:
            content = constructPromptForSCE(ques, alternative_answer_lists[idx])
            queryList.append(content)
            gtList.append(ques['answer'])
            responses.append(llm.get_response(content))
        else:
            content = constructPrompt(ques)
            queryList.append(content)
            gtList.append(ques['answer'])
            responses.append(llm.get_response(content))
    writeFinal(responses, queryList, gtList, idxList, args.save_dir)
    return


def main():
    questionListTotal = getQuestionList(args.dataset)
    questionList = questionListTotal[start_index:start_index+args.num]
    idxList = list(range(start_index, start_index+args.num))
    idxList = [val for val in idxList for i in range(5)] if args.self_cons_cot else idxList
    if args.local_LLM == None:
        webChat(questionList, idxList)
    else:
        localChat(questionList, idxList)
    return 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=str, help="which subject to evaluate, used in fewshot setting.")
    parser.add_argument("--dataset", type=str, help="dataset path")
    parser.add_argument("--num", type=int, help="number of question to be asked")

    parser.add_argument("--few_shot", action="store_true", default=False, help="Whether to use few shot")
    parser.add_argument("--cot", action="store_true", default=False, help="Whether to use cot")
    parser.add_argument("--self_cons_cot", action="store_true", default=False, help="Whether to use self-consistency cot")
    parser.add_argument("--self_cons_eval", action="store_true", default=False, help="Whether to use self-consistency evaluation")
    parser.add_argument("--self_cons_eval_path", default=None, help="path of alternative answers when using self-consistency evaluation.")
    parser.add_argument("--iteration_study", action="store_true", default=False, help="Whether to conduct iteration_study.")
    parser.add_argument("--last_iteration_path", type=str, default=None)

    parser.add_argument("--web_LLM", choices=['gpt-3.5-turbo', 'text-davinci-003'], default='gpt-3.5-turbo', help="which web LLM to use")
    parser.add_argument("--local_LLM", choices=['ChatGLM', None], default=None, help="which local LLM to use")
    parser.add_argument("--save_dir", type=str, required=True, help="save directory")
    args = parser.parse_args()

    if args.few_shot:
        with open(f'../data/{args.subject}/few_shot.txt', 'r', encoding='utf-8') as f:
            few_shot = f.read()
    else:
        few_shot = ''

    if os.path.exists(args.save_dir):
        with open(args.save_dir, 'r', encoding='utf-8') as f:
            responded = json.load(f)
        start_index = responded[-1]['idx']+1
        print('Continue, starting from {}, num {}'.format(start_index, args.num))
    else:
        print('Starting from new.')
        start_index = 0

    if args.self_cons_cot:
        args.cot = True
    
    alternative_answer_lists = []
    if args.self_cons_eval:
        with open(args.self_cons_eval_path, 'r', encoding='utf-8') as f:
            alternative_res_list = json.load(f)
        for i in range(args.num):
            if (start_index+i)*5 > len(alternative_res_list):
                break
            alternative_answer_lists.append([item['response'][:400] for item in alternative_res_list[(start_index+i)*5:(start_index+i)*5+5]])
        # print(len(alternative_answer_lists))
    if args.iteration_study:
        if args.last_iteration_path == None or not os.path.exists(args.last_iteration_path):
            print("Give last iteration path.")
            exit()
        else:
            iteration_ans_list = []
            with open(args.last_iteration_path, 'r', encoding='utf-8') as f:
                iteration_res_list = json.load(f)
            for i in range(args.num):
                if start_index+i > len(iteration_res_list)-1:
                    break
                iteration_ans_list.append(iteration_res_list[start_index+i]['response'][:3000])
    print(args)
    main()