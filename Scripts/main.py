from piazza_api import Piazza

p = Piazza()
p.user_login()
user_profile = p.get_user_profile()
eece210 = p.network("hl5qm84dl4t3x2")
eece210.get_post(10)
posts = eece210.iter_all_posts(limit=10)
print (posts)
for post in posts:
    print (post)

all_users = eece210.get_all_users()
print (all_users[0])

#
# piazza = Piazza()
# piazza.user_login('vtatan3@gatech.edu', 'Visa123456!')
# course = piazza.network('ipgo72nw7yu1jv')
#
# # rpc api to post notes
# piazza_rpc = PiazzaRPC('j0a1bog7vzu2cj')
# piazza_rpc.user_login(config.creds['email'], config.creds['password'])