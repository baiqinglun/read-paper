from openai import OpenAI
import openai
import time
import PyPDF2
import pandas as pd
import json
import os
from pathlib import Path

# 定义自己的 key
key = "API-KEY"
# 访问的接口
# api_url = "https://api.deepseek.com"
api_url = "https://api.moonshot.cn/v1"
# 指定输出文件路径
output_file = 'output.xlsx'

def get_all_file_paths(folder_path):
    file_paths = []

    # 遍历指定文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 获取完整文件路径
            full_path = os.path.join(root, file)
            file_paths.append(full_path)

    return file_paths

def read_pdf(file_path):
    context = ""

    # 打开PDF文件
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # 获取PDF总页数
        num_pages = len(reader.pages)
        print(f'Total pages: {num_pages}')
        
        # 读取每一页的内容
        for i in range(num_pages):
            page = reader.pages[i]
            text = page.extract_text()
            context += text
    return context

def sendToDeepSeek(file_path):
    print('正在验证身份，请稍等....')
    # 请求接口并验证身份，创建客户端对象
    client = OpenAI(api_key=key, base_url=api_url)
    print('正在思考，请耐心等待...')
    # 发送请求数据并等待获取响应数据
    file_object = client.files.create(file=Path(file_path), purpose="file-extract")
    file_content = client.files.content(file_id=file_object.id).text

    # 把它放进请求中
    messages = [
            {
                "role": "system",
                # "content": "您是一名经验丰富的研究学者，我将会发送一些学术文献给您，请您仔细阅读文献内容，并为我详细讲解文献的各个部分，解答我的疑问。这对我非常重要，因此我希望您能够认真对待，确保每个问题都能得到准确和深入的回答。完成任务后，我将给予丰厚的报酬。注意！请您详细阅读文章内容，不要偷懒！要求内容实事求是，不准篡改原文意图，分析题目、研究目的、研究内容、研究方法、研究结果、研究结论、关键词以及文章主要内容，格式为"{"title": "Evaluation of burst pressure prediction models for line pipes\", \"研究目的\": \"评估用于油气管道的爆破压力预测模型的准确性。\", \"研究内容\": \"研究比较了基于塑性理论的三种解决方案（Tresca准则、von Mises准则和ZL（Zhu-Leis）准则）以及基于圆柱不稳定性应力（CIS）概念的解决方案和其他先前评估过的分析和经验模型。\", \"研究方法\": \"使用包含100多次测试的爆破压力数据库，涵盖多种管道钢级别和尺寸，通过统计分析预测模型的均值误差和标准差来衡量预测的可行性。\", \"研究结果\": \"Zhu-Leis解决方案在预测爆破压力方面表现最佳，包括考虑应变硬化效应，而Tresca强度解决方案如Barlow、最大剪切应力、Turner和ASME锅炉代码为中等应变硬化响应的管线钢类提供了合理的预测。\", \"研究结论\": \"Zhu-Leis模型基于统计评估被认为是预测爆破压力的最佳方程。Tresca强度解决方案包括Barlow（最好使用平均直径）、最大剪切应力、Turner、ASME锅炉代码和Bailey-Nadai模型，为中等至高Y/T（0.7至0.9）的管线钢提供了合理的爆破压力预测。\", \"关键词\": \"Pipeline Burst pressure Predictive model Y/T ratio Tresca criterion von Mises criterion\", \"主要内容概述\": \"本文重新评估了大量用于无缺陷管道端盖的爆破压力预测模型，这些模型最初由Law和Bowie考虑，包括CIS和Zhu-Leis解决方案。在将模型归类为使用Tresca和von Mises准则之后，报告了详细的统计分析，对比了109个全尺寸爆破测试的预测与观察到的破坏压力，包括Law和Bowie最初考虑的五个爆破测试。确定了每个预测模型的均值误差和标准差，并用这些结果评估了每个模型的质量和适用性。讨论还补充了使用专有的EPRG数据库进行的类似分析，该数据库包括38个额外的全尺寸爆破测试。\}，不许更改此格式。研究目的、研究内容、研究方法、研究结果、研究结论和文章主要内容要详尽，严格以python中的字典格式给出，严格在字典中使用英文双括号包括字段和值，不能使用单引号\"},
                # "content": "您是一名经验丰富的研究学者，我将会发送一些学术文献给您，请您仔细阅读文献内容，并为我详细讲解文献的各个部分，解答我的疑问。这对我非常重要，因此我希望您能够认真对待，确保每个问题都能得到准确和深入的回答。完成任务后，我将给予丰厚的报酬。注意！请您详细阅读文章内容，不要偷懒！要求内容实事求是，不准篡改原文意图，分析题目、研究目的、研究内容、研究方法、研究结果、研究结论、关键词以及文章主要内容，格式为'{"title": "Evaluation of burst pressure prediction models for line pipes", "研究目的": "评估用于油气管道的爆破压力预测模型的准确性。", "研究内容": "研究比较了基于塑性理论的三种解决方案（Tresca准则、von Mises准则和ZL（Zhu-Leis）准则）以及基于圆柱不稳定性应力（CIS）概念的解决方案和其他先前评估过的分析和经验模型。", "研究方法": "使用包含100多次测试的爆破压力数据库，涵盖多种管道钢级别和尺寸，通过统计分析预测模型的均值误差和标准差来衡量预测的可行性。", "研究结果": "Zhu-Leis解决方案在预测爆破压力方面表现最佳，包括考虑应变硬化效应，而Tresca强度解决方案如Barlow、最大剪切应力、Turner和ASME锅炉代码为中等应变硬化响应的管线钢类提供了合理的预测。", "研究结论": "Zhu-Leis模型基于统计评估被认为是预测爆破压力的最佳方程。Tresca强度解决方案包括Barlow（最好使用平均直径）、最大剪切应力、Turner、ASME锅炉代码和Bailey-Nadai模型，为中等至高Y/T（0.7至0.9）的管线钢提供了合理的爆破压力预测。", "关键词": "Pipeline Burst pressure Predictive model Y/T ratio Tresca criterion von Mises criterion", "主要内容概述": "本文重新评估了大量用于无缺陷管道端盖的爆破压力预测模型，这些模型最初由Law和Bowie考虑，包括CIS和Zhu-Leis解决方案。在将模型归类为使用Tresca和von Mises准则之后，报告了详细的统计分析，对比了109个全尺寸爆破测试的预测与观察到的破坏压力，包括Law和Bowie最初考虑的五个爆破测试。确定了每个预测模型的均值误差和标准差，并用这些结果评估了每个模型的质量和适用性。讨论还补充了使用专有的EPRG数据库进行的类似分析，该数据库包括38个额外的全尺寸爆破测试。}，不许更改此格式。研究目的、研究内容、研究方法、研究结果、研究结论和文章主要内容要详尽，严格以python中的字典格式给出，严格在字典中使用英文双括号包括字段和值，不能使用单引号"},
                # "content": "您是一名经验丰富的研究学者，我将会发送一些学术文献给您，\
                # 请您仔细阅读文献内容，并为我详细讲解文献的各个部分，解答我的疑问。\
                # 这对我非常重要，因此我希望您能够认真对待，确保每个问题都能得到准确和深入的回答。\
                # 完成任务后，我将给予丰厚的报酬。注意！请您详细阅读文章内容，不要偷懒！\
                # 要求内容实事求是，不准篡改原文意图，\
                # 分析题目、研究目的、研究内容、研究方法、研究结果、研究结论、关键词以及文章主要内容，\
                # 格式为{"title":\"da\",\"研究目的\":\"p1\",\"研究内容\":\"p2\",\"研究方法\":\"p2\",\"研究结果\":\"p2\",\"研究结论\":\"p1\",\"主要内容\":\"da\"]，\
                # 不许更改此格式。研究目的、研究内容、研究方法、研究结果、研究结论和文章主要内容要详尽，\
                # 严格以python中的字典格式给出，严格在字典中使用英文双括号包括字段和值，不能使用单引号"
                "content": "您是一名经验丰富的研究学者，我将会发送一些学术文献给您，\
                请您仔细阅读文献内容，并为我详细讲解文献的各个部分，解答我的疑问。\
                这对我非常重要，因此我希望您能够认真对待，确保每个问题都能得到准确和深入的回答。\
                完成任务后，我将给予丰厚的报酬。注意！请您详细阅读文章内容，不要偷懒！\
                要求内容实事求是，不准篡改原文意图，\
                分析题目、研究目的、研究内容、研究方法、研究结果、研究结论、关键词以及文章主要内容，\
                格式为{\"title\":\"p2\",\"研究目的\":\"p1\",\"研究内容\":\"p2\",\"研究方法\":\"p2\",\"研究结果\":\"p2\",\"研究结论\":\"p1\",\"关键词\":\"p2\",\"主要内容\":\"da\"]，\
                不许更改此格式。研究目的、研究内容、研究方法、研究结果、研究结论和文章主要内容要详尽并使用中文，\
                严格以python中的字典格式给出，严格在字典中使用英文双括号包括字段和值，不能使用单引号"
            },
            {
                "role": "system",
                "content": file_content
            },
            {
                "role": "user", 
                "content": "请简单介绍pdf中讲了啥"
            }
    ]
    response = client.chat.completions.create(
    model="moonshot-v1-32k",
    # model="deepseek-chat",
    messages=messages,
    temperature=0.3,
    )
    # response = client.chat.completions.create(
    #     # model="deepseek-chat",
    #     model = "moonshot-v1-8k",
    #     messages=[
    #         {"role": "system", "content": "您是一名经验丰富的研究学者，我将会发送一些学术文献给您，请您仔细阅读文献内容，并为我详细讲解文献的各个部分，解答我的疑问。这对我非常重要，因此我希望您能够认真对待，确保每个问题都能得到准确和深入的回答。完成任务后，我将给予丰厚的报酬。注意！请您详细阅读文章内容，不要偷懒！要求内容实事求是，不准篡改原文意图，格式为题目、研究目的、研究内容、研究方法、研究结果、研究结论、关键词以及一段话详细概括文章主要内容，研究目的、研究内容、研究方法、研究结果、研究结论和文章主要内容要详尽，不许更改此格式，严格以python中的字典格式给出，字典中使用英文双括号包括字段和值"},
    #         # {"role": "system", "content": "你是风趣幽默的客服，请用轻松幽默的语气回答用户的问题。"},
    #         {"role": "user", "content": say},
    #     ],
    #     stream=False
    # )
    return response.choices[0].message.content



def make_request_with_retries(file_path,max_retries=5, wait_time=1):
    for attempt in range(max_retries):
        try:
            response = sendToDeepSeek(file_path)  # 用实际的 API 调用替换
            return response  # 如果请求成功，返回响应

        except openai.RateLimitError as e:
            print(f"Rate limit exceeded. Attempt {attempt + 1}/{max_retries}. Waiting {wait_time} seconds...")
            time.sleep(wait_time)  # 等待一段时间后重试
            
            # 逐步增加等待时间（指数退避）
            wait_time *= 2  # 可以选择保持此行（指数退避）或直接使用固定的等待时间

# 如果文件已存在，先读取现有数据
for file_path in get_all_file_paths("exp"):
    try:
        response = make_request_with_retries(file_path)
        print("Request successful:", response)
        data = json.loads(response)
        new_data_df = pd.DataFrame([data])

        if os.path.exists(output_file):
            existing_df = pd.read_excel(output_file)
        else:
            existing_df = pd.DataFrame()

        # 合并新数据和现有数据
        combined_df = pd.concat([existing_df, new_data_df], ignore_index=True)
        # 将合并后的DataFrame写入Excel
        combined_df.to_excel(output_file, index=False)
    except Exception as e:
        print("Error:", e)
