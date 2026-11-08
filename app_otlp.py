from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider(resource=Resource.create({"service.name": "a8-demo"}))
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("a8.demo")

with tracer.start_as_current_span("checkout") as parent:
    parent.set_attribute("order.id", "A8-002")
    with tracer.start_as_current_span("charge-card") as child:
        child.set_attribute("payment.amount", 120)
        print("paid (sent to collector)")

provider.shutdown()   # flush the batch before the program exits