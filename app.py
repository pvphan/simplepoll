import os.path

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__, template_folder="templates")

if not os.path.exists("polls.csv"):
    structure = {
        "id": [],
        "poll": [],
        "option1": [],
        "option2": [],
        "option3": [],
        "option4": [],
        "votes1": [],
        "votes2": [],
        "votes3": [],
        "votes4": [],
    }

    pd.DataFrame(structure).set_index("id").to_csv("polls.csv")

polls_df = pd.read_csv("polls.csv").set_index("id")


@app.route("/")
def index() -> str:
    return render_template("index.html", polls=polls_df)


@app.route("/polls/<id>")
def polls(id: str) -> str:
    poll = polls_df.loc[int(id)]
    print(poll)
    return render_template("show_poll.html", poll=poll)


@app.route("/vote/<id>/<option>")
def vote(id: str, option: str) -> str:
    cookieKey = f"vote_{id}_cookie"
    cookie = request.cookies.get(cookieKey)
    if cookie is None:
        polls_df.at[int(id), "votes"+option] += 1
        polls_df.to_csv("polls.csv")
        response = make_response(redirect(url_for("polls", id=id)))
        response.set_cookie(cookieKey, option)
        return response
    else:
        return "Cannot vote more than once! Go back <a href=" + url_for("polls", id=id) + ">here</a>"


@app.route("/polls", methods=["GET", "POST"])
def create_poll() -> str:
    if request.method == "GET":
        return render_template("new_poll.html")
    elif request.method == "POST":
        poll = request.form["poll"]
        option1 = request.form["option1"]
        option2 = request.form["option2"]
        option3 = request.form["option3"]
        option4 = request.form["option4"]
        polls_df.loc[max(polls_df.index.values) + 1] = [poll, option1, option2, option3, option4, 0, 0, 0, 0]
        polls_df.to_csv("polls.csv")
        return redirect(url_for("index"))
    else:
        return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

