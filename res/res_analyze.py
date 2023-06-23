import json
import re
import argparse

def extract_ans(response_str):
    pattern=[
        r"^选([A-D])",
        r"^选项([A-D])",
        r"答案是\s?选?项?\s?([A-D])",
        r"答案为\s?选?项?\s?([A-D])",
        r"答案应为\s?选?项?\s?([A-D])",
        r"答案选\s?选?项?\s?([A-D])",
        r"答案是:\s?选?项?\s?([A-D])",
        r"答案应该是:\s?选?项?\s?([A-D])",
        r"正确的一项是\s?([A-D])",
        r"答案为:\s?选?项?\s?([A-D])",
        r"答案应为:\s?选?项?\s?([A-D])",
        r"答案:\s?选?项?\s?([A-D])",
        r"答案是：\s?选?项?\s?([A-D])",
        r"答案应该是：\s?选?项?\s?([A-D])",
        r"答案为：\s?选?项?\s?([A-D])",
        r"答案应为：\s?选?项?\s?([A-D])",
        r"答案：\s?选?项?\s?([A-D])",
    ]
    ans_list=[]
    if response_str[0] in ["A",'B','C','D']:
        ans_list.append(response_str[0])
    for p in pattern:
        if len(ans_list)==0:
            ans_list=re.findall(p,response_str)
        else:
            break
    return ans_list

def analyze_res(file_dir, count_cal, is_self_cons=False):
    if 'physics' in file_dir and count_cal:
        with open('../data/physics/calculation_set_idx.txt', 'r') as f:
            cal_set_idx = f.readlines()
            cal_set_idx = [int(item.strip()) for item in cal_set_idx]
    else:
        count_cal = False
    with open(file_dir, 'r', encoding='utf-8') as f:
        res = json.load(f)

    total_num = len(cal_set_idx) if count_cal else len(res)
    correct_num = 0
    unknown_num = 0
    for r in res:
        if count_cal and 'physics' in file_dir and r['idx'] not in cal_set_idx:
            continue
        if r['isCorrect'] == 1:
            correct_num += 1
        elif r['isCorrect'] == -1:
            if len(r['response']) > 0:
                if r['gt'] == extract_ans(r['response']):
                    correct_num += 1
                elif '[[' in r['response']:
                    # print(r['idx'])
                    if r['response'].find('[[')+2 < len(r['response']) and r['response'][r['response'].find('[[')+2] == r['gt'][0]:
                        correct_num += 1
            unknown_num += 1

    print(file_dir)
    print("total num:", total_num)
    print("correct num:", correct_num)
    print("unknown num:", unknown_num)

def complete_dir(subject, model):
    subfix = ['simple', 'cot', 'fewshot', 'fewshot_cot', 'sce', 'fewshot_sce']
    dir_list = []
    for i in subfix:
        dir_list.append('./'+subject+'/'+model+'_'+i+'.json')
    return dir_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=str)
    parser.add_argument("--model", type=str)
    parser.add_argument("--cal", action="store_true", default=False)
    parser.add_argument("--dir", type=str, default=None)
    args = parser.parse_args()
    if args.dir is not None:
        analyze_res(args.dir, args.cal)
        exit()
    dir_list = complete_dir(args.subject, args.model)
    for dir_ in dir_list:
        analyze_res(dir_, count_cal=args.cal)