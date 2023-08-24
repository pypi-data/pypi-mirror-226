import os
from typing import Optional

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
import importlib.util

from opentelemetry.trace import get_tracer_provider, ProxyTracerProvider

from traceloop.semconv import SpanAttributes
from traceloop.tracing.no_log_span_batch_processor import NoLogSpanBatchProcessor

TRACER_NAME = "traceloop.tracer"
TRACELOOP_API_ENDPOINT = "https://api.traceloop.dev/v1/traces"
EXCLUDED_URLS = "api.openai.com,openai.azure.com"


def span_processor_on_start(span, parent_context):
    if Tracer.get_correlation_id() is not None:
        span.set_attribute(SpanAttributes.TRACELOOP_CORRELATION_ID, Tracer.get_correlation_id())

    if Tracer.get_workflow_name() is not None:
        span.set_attribute(SpanAttributes.TRACELOOP_WORKFLOW_NAME, Tracer.get_workflow_name())


class Tracer:
    __instance = None
    __correlation_id = None
    __workflow_name = None
    __processor = None
    __provider = None

    @staticmethod
    def init(app_name: Optional[str] = None):
        api_key = os.getenv("TRACELOOP_API_KEY")
        api_endpoint = os.getenv("TRACELOOP_API_ENDPOINT") or TRACELOOP_API_ENDPOINT
        print(f"Initializing Traceloop Tracer... API endpoint: {api_endpoint}")

        if app_name is not None:
            os.environ["OTEL_SERVICE_NAME"] = app_name

        exporter = OTLPSpanExporter(
            endpoint=api_endpoint,
            headers={
                "Authorization": f"Bearer {api_key}",
            }
        )

        default_provider = get_tracer_provider()
        if isinstance(default_provider, ProxyTracerProvider):
            Tracer.__provider = TracerProvider()
            trace.set_tracer_provider(Tracer.__provider)
        elif not hasattr(default_provider, "add_span_processor"):
            print("Cannot add span processor to the default provider since it doesn't support it")
            return
        else:
            Tracer.__provider = default_provider

        Tracer.__processor = NoLogSpanBatchProcessor(exporter)
        Tracer.__processor.on_start = span_processor_on_start
        Tracer.__provider.add_span_processor(Tracer.__processor)
        Tracer.__instance = trace.get_tracer(TRACER_NAME)

        if importlib.util.find_spec("openai") is not None:
            from traceloop.instrumentation.openai import OpenAIInstrumentor

            instrumentor = OpenAIInstrumentor()
            if not instrumentor.is_instrumented_by_opentelemetry:
                instrumentor.instrument()

        if importlib.util.find_spec("requests") is not None:
            from opentelemetry.instrumentation.requests import RequestsInstrumentor

            instrumentor = RequestsInstrumentor()
            if not instrumentor.is_instrumented_by_opentelemetry:
                instrumentor.instrument(excluded_urls=EXCLUDED_URLS)

        if importlib.util.find_spec("urllib3") is not None:
            from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor

            instrumentor = URLLib3Instrumentor()
            if not instrumentor.is_instrumented_by_opentelemetry:
                instrumentor.instrument(excluded_urls=EXCLUDED_URLS)

        if importlib.util.find_spec("pymysql") is not None:
            from opentelemetry.instrumentation.pymysql import PyMySQLInstrumentor

            instrumentor = PyMySQLInstrumentor()
            if not instrumentor.is_instrumented_by_opentelemetry:
                instrumentor.instrument()

    @staticmethod
    def instance():
        if Tracer.__instance is None:
            raise Exception("Tracer is not initialized")
        return Tracer.__instance

    @staticmethod
    def set_correlation_id(correlation_id: str):
        Tracer.__correlation_id = correlation_id

    @staticmethod
    def get_correlation_id():
        return Tracer.__correlation_id

    @staticmethod
    def set_workflow_name(workflow_name: str):
        Tracer.__workflow_name = workflow_name

    @staticmethod
    def get_workflow_name():
        return Tracer.__workflow_name

    @staticmethod
    def flush():
        if Tracer.__processor is not None:
            Tracer.__processor.force_flush()
