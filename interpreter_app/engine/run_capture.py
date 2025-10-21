# run_capture.py
import io
import contextlib
from .interpreter import evaluate_source, EvalVisitor

def run_source_capture(source: str):
    visitor = EvalVisitor()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        evaluate_source(source, visitor)
    return buf.getvalue()
