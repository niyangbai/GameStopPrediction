# -*- coding: utf-8-sig -*-
import praw
from praw.models import MoreComments
import datetime as dt
import pandas as pd
from psaw import PushshiftAPI

username = 'niyangbai'
with open('pw.txt', 'r') as f:
    pw = f.read()
CLIENT_ID = 'w66eheluJKCHiSWF8oZmfw'
CLIENT_KEY = 'OlKg7Wd019ARZe50pgzqDPEdvG5OnA'
start_time = dt.datetime(2022, 4, 1)
end_time = dt.datetime(2022, 4, 2)
spam_user = ['VisualMod', 'AutoModerator']
path = 'aaa.csv'

class API:
    def __init__(self, client_id, client_key, username, passwd):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_key,
            password=passwd,
            user_agent="thesis",
            username=username,
            check_for_async=False)

    def get_data(self, start_time, end_time, spam_user=[], limit = None):
        api = PushshiftAPI(self.reddit)
        start_epoch = int(start_time.timestamp())
        end_epoch = int(end_time.timestamp())
        submissions_generator = api.search_submissions(after=start_epoch,
                                                       before=end_epoch,
                                                       subreddit='wallstreetbets',
                                                       limit=limit)
        submissions = list(submissions_generator)

        submissions_dict = {"id": [],
                            "url": [],
                            "title": [],
                            "score": [],
                            "num_comments": [],
                            "created_utc": [],
                            "selftext": [],
                            "top_comments": []}

        spam_user = spam_user

        for submission_id in submissions:
            submission_praw = self.reddit.submission(id=submission_id)
            submissions_dict["id"].append(submission_praw.id)
            submissions_dict["url"].append(submission_praw.url)
            submissions_dict["title"].append(submission_praw.title)
            submissions_dict["score"].append(submission_praw.score)
            submissions_dict["num_comments"].append(submission_praw.num_comments)
            submissions_dict["created_utc"].append(submission_praw.created_utc)
            submissions_dict["selftext"].append(submission_praw.selftext)
            submission_praw.comment_sort = "top"
            submission_praw.comment_limit = 10
            top_comments = []
            for comment in submission_praw.comments:
                if isinstance(comment, MoreComments):
                    continue
                if comment.author not in spam_user:
                    top_comments.append(comment.body)
            submissions_dict["top_comments"].append(' . '.join(top_comments))

        df = pd.DataFrame(submissions_dict)
        return df

### test
a = API(CLIENT_ID, CLIENT_KEY, username, pw)
print(a.get_data(start_time, end_time, limit = 5))
