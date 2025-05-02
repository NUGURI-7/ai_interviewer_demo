from RealProject import create_app
from app.ws import socketio, register_socketio_events

app = create_app()
register_socketio_events(app)  #  注册事件在这里完成，避免循环

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
