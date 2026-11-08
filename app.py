from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

provider = TracerProvider(resource=Resource.create({"service.name": "a8-demo"}))
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("a8.demo")

with tracer.start_as_current_span("checkout") as parent:          # parent span
    parent.set_attribute("order.id", "A8-001")
    with tracer.start_as_current_span("charge-card") as child:    # child span
        child.set_attribute("payment.amount", 120)
        print("paid")