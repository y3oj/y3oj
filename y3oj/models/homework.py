import functools

from y3oj import db
from y3oj.models import User, Problem, UserGroup, Submission
from y3oj.modules.problem import get_problem


class HomeworkInitError(Exception):
    pass


class Homework(object):

    def includes(self, problem: Problem):
        return problem in self.problem_list

    def includes_user(self, user: User):
        return user in self.usergroup.user_list

    def get_statistics(self):
        submissions = db.session.query(Submission).all()
        statistics = [{'user': user, 'accepted': 0, 'score': 0, 'submission': [None] * len(self.problem_list)} for user in self.usergroup.user_list]
        for submission in submissions:
            if submission.user not in self.usergroup.key_list or submission.problem not in self.id_list:
                continue
            user_index = self.usergroup.key_list.index(submission.user)
            problem_index = self.id_list.index(submission.problem)
            if statistics[user_index]['submission'][problem_index] and submission.status != 'Accepted':
                continue
            statistics[user_index]['submission'][problem_index] = submission.get_mixin()

        for statistic in statistics:
            for submission in statistic['submission']:
                if submission is None:
                    continue
                statistic['score'] += submission.passed_count / len(submission.details)
                if submission.status == 'Accepted':
                    statistic['accepted'] += 1

        def cmp(a, b):
            return b['score'] - a['score'] or a['accepted'] - b['accepted'] or a['user'].key - b['user'].key

        statistics.sort(key=functools.cmp_to_key(cmp))
        for i in range(len(statistics)):
            if i and statistics[i]['score'] == statistics[i - 1]['score']:
                statistics[i]['rank'] = statistics[i - 1]['rank']
            else:
                statistics[i]['rank'] = i + 1

        return statistics

    def __init__(self, id: str, name: str, description: str, usergroup: UserGroup, problem_list: list):
        self.id = id
        self.name = name
        self.description = description
        self.usergroup = usergroup

        self.id_list = []
        self.problem_list = []
        for problem_id in problem_list:
            problem = get_problem(problem_id)
            if problem is None:
                raise HomeworkInitError(f'题目 {problem_id} 不存在')
            self.id_list.append(problem.id)
            self.problem_list.append(problem)

    def __len__(self):
        return len(self.problem_list)

    def __repr__(self):
        return '<Homework [%s] [%s]>' % (', '.join(self.usergroup.id_list), ', '.join(self.id_list))
