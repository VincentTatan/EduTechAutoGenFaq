# from piazza_api import Piazza
#
# p = Piazza()
# p.user_login()
# user_profile = p.get_user_profile()
# eece210 = p.network("hl5qm84dl4t3x2")
# eece210.get_post(10)
# posts = eece210.iter_all_posts(limit=10)
# print (posts)
# for post in posts:
#     print (post)
#
# all_users = eece210.get_all_users()
# print (all_users[0])

#
# piazza = Piazza()
# piazza.user_login('vtatan3@gatech.edu', 'Visa123456!')
# course = piazza.network('ipgo72nw7yu1jv')
#
# # rpc api to post notes
# piazza_rpc = PiazzaRPC('j0a1bog7vzu2cj')
# piazza_rpc.user_login(config.creds['email'], config.creds['password'])



import praw
import config

reddit = praw.Reddit(client_id = config.client_id,
                     client_secret= config.client_secret,
                    username=config.username,
                    password=config.password,
                     user_agent=config.user_agent
                     )
subreddit=reddit.subreddit('OMSCS')
hot_python = subreddit.hot(limit=500)

for submission in hot_python:
    if not submission.stickied:
        print('Title: {}, ups: {}, downs: {}, Have we visited: {}'.format(submission.title,
                                                                          submission.ups,
                                                                          submission.downs,
                                                                          submission.visited)
                                                                          )
        comments = submission.comments
        for comment in comments:
            print(20*'-')
            print(comment.body)
            if len(comment.replies)>0:
                for reply in comment.replies:
                    print('REPLY: ',reply.body)