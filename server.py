import socket

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(1)
    print("Сервер запущен. Ожидание игрока...")

    conn, addr = server.accept()
    print(f"Игрок подключен: {addr}")

    total_score = 0
    
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        
        if data.startswith("SCORE:"):
            points = int(data.split(":")[1])
            total_score += points
            print(f"Получены баллы: {points}. Всего: {total_score}")
            conn.send(f"Баллы приняты. Всего: {total_score}".encode('utf-8'))
        
        if data == "GET_TOTAL":
            conn.send(f"Итоговый результат: {total_score}/99".encode('utf-8'))

    conn.close()

if __name__ == "__main__":
    start_server()