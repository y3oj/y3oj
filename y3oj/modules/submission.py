from y3oj import db, judger
from y3oj.models import Submission, User, Problem


def get_submission(id):
    return db.session.query(Submission).filter_by(id=id).first()


def judge_submission(submission: Submission):
    if submission is None:
        return
    judger.submit(submission)


def rejudge_submission(id: str):
    judge_submission(get_submission(id))


def submit_code(user: User, problem: Problem, code: str):
    code = code.replace('\r\n', '\n').replace('\r', '\n')
    submission = Submission(user=int(user.key),
                            problem=str(problem.id),
                            code=code)
    # print('[submit-code]', user, problem, submission)
    db.session.add(submission)
    db.session.commit()
    judge_submission(submission)