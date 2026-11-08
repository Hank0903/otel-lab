import logging, time
from flask import Flask
from opentelemetry import trace

app = Flask(__name__)
tracer = trace.get_tracer("a8.web")
log = logging.getLogger("a8.web")

@app.route("/")
def index():
    return "hello from a8-flask"

@app.route("/checkout")
def checkout():
    with tracer.start_as_current_span("charge-card") as span:   # manual child span
        span.set_attribute("payment.amount", 120)
        time.sleep(0.2)                                          # simulate payment latency
    log.warning("checkout finished, amount=120")
    return "paid"

@app.route("/error")
def error():
    log.error("about to fail on purpose")
    raise RuntimeError("deliberate failure for A8")