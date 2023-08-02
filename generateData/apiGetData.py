# This is a sample Python script.
from random import Random
import jsonlines
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import openai
from tqdm import tqdm

openai.api_key = 'xx'
MODEL = "gpt-3.5-turbo"

QAList = []
with jsonlines.open("processedData.json") as reader:
    for item in reader:
        QAList.append(item)

with jsonlines.open("问题融合v1数据.json","w") as writer:
    for repeat in range(2):
        for item in tqdm(QAList):
            random = Random()
            randomChoice = random.choice(QAList)
            question = item["prompt"]
            questionNext = randomChoice["prompt"]
            answer = item["chosen"]
            content = f"当前任务需要你根据对话历史，将对话历史中包含多个问题融合为一个问题，以使得被提问人能更好的理解上下文，注意你不能回答问题，你需要将多个问题的语义融合为一个新问题：" \
                                                f"：问题: {question} \n" \
                                                f" 答案：{answer} \n" \
                                                f" 问题：{questionNext} \n"

            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": content
                     },
                ],
                temperature=0,
            )
            output = response['choices'][0]['message']['content']
            print(output)
            try:
                writer.write({"input":content,"output":output})
            except Exception:
                pass
            

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
