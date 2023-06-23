import json
import math
import re


subject = 'physics'
model = 'td003'
dir = './'+subject+'/'+model+'_self_cons_cot.json'
count_cal = True
cal_set_idx = []

if 'physics' in dir and count_cal:
    with open('../data/physics/calculation_set_idx.txt', 'r') as f:
        cal_set_idx = f.readlines()
        cal_set_idx = [int(item.strip()) for item in cal_set_idx]
        print(len(cal_set_idx))

with open(dir, 'r', encoding='utf-8') as f:
    res = json.load(f)

# with open('../res/physics/chatgpt_total_sce.json', 'r', encoding='utf-8') as f:
#     res_sce = json.load(f)
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

total_num = len(res)
total_num_div_con = len(cal_set_idx) if count_cal else int(len(res) / 5)
correct_num = 0
for idx in range(0, total_num, 5):
    if count_cal and res[idx]['idx'] not in cal_set_idx:
        continue
    answer_list = []
    gt = res[idx]['gt']
    for r in res[idx: idx+5]:
        if len(r['gpt_answer']) < 1:
            answer = '/'.join(extract_ans(r['response']))
            if answer == [] and '[[' in r['response']:
                asnwer = r['response'][r['response'].find('[[')+2]
        elif len(r['gpt_answer']) > 1:
            answer = '/'.join(r['gpt_answer'])
        else:
            answer = r['gpt_answer'][0]
        answer_list.append(answer)
    if len(answer_list) < 1:
        continue
    maxlabel = max(answer_list, key=answer_list.count)
    if list(maxlabel.split('/')) == gt:
        correct_num += 1
    # elif res_sce[idx//5]['isCorrect'] == 1:
    #     print(idx//5)


print(dir)
print("total num: ", total_num_div_con)
print("correct num: ", correct_num)