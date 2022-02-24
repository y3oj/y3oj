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
        statistic = [[None for _ in range(len(self))] for _ in range(len(self.usergroup))]
        for submission in submissions:
            if submission.user not in self.usergroup.key_list or submission.problem not in self.id_list:
                continue
            user_index = self.usergroup.key_list.index(submission.user)
            problem_index = self.id_list.index(submission.problem)
            if statistic[user_index][problem_index] and submission.status != 'Accepted':
                continue
            statistic[user_index][problem_index] = submission.get_mixin()
        return statistic

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
        return '<Homework [%s] [%s]>' % (
            ', '.join(self.usergroup.id_list),
            ', '.join(self.id_list),
        )
