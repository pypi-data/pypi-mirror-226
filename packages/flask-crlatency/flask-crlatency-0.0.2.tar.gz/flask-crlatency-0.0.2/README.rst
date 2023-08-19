flask-crlatency (flask-check-route-latency)
===========================================

A flask extension to log route latency

Example
-------

.. code:: py 

    from flask import Flask 
    from flask_crlatency import RouteLatencyLogger

    app = Flask(__name__) 
    app.config["SECRET_KEY"] ="your_secret_key" 
    app.config["DEBUG"] = True
    app.config["MAX_ROUTE_LATENCY"] = 0.1
    
    latency_logger = RouteLatencyLogger(app)
    
    @app.route("/") 
    def index(): 
        return "Hello, World!"

    if __name__ == "__main__": 
        app.run()

    response:
    
    [2023-08-19 10:00:58,654] WARNING in __init__: High latency for route index: 3.001345 seconds
    127.0.0.1 - - [19/Aug/2023 10:00:58] "GET / HTTP/1.1" 200 -
