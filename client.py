import socket
import struct
import time

HOST = "127.0.0.1"
PORT = 65432

def split_message_with_padding(message, max_bytes):
    message_bytes = message.encode('utf-8')
    segments = []
    start = 0
    while start < len(message_bytes):
        end = start + max_bytes
        while end < len(message_bytes) and (message_bytes[end] & 0b11000000) == 0b10000000:
            end -= 1
        segment = message_bytes[start:end]
        if len(segment) < max_bytes:
            segment += b' ' * (max_bytes - len(segment))
        segments.append(segment)
        start = end
    return segments

def sliding_window_protocol(client_socket, message, max_bytes, window_size, timeout):
    segments = split_message_with_padding(message, max_bytes)
    total_segments = len(segments)
    window_start = 0
    acked_segments = set()
    sent_segments = set()  
    segment_timestamps = {}  

    while window_start < total_segments:
        for i in range(window_start, window_start + window_size):
            if i < total_segments and i not in sent_segments:
                payload = segments[i]
                flags = 0

                if i == total_segments - 1:
                    flags = 1  # Set flag to 1 for the last segment

                print(f"Sending segment {i}: {payload}, Flag: {flags}")

                tcp_header = struct.pack(
                    '!HHLLBBHHH',
                    12345,             # Source Port
                    65432,             # Destination Port
                    i,                 # Sequence Number
                    i+1,               # Acknowledgment Number
                    (5 << 4) | flags,  # Data Offset and Flags
                    0,                 # Reserved
                    window_size * (max_bytes + 20),  # Window Size
                    0,                 # Checksum
                    0                  # Urgent Pointer
                )

                message_with_header = tcp_header + payload
                client_socket.sendall(message_with_header)
                sent_segments.add(i)
                segment_timestamps[i] = time.time()  # Save the send time

        # Wait for ACKs
        try:
            while True:
                data = b''
                while len(data) < 4:
                    chunk = client_socket.recv(4 - len(data))
                    if not chunk:
                        raise ConnectionError("Connection closed before receiving all data")
                    data += chunk

                ack = struct.unpack('!I', data)[0]
                print(f"Received ACK: {ack}")

                # Ignore old ACKs
                if ack < window_start:
                    print(f"Ignoring outdated ACK: {ack}")
                    continue

                if ack in range(window_start, window_start + window_size):
                    acked_segments.add(ack)

                    # Slide the window forward
                    if ack == window_start:
                        while window_start in acked_segments:
                            window_start += 1
                            print(f"Window start moved to {window_start}")

                            # Stop moving the window if we've reached the last segment
                            if window_start >= total_segments:
                                print("Reached the last segment. Stopping window update.")
                                break

                break
        except socket.timeout:
            # Check for timeouts for unacknowledged segments
            current_time = time.time()
            for i in range(window_start, min(window_start + window_size, total_segments)):
                if i not in acked_segments and current_time - segment_timestamps[i] >= timeout:
                    payload = segments[i]
                    tcp_header = struct.pack(
                        '!HHLLBBHHH',
                        12345, 65432, i, 0, 5 << 4, 0, window_size * (max_bytes + 20), 0, 0
                    )
                    message_with_header = tcp_header + payload
                    print(f"Resending segment {i}: {payload} after timeout")
                    client_socket.sendall(message_with_header)
                    segment_timestamps[i] = current_time  # Update send time

def get_parameters_from_file(file_path):
    parameters = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("message:"):
                parameters["message"] = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("window_size:"):
                parameters["window_size"] = int(line.split(":", 1)[1].strip())
            elif line.startswith("timeout:"):
                parameters["timeout"] = int(line.split(":", 1)[1].strip())
    return parameters  
def get_parameters_from_user():
    message = input("Enter the message to send: ").strip()
    window_size = int(input("Enter the window size: ").strip())
    timeout = int(input("Enter the timeout (in seconds): ").strip())
    return {"message": message, "window_size": window_size, "timeout": timeout}
                  

def client():
    source = input("Do you want to get parameters from a file or input manually? (file/manual): ").strip().lower()

    if source == "file":
        file_path = input("Enter the path to the configuration file: ").strip()
        parameters = get_parameters_from_file(file_path)
    elif source == "manual":
        parameters = get_parameters_from_user()
    else:
        print("Invalid choice. Exiting.")
        return

    message = parameters['message']
    window_size = parameters['window_size']
    timeout = parameters['timeout']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        print("Connecting to the server...")
        client_socket.connect((HOST, PORT))
        print("Connected to the server.")

        data = b''
        while len(data) < 4:
            chunk = client_socket.recv(4 - len(data))
            if not chunk:
                raise ConnectionError("Connection closed before receiving all data")
            data += chunk

        max_words_per_message = struct.unpack('!I', data)[0]
        print(f"Maximum words per message received from server: {max_words_per_message}")

        sliding_window_protocol(client_socket, message, max_words_per_message, window_size, timeout)

if __name__ == "__main__":
    client()