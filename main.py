import threading

from webview.webview import Webview, Size, SizeHint
from server import run_server

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    window_size = Size(800, 600, SizeHint.NONE)
    webview = Webview(size=window_size)
    webview.navigate("http://localhost:60002")
    webview.run()
     