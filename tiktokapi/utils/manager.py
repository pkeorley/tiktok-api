import json
import time
from pathlib import Path

from TikTokApi import TikTokApi

from config import COMMENT_LIMIT


class TikTokApiManager:
    def __init__(self, ms_token: str):
        self._ms_token = ms_token

    async def get_user_comments(
            self,
            username: str,
            log: bool = False,
            save_path: str = None,
            save_dir: str = None
    ):
        """
        Asynchronously retrieves comments made by a user on TikTok videos.
        Args:
            username (str): The username of the user whose comments will be retrieved.
            log (bool, optional): Whether to log the progress and details of the retrieval process. Defaults to False.
            save_path (str, optional): The path where the retrieved comments will be saved. Defaults to None.
            save_dir (str, optional): The directory where the retrieved comments will be saved. Defaults to None.
        Returns:
            str: The path to the file where the comments were saved.
        """

        p = (save_dir or "")
        if not p.endswith("/"):
            p += "/"

        if save_path is None:
            p += f"comments-{username}-{time.time()}.json"

        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[self._ms_token], num_sessions=1, sleep_after=3)

            comments = {}

            user = api.user(username)
            account = await user.info()

            async for video in user.videos(count=account["userInfo"]["stats"]["videoCount"]):

                comment_count = video.as_dict["stats"]["commentCount"]
                comment_count = comment_count if comment_count <= COMMENT_LIMIT else COMMENT_LIMIT

                async for comment in video.comments(count=comment_count):

                    if comment.author.username not in comments:
                        comments[comment.author.username] = []

                    if log:
                        print(
                            f"{video.as_dict['id']}  |  ({len(comments[comment.author.username])})  "
                            f"|  {comment.author.username}  =>  {comment.text}")

                    comments[comment.author.username].append(comment.text)

            json.dump(
                {
                    "nickname": username,
                    "comments": comments
                },
                open(p, "w", encoding="utf-8"),
                indent=4,
                ensure_ascii=False
            )

            return p
