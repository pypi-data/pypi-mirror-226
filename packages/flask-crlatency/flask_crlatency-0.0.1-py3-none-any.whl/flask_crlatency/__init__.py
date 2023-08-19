import logging
import time

from flask import request


class RouteLatencyLogger:
    def __init__(self, app=None):
        self.app = app
        self.max_route_latency = None
        if app is not None:
            self.init_app(self.app)

    def init_app(self, app):
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        self.max_route_latency = app.config.get('MAX_ROUTE_LATENCY', None)

    def before_request(self):
        request._start_time = time.time()

    def after_request(self, response):
        if hasattr(request, '_start_time'):
            latency = time.time() - request._start_time
            route = request.endpoint
            print(self.max_route_latency,latency)
            if self.max_route_latency is not None and latency > self.max_route_latency:
                logging.warning(f'High latency for route {route}: {latency:.6f} seconds')
            else:
                logging.info(f'Latency for route {route}: {latency:.6f} seconds')

        return response