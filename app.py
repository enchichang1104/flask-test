# from flask import Flask, render_template, request
# import openai
# import PyPDF2

# app = Flask(__name__)

# # 设置您的 OpenAI API 密鑰
# openai.api_key = "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"

# # 函數用於從 PDF 文件中提取摘要
# def extract_summary_from_pdf(file_path):
#     # 讀取 PDF 文件
#     with open(file_path, "rb") as file:
#         reader = PyPDF2.PdfReader(file)
#         text = "給我檔案的重點摘要全英文的，且不要有亂碼"
#         for page in reader.pages:
#             text += page.extract_text()

#     # 調用 OpenAI 的摘要模型
#     response = openai.Completion.create(
#         engine="gpt-3.5-turbo-instruct",
#         prompt=text,
#         max_tokens=2000
#     )
    
#     # 提取摘要
#     summary = response.choices[0].text.strip()
#     return summary

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         # 获取上传的文件
#         uploaded_file = request.files["file"]
#         # 保存上传的文件到服务器
#         uploaded_file_path = "uploads/" + uploaded_file.filename
#         uploaded_file.save(uploaded_file_path)
#         # 提取摘要
#         summary = extract_summary_from_pdf(uploaded_file_path)
#         # 返回摘要页面
#         return render_template("index.html", summary=summary)
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)


import os
import openai
import PyPDF2
from flask import Flask, render_template, request

app = Flask(__name__)

# 设置您的 OpenAI API 密钥
openai.api_key = "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"

# 设置上传文件的临时存储目录
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 函数用于从 PDF 文件中提取摘要
def extract_summary_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    # 调用 OpenAI 的摘要模型
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=text,
        max_tokens=200
    )

    # 提取摘要
    summary = response.choices[0].text.strip()
    return summary

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    if request.method == "POST":
        # 获取上传的文件
        uploaded_file = request.files["file"]
        if uploaded_file.filename != '':
            # 保存上传的文件到服务器
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)
            # 提取摘要
            summary = extract_summary_from_pdf(file_path)
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
