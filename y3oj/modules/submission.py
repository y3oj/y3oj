from y3oj import db
from y3oj.models import Submission


def get_submission(id):
    res = db.session.query(Submission).filter_by(id=id).all()
    return res[0] if len(res) else None


def submit_code(user, problem, code):
    code = code.replace('\r\n', '\n').replace('\r', '\n')
    submission = Submission(user=str(user.key),
                            problem=str(problem.id),
                            code=code)
    print('[submit-code]', user, problem, submission)
    db.session.add(submission)
    db.session.commit()
