import os
import json
import requests
import datetime
import yaml

def getQuestionList(path):
    with open(path, 'r', encoding='utf-8') as f:
        questionList = json.load(f)
    return questionList

def getQuestion(questionList, **kw):
    '''
    通过 id 或 index 访问questionList
    如果找到对应的question，返回一个
    '''
    if 'id' in kw:
        for question in questionList:
            if question['id'] == kw['id']:
                return question
        return None
    elif 'index' in kw and kw['index'] < len(questionList):
        return questionList[kw['index']]
    elif 'text' in kw:
        for question in questionList:
            if kw['text'] in question['qeustion']:
                return question
    else:
        return None

def write_new(res, path):
    '''
    写入新文件
    '''
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)

def getbalance(apikey):
    '''
    显示openai api 账号余额
    '''
    subscription_url = "https://api.openai.com/v1/dashboard/billing/subscription"
    headers = {
        "Authorization": "Bearer " + apikey,
        "Content-Type": "application/json"
    }
    subscription_response = requests.get(subscription_url, headers=headers)
    if subscription_response.status_code == 200:
        data = subscription_response.json()
        total = data.get("hard_limit_usd")
    else:
        return subscription_response.text

    # end_date设置为今天日期+1
    end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    billing_url = "https://api.openai.com/v1/dashboard/billing/usage?start_date=2023-03-09&end_date=" + end_date
    billing_response = requests.get(billing_url, headers=headers)
    if billing_response.status_code == 200:
        data = billing_response.json()
        total_usage = data.get("total_usage") / 100
        daily_costs = data.get("daily_costs")
        days = min(5, len(daily_costs))
        recent = f"##### 最近{days}天使用情况  \n"
        for i in range(days):
            cur = daily_costs[-i-1]
            date = datetime.datetime.fromtimestamp(cur.get("timestamp")).strftime("%Y-%m-%d")
            line_items = cur.get("line_items")
            cost = 0
            for item in line_items:
                cost += item.get("cost")
            recent += f"\t{date}\t{cost / 100} \n"
    else:
        return billing_response.text

    return f"\n#### 总额:\t{total:.4f}  \n" \
                f"#### 已用:\t{total_usage:.4f}  \n" \
                f"#### 剩余:\t{total-total_usage:.4f}  \n" \
                f"\n"+recent


if __name__ == "__main__":
    with open('openai_config.yml', 'r', encoding='utf-8') as f:
        d = yaml.load(f.read(), Loader=yaml.Loader)
        # print(d)
        for auth in d:
            print(auth)
            apikey = d[auth]['api_key']
            print(apikey)
            print(getbalance(apikey))
    # ql = getQuestionList('../data/ProblemSetClean.json')
    # for item in ql:
    #     if (item['type'] == 'MCQ' and len(item['answer']) <= 1) or (item['type'] == 'CQ' and len(item['answer']) > 1):
    #         print(item['id'])
    