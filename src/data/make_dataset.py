# -*- coding: utf-8-sig -*-
import praw
from praw.models import MoreComments
import pandas as pd
from psaw import PushshiftAPI
import time
import datetime as dt


class ApiGetData:

    def __init__(self, client_id, client_key, username, passwd):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_key,
            password=passwd,
            user_agent="thesis",
            username=username,
            check_for_async=False)

    def get_data(self, start_time, end_time, subreddit, spam_user=[], limit=None):
        api = PushshiftAPI(self.reddit)
        start_epoch = int(start_time.timestamp())
        end_epoch = int(end_time.timestamp())
        submissions_generator = api.search_submissions(after=start_epoch,
                                                       before=end_epoch,
                                                       subreddit=subreddit,
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


def data_clean(df):
    deleted = ['[removed]', '[deleted]', '[deleted by user]']
    df_clean = df.replace(deleted, None)
    df_clean = df_clean.loc[df_clean[['title', 'selftext', 'top_comments']].notna().sum(axis=1) != 0, ]
    df_clean = df_clean.replace(r'\n', ' ', regex=True)

    word_col = ['title', 'selftext', 'top_comments']

    for col in word_col:
        df_clean[col] = df_clean[col].replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)
        df_clean[col] = df_clean[col].replace(r'\!\[img\]\S+', '', regex=True)
        df_clean[col] = df_clean[col].replace(r'\[deleted\]', '', regex=True)
        df_clean[col] = df_clean[col].replace(r'\[removed\]', '', regex=True)

    df_clean['created_utc'] = df_clean['created_utc'].apply(lambda x: time.strftime('%m-%d-%y', time.localtime(x)))
    return df_clean


def main():
    import os


    base_dir = os.getcwd()
    username = 'niyangbai'
    with open(os.path.join(base_dir, 'src\\data\\pw.txt'), 'r') as f:
        pw = f.read()
    cid = 'w66eheluJKCHiSWF8oZmfw'
    key = 'OlKg7Wd019ARZe50pgzqDPEdvG5OnA'
    start_time = dt.datetime(2022, 4, 1)
    end_time = dt.datetime(2022, 4, 2)
    spam_user = ['VisualMod', 'AutoModerator']
    subreddit = 'wallstreetbets'

    api = ApiGetData(cid, key, username, pw)
    df_raw = api.get_data(start_time, end_time, subreddit, spam_user)
    df_raw.to_csv(os.path.join(base_dir, 'data\\interim\\df_raw.csv'), index=False, encoding='utf-8-sig')

    df_clean = data_clean(df_raw)
    df_clean.to_csv(os.path.join(base_dir, 'data\\interim\\df_clean.csv'), index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    main()
