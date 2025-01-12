
# 📨 Reliable Message Transmission with Sliding Window Protocol
## 🚀 A Python-based client-server system implementing reliable message transmission using a sliding window protocol.
This project showcases the basics of TCP-like communication, error handling, and retransmission mechanisms.

### 📋 Features
🖥️ Client-Server Communication
Reliable message exchange using a custom sliding window protocol over TCP.

📜 Configurable Parameters
Supports file-based or manual configuration for message size, window size, and timeout.

⚙️ Sliding Window Protocol

Segments messages with padding for safe transmission.
Handles retransmissions for unacknowledged segments.
Acknowledges received segments to ensure reliability.
🔄 Real-Time Logs
Provides detailed logging for every message segment, acknowledgment, and retransmission.

❌ Error Handling
Detects invalid configurations, timeouts, and connection issues with informative error messages.

## 🛠️ How It Works
Start the Server:
The server listens for connections and handles segmented message reception and reassembly.

Run the Client:
The client sends messages in small segments, waits for acknowledgments, and retransmits if necessary.

## Protocol Details:

Header Structure: Each segment includes a custom header with sequence numbers, flags, and more.
Sliding Window: Efficiently manages multiple in-flight segments while waiting for acknowledgments.
🎯 Getting Started
Prerequisites
Python 3.6 or higher
Basic understanding of TCP and sliding window protocols (helpful but not required)
🧑‍💻 Usage
Clone the repository:


Copy code
git clone https://github.com/your-username/reliable-message-transmission.git
cd reliable-message-transmission

### Start the server:

python server.py
Select manual or file-based configuration for the maximum message size.

### Start the client:

python client.py
Choose to input parameters manually or load them from a configuration file.

Watch the magic happen! ✨

### 📝 Example Configuration File (config.txt)

message: "Hello, this is a test message!"
window_size: 5
timeout: 3
maximum_msg_size: 100

### 🛡️ Error Handling
Timeouts: Retransmits unacknowledged segments after a configurable timeout.
Invalid Inputs: Alerts users to incorrect configurations or message formatting issues.
Connection Errors: Handles server disconnections gracefully.
