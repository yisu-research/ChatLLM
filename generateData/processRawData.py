import docx
import os
from docx import Document
import jsonlines
import pandas as pd

outputPath = "processedData.json"
def processDocx(path="./rawdata/"):
    listPath = os.listdir(path)
    with jsonlines.open(outputPath, "w") as writer:
        for item in listPath:
            document = Document(f"{path}{item}")
            question = item.strip(r".docx").strip()
            answers = []
            for paragraph in document.paragraphs:
                answers.append(paragraph.text.replace("\n", ""))
            answer = "\n".join(answers)
            var = {"prompt": question, "chosen": answer, "rejected": ""}
            writer.write(var)

def processCsv(path ="./rawQA/副本大模型问答内容对话数据0712.csv"):
    data = pd.read_csv(path)
    data = data[["Human/Bot","对话数据"]]
    data = data.fillna("")
    dataType = data["Human/Bot"]
    dataContent = data["对话数据"]

    prompt = ""
    answer = ""
    with jsonlines.open(outputPath, "a") as writer:
        for i in range(len(dataType)):
            if dataType[i] == "":
                writer.write({"prompt": prompt, "chosen": answer, "rejected": ""})
                prompt = ""
                answer = ""
            else:
                prompt += answer
                answer = dataContent[i]
        writer.write({"prompt": prompt, "chosen": answer, "rejected": ""})


if __name__ == '__main__':
    processDocx()
    processCsv()