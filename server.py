import socket
import threading
import struct

HOST = '127.0.0.1'
PORT = 65432

def get_server_parameters(file_path):
    parameters = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(':', 1)
            parameters[key.strip()] = value.strip().strip('"')
    return int(parameters['maximum_msg_size'])

def handle_client(conn, addr, max_msg_size):
    print(f"Connected by {addr}")
    received_segments = []  # רשימה לאחסון כל המקטעים שהתקבלו
    try:
        # שליחת גודל ההודעה המרבי ללקוח כנתון בינארי
        conn.sendall(struct.pack('!I', max_msg_size))  # שליחה של 4 בייטים
        print(f"Sent maximum message size ({max_msg_size}) to {addr} in binary format")

        while True:
            # קבלת TCP Header וגודל מקטע ההודעה
            header_and_payload_size = 20 + max_msg_size
            data = conn.recv(header_and_payload_size)
            if not data:
                break

            # פיצול הנתונים ל-TCP Header ו-Payload
            tcp_header = data[:20]
            payload = data[20:20 + max_msg_size]
            print(f"Raw payload: {payload}")

            # פרסינג של ה-TCP Header
            unpacked_header = struct.unpack('!HHLLBBHHH', tcp_header)
            sequence_number = unpacked_header[2]
            acknowledgment_number = unpacked_header[3]
            flags = unpacked_header[5] & 0b00000001  # בדיקת הביט שמייצג את הדגל

            print(f"Received TCP Header: Seq={sequence_number}, Ack={acknowledgment_number}, Flags={flags}")

            # שמירת המטען ברשימה
            received_segments.append(payload)

            # שליחת ACK ללקוח
            conn.sendall(struct.pack('!I', sequence_number))
            print(f"Sent ACK for sequence {sequence_number}")

            # אם הדגל מציין שזה הסגמנט האחרון, יציאה מהלולאה
            if flags == 1:
                print("Last segment received. Exiting loop.")
                break
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")
        # איחוד כל הסגמנטים ופרסום ההודעה המלאה
        full_message_bytes = b''.join(received_segments)
        try:
            full_message = full_message_bytes.decode('utf-8').strip()
            print(f"Full message received from {addr}: {full_message}")
        except UnicodeDecodeError as e:
            print(f"Error decoding full message: {e}")
            print(f"Raw full message bytes: {full_message_bytes}")

def server():
    source = input("Do you want to get the maximum message size from a file or input manually? (file/manual): ").strip().lower()

    if source == "file":
        file_path = input("Enter the path to the configuration file: ").strip()
        max_msg_size = get_server_parameters(file_path)
    elif source == "manual":
        max_msg_size = int(input("Enter the maximum message size: ").strip())
    else:
        print("Invalid choice. Exiting.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on port {PORT} with maximum message size: {max_msg_size}")
        while True:
            conn, addr = server_socket.accept()
            print(f"Connection established with {addr}")
            threading.Thread(target=handle_client, args=(conn, addr, max_msg_size)).start()

if __name__ == "__main__":
    server()

