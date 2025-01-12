
#📨 Reliable Message Transmission with Sliding Window Protocol
##🚀 A Python-based client-server system implementing reliable message transmission using a sliding window protocol.
This project showcases the basics of TCP-like communication, error handling, and retransmission mechanisms.

###📋 Features
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

🛠️ How It Works
Start the Server:
The server listens for connections and handles segmented message reception and reassembly.

Run the Client:
The client sends messages in small segments, waits for acknowledgments, and retransmits if necessary.

Protocol Details:

Header Structure: Each segment includes a custom header with sequence numbers, flags, and more.
Sliding Window: Efficiently manages multiple in-flight segments while waiting for acknowledgments.
🎯 Getting Started
Prerequisites
Python 3.6 or higher
Basic understanding of TCP and sliding window protocols (helpful but not required)
🧑‍💻 Usage
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/reliable-message-transmission.git
cd reliable-message-transmission
Start the server:

bash
Copy code
python server.py
Select manual or file-based configuration for the maximum message size.

Start the client:

bash
Copy code
python client.py
Choose to input parameters manually or load them from a configuration file.

Watch the magic happen! ✨

📦 File Structure
bash
Copy code
📁 reliable-message-transmission
├── client.py   # The client script implementing the sliding window protocol
├── server.py   # The server script handling message reception and acknowledgments
└── config.txt  # Example configuration file (optional)
📝 Example Configuration File (config.txt)
txt
Copy code
message: "Hello, this is a test message!"
window_size: 5
timeout: 3
maximum_msg_size: 100
🔍 Logs Example
Server:

vbnet
Copy code
Server listening on port 65432 with maximum message size: 100
Connection established with ('127.0.0.1', 54321)
Received segment: 0, Payload: "Hello,", Flags: 0
Sent ACK for sequence 0
Client:

css
Copy code
Connecting to the server...
Connected to the server.
Maximum words per message received from server: 100
Sending segment 0: "Hello,", Flags: 0
Received ACK: 0
🛡️ Error Handling
Timeouts: Retransmits unacknowledged segments after a configurable timeout.
Invalid Inputs: Alerts users to incorrect configurations or message formatting issues.
Connection Errors: Handles server disconnections gracefully.
