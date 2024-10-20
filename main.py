import socket
import threading
import wave
import pyaudio

# Set up server socket to act as a mediator
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000))  # Listen on all interfaces, port 5000
server_socket.listen(2)  # Listen for two clients (Client A and Client B)
print("Waiting for two clients to connect...")

clients = []  # To store the two connected clients

def play_notify_sound(file_name):
    """Play a notification sound when a client connects or disconnects."""
    wf = wave.open(file_name, 'rb')

    # Open a pyaudio stream
    notify_stream = pyaudio.PyAudio().open(format=pyaudio.PyAudio().get_format_from_width(wf.getsampwidth()),
                                           channels=wf.getnchannels(),
                                           rate=wf.getframerate(),
                                           output=True)

    # Read and play sound file
    data = wf.readframes(1024)
    while data:
        notify_stream.write(data)
        data = wf.readframes(1024)

    # Close the stream
    notify_stream.stop_stream()
    notify_stream.close()

def forward_audio(src_conn, dst_conn):
    """Forward audio data from one client to the other."""
    try:
        while True:
            data = src_conn.recv(1024)
            if not data:
                print("Client disconnected")
                play_notify_sound('disconnect.wav')  # Play sound on client disconnect
                break
            dst_conn.sendall(data)  # Forward data to the other client
    except Exception as e:
        print(f"Error forwarding audio: {e}")
    finally:
        src_conn.close()
        dst_conn.close()

def handle_clients():
    """Handle both clients and forward data between them."""
    if len(clients) == 2:
        print("Both clients connected, starting communication...")
        play_notify_sound('notify.wav')  # Play sound when both clients are connected

        # Create threads to forward audio between Client A and Client B
        threading.Thread(target=forward_audio, args=(clients[0], clients[1])).start()  # Client A -> Client B
        threading.Thread(target=forward_audio, args=(clients[1], clients[0])).start()  # Client B -> Client A

        # Remove disconnected clients
        clients.clear()

# Main loop to accept new client connections even after disconnection
while True:
    try:
        conn, addr = server_socket.accept()
        print(f"Client connected from {addr}")
        clients.append(conn)

        if len(clients) == 2:
            handle_clients()  # Start forwarding audio between clients once both are connected

    except Exception as e:
        print(f"Server error: {e}")

# The server will continue running and wait for new connections even after clients disconnect
