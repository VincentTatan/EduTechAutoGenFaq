from dateutil import parser


class Post:
    def __init__(self, json):
        try:
            self.folders = ' '.join(json['folders']).decode('utf-8')
            self.body = json['history'][0]['content']
            self.subject = json['history'][0]['subject']
            self.id = json['nr']
            self.guid = json['id']
            self.views = json['unique_views']
            self.is_private = True if json['status'] == 'private' else False
            self.date = parser.parse(json['created'])

            # note: json['type'] takes values 'note', 'question', 'poll'
            self.is_question = True if json['type'] == 'question' else False
            self.follow_ups = len(json['children'])  # number of follow up questions posted

            self.good_question_tally = len(json['tag_good'])  # total number of good question upvotes for the post
            self.good_question_ta_tally = sum(1 for x in json['tag_good'] if x['admin'] == True)

            self.has_i_answer = False
            self.has_s_answer = False
            self.has_answer = False  # assume answer present for notes/polls

            self.good_student_answer_tally = 0  # total good answer upvotes on student answer
            self.good_student_answer_ta_tally = 0  # total good answer upvotes on student answer by a TA

            self.good_instructor_answer_tally = 0  # total good answer upvotes on TA answer
            self.good_instructor_answer_ta_tally = 0  # total good answer upvotes on TA answer by other TAs

            self.i_answer = ''
            self.s_answer = ''
            # count the above tallies
            # note there will be only one i_answer and/or one s_answer per post
            for child in json['children']:
                if child['type'] == 'i_answer':
                    self.has_i_answer = True
                    self.i_answer = child['history'][0]['content']
                    self.good_instructor_answer_tally = len(child['tag_endorse'])
                    self.good_instructor_answer_ta_tally = sum(1 for x in child['tag_endorse'] if x['admin'] == True)

                if child['type'] == 's_answer':
                    self.has_s_answer = True
                    self.s_answer = child['history'][0]['content']
                    self.good_student_answer_tally = len(child['tag_endorse'])
                    self.good_student_answer_ta_tally = sum(1 for x in child['tag_endorse'] if x['admin'] == True)

            self.has_answer = self.has_i_answer or self.has_s_answer
            self.json = json  # in case something else is required
        except:
            print('could not convert post id {0} to object'.format(self.id))

# bookmarked          : 2
# bucket_name         : 'today'
# created             : creation date of the post
# default_anonymity:  : public/private post
# folders             : labels for the post
# history             : history[0] gives the latest post
# id                  : unique identifier for the post
# is_tag_good         : tells if 'good note' for the post by instructor
# my_favorite         : did the bot mark this post as a favorite for some reason
# no_answer           : 0
# nr                  : post id (number)
# num_favorites       : how many students marked this post as their favorites
# tag_good            : list of dicts, each dict is an instructor and info
# unique_views        : number of unique views in the post
# upvote_ids          : ids of all the students who upvoted(?)