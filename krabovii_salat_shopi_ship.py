from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    return render_template("index1.html")
@app.route("/about")
def about():
    return render_template("about krabovii_salat_shop_ship.html")

@app.route("/olivie luche chem krabovii salat")
def contacts():
    return render_template("nepravda.html")


if __name__ == "__main__":
    app.run(debug=True)