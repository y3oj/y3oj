from y3oj import app, db, loader, config

if __name__ == '__main__':
    db.create_all()
    loader.all()

    app.debug = True
    app.run(host=config.host, port=config.port)
