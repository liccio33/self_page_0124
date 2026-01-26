from flask import Flask, request, redirect, url_for, render_template_string
import os

app = Flask(__name__)

# 上传文件保存的位置
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 如果文件夹不存在就创建
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 允许的文件类型
ALLOWED_EXTENSIONS = {
    "html", "css", "js",
    "png", "jpg", "jpeg", "gif",
    "pdf"
}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# 上传页面
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "没有找到文件"

        file = request.files["file"]

        if file.filename == "":
            return "未选择文件"

        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            return f"上传成功：{file.filename}"

        return "不支持的文件类型"

    # 简单的上传页面（不需要额外 HTML 文件）
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>作品集文件上传</title>
    </head>
    <body>
        <h2>上传你的作品集文件</h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <br><br>
            <input type="submit" value="上传">
        </form>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
    