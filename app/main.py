import asyncio
import os
import time

import mpld3
from flask import Flask, render_template, request, redirect, url_for

from config import ms_token
from tiktokapi import TikTokApiManager, Visualizer, Color

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        form_username = request.form["search"]
        return redirect(f"/tiktok/{form_username}")

    return render_template("index.html")


@app.route('/tiktok/<username>')
def tiktok(username: str):
    manager = TikTokApiManager(ms_token=ms_token)

    filename = ""
    data = {}

    for filename in os.listdir("../datas"):
        if filename.startswith(f"comments-{username}"):
            d = filename.rstrip(".json").lstrip("comments-").split("-")
            created_at_sec_ago = time.time() - float(d[1])

            # Якщо файлу вже більше аніж 1 день, оновити дані
            if created_at_sec_ago < 86_400:
                data["username"] = d[0]
                data["created_at_sec_ago"] = created_at_sec_ago

    # Отримуємо графіку
    path = asyncio.run(manager.get_user_comments(
        username=username,
        log=True,
        save_dir="../datas"
    )) if not data else "../datas/" + filename
    plt, figure = Visualizer(path).get_plt((15, 10))

    html = mpld3.fig_to_html(figure)
    with open("templates/plt.html", "w") as file:
        file.write(html)
        file.close()

    return render_template("plt.html")


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
