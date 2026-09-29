import eventlet
eventlet.monkey_patch()

# Buradan sonra senin mevcut kodların devam edecek:
# from flask import Flask...
# from flask_socketio import SocketIO...
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli_anahtar_buraya'

# cors_allowed_origins="*" ile mobil cihazlardan gelen tüm bağlantılara izin veriyoruz.
# logger=True ve engineio_logger=True bağlantı detaylarını terminale basar.
socketio = SocketIO(
    app, 
    cors_allowed_origins="*", 
    logger=True, 
    engineio_logger=True,
    always_connect=True
)

@socketio.on('connect')
def handle_connect():
    print(f"Yeni bağlantı kabul edildi: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Bağlantı koptu: {request.sid}")

# --- Oda Oluşturma & Katılma Örnek Fonksiyonları ---

@socketio.on('create_room')
def handle_create_room(data):
    room = data.get('room')
    if room:
        join_room(room)
        print(f"Oda oluşturuldu ve katılma sağlandı: {room} (Oyuncu: {request.sid})")
        emit('room_created', {'status': 'success', 'room': room}, room=request.sid)

@socketio.on('join_room')
def handle_join_room(data):
    room = data.get('room')
    if room:
        join_room(room)
        print(f"Odaya katılındı: {room} (Oyuncu: {request.sid})")
        emit('user_joined', {'sid': request.sid}, room=room)

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data.get('room')
    if room:
        leave_room(room)
        print(f"Odadan ayrılındı: {room} (Oyuncu: {request.sid})")

if __name__ == '__main__':
    print("Sunucu başlatılıyor... (Tüm ağ arayüzleri dinleniyor: port 5000)")
    # host='0.0.0.0' mobil cihazların IP adresin üzerinden bağlanabilmesi için şarttır.
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
