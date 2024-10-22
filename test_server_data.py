import json
import sys
import threading
import time
from websockets import __main__ as ws
from websockets.sync.client import connect

def make_msg(message):
    return f"MSG {'{'}\"character\":\"{'test character'}\",\"message\":\"{message}\",\"channel\":\"ADH-c5de3ec454aaac984526\"'{'}'}'"


def main() -> None:
    # Parse command line arguments.
    uri = sys.argv[1]
    file = sys.argv[2]

    if uri is None or file is None:
        raise IndexError("the following arguments are required: <uri> <file>")

    # Untested
    # If we're on Windows, enable VT100 terminal support.
    if sys.platform == "win32":
        try:
            win_enable_vt100()
        except RuntimeError as exc:
            sys.stderr.write(
                f"Unable to set terminal to VT100 mode. This is only "
                f"supported since Win10 anniversary update. Expect "
                f"weird symbols on the terminal.\nError: {exc}\n"
            )
            sys.stderr.flush()

    file_messages = json.load(open(file, 'r'))['_webSocketMessages']
    print("Read File")
    time_mult = 5

    try:
        websocket = connect(uri)
    except Exception as exc:
        print(f"Failed to connect to {uri}: {exc}.")
        sys.exit(1)
    else:
        print(f"Connected to {uri}.")

    stop = threading.Event()

    # Start the thread that reads messages from the connection.
    thread = threading.Thread(target=ws.print_incoming_messages, args=(websocket, stop))
    thread.start()

    # Read from stdin in the main thread in order to receive signals.
    prev_time = file_messages[0]['time']
    try:
        print("Beginning to send messages")
        for message in file_messages:
            if message['type'] == "receive":
                ws.print_over_input(message[:25])
                websocket.send(message['data'])
            diff_time = max(5, (message['time'] - prev_time) * time_mult)
            time.sleep(diff_time)
            prev_time = message['time']

        input("End of file, press enter to continue")
        message = input("> ")
        websocket.send(make_msg(message))
    except (KeyboardInterrupt, EOFError):
        stop.set()
        websocket.close()
        ws.print_over_input("Connection closed.")

    thread.join()

if __name__ == '__main__':
    main()