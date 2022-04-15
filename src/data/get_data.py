# -*- coding: utf-8-sig -*-

with open('pw.txt', 'r') as f:
    pw = f.read()
CLIENT_ID = 'w66eheluJKCHiSWF8oZmfw'
CLIENT_KEY = 'OlKg7Wd019ARZe50pgzqDPEdvG5OnA'
    
reddit = praw.Reddit(
         client_id = CLIENT_ID,
         client_secret = CLIENT_KEY,
         password = pw,
         user_agent = "thesis/0.0.1",
         username = "niyangbai",
         check_for_async = False
)
api = PushshiftAPI(reddit)

start_epoch=int(dt.datetime(2022, 4, 1).timestamp()) 
end_epoch=int(dt.datetime(2022, 4, 2).timestamp()) 

submissions_generator = api.search_submissions(after = start_epoch,before = end_epoch , subreddit='wallstreetbets',limit = 30) 
submissions = list(submissions_generator)

submissions_dict = {
            "id" : [],
            "url" : [],
            "title" : [],
            "score" : [],
            "num_comments": [],
            "created_utc" : [],
            "selftext" : [],
            "top_comments":[]
            }

spam_user = ['VisualMod', 'AutoModerator']

for submission_id in submissions:
    submission_praw = reddit.submission(id = submission_id)
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

df.to_csv('api.csv', index = False, encoding = 'utf-8-sig')








