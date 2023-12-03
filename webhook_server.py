import threading

from flask import Flask, request

class WebhookServer:
    def __init__(self, name, port, post_handler, debug=False):
        self.name = name
        self.port = port
        self.post_handler = post_handler
        self.debug = debug

    def start(self):
        self.webhook_server = Flask(self.name)

        self.webhook_server.route("/", methods=["POST"])(
            self.post_handler
        )

        def start_server():
            print(f"Starting {self.name} on port {self.port}")
            self.webhook_server.run(port=self.port, debug=self.debug)

        self._webhook_thread = threading.Thread(target=start_server)
        self._webhook_thread.start()

    def teardown(self):
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        shutdown_func()

        self._webhook_thread.join()
