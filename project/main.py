from project.app import create_app
from project.app import scheduler

app = create_app()

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True)
