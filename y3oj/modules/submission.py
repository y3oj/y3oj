from y3oj import db, judger
from y3oj.models import Submission, UserMixin, Problem


def get_submission(id):
    res = db.session.query(Submission).filter_by(id=id).all()
    return res[0] if len(res) else None


def judge_submission(submission: Submission):
    if submission is None:
        return
    judger.submit(submission)


def rejudge_submission(id):
    judge_submission(get_submission(id))


def submit_code(user: UserMixin, problem: Problem, code):
    code = code.replace('\r\n', '\n').replace('\r', '\n')
    submission = Submission(user=int(user.key),
                            problem=str(problem.id),
                            code=code)
    print('[submit-code]', user, problem, submission)
    db.session.add(submission)
    db.session.commit()
    judge_submission(submission)