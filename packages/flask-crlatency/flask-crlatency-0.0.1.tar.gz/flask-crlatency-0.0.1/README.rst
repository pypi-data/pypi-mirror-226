flask-crlatency (flask-check-route-latency)
===========================================

A flask extension to log route latency

Example
-------

.. code:: py 

    app = Flask(__name__) 
    app.config["SECRET_KEY"] ="your_secret_key" 
    app.config["DEBUG"] = True
    
    latency_logger = RouteLatencyLogger(app)
    
    @app.route("/") 
    def index(): return "Hello, World!"

    if __name__ == "__main__": 
        app.run()

    response:
    
    [2023-08-10 21:52:54,341] INFO in **init**: Latency for route index:
    0.000188 seconds 127.0.0.1 - - [10/Aug/2023 21:52:54] “GET / HTTP/1.1”
    200 -
