from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def runScript():
	if request.method == "POST":
		url = request.form["url"]
		print("url: ",url)
		return redirect(url_for("download", data=url))
	else:
		return render_template("form.html")

@app.route("/download/<path:data>/")
def download(data):
    return f"<h1>{data}</h1>"

if __name__ == "__main__":
    app.run()
