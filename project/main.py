from app import create_app
from app import scheduler

app = create_app()

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(host="0.0.0.0", port=5000, debug=True)
