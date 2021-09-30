from y3oj import app, config

if __name__ == '__main__':
    app.debug = True
    app.run(host=config.host, port=config.port)