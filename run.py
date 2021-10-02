from y3oj import app, db, config
from y3oj.modules import problem

if __name__ == '__main__':
    db.create_all()
    problem.loadFromLocal()
    app.debug = True
    app.run(host=config.host, port=config.port)
