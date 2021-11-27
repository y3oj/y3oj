from y3oj import db
from y3oj.models import UserGroup, Submission
from y3oj.modules.problem import get_problem


class HomeworkInitializeException(Exception):
    pass


class Homework(object):
    def get_statistics(self):
        submissions = db.session.query(Submission).all()
        statistic = [[None for _ in range(len(self))]
                     for _ in range(len(self.usergroup))]
        for submission in submissions:
            if submission.user not in self.usergroup.key_list or \
                    submission.problem not in self.id_list:
                continue
            user_index = self.usergroup.key_list.index(submission.user)
            problem_index = self.id_list.index(submission.problem)
            if statistic[user_index][problem_index] and \
                    submission.status != 'Accepted':
                continue
            statistic[user_index][problem_index] = submission.get_mixin()
        return statistic

    def __init__(self, usergroup: UserGroup, problem_list):
        self.usergroup = usergroup
        self.id_list = []
        self.problem_list = []
        for problem_id in problem_list:
            problem = get_problem(problem_id)
            if problem is None:
                raise HomeworkInitializeException(f'题目 {problem_id} 不存在')
            self.id_list.append(problem.id)
            self.problem_list.append(problem)

    def __len__(self):
        return len(self.problem_list)

    def __repr__(self):
        return '<Homework [%s] [%s]>' % (
            ', '.join(self.usergroup.id_list),
            ', '.join(self.id_list),
        )
