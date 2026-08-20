import sys
import traceback

try:
    from fastapi import FastAPI
    from backend.engine import ClaimEngine
    from backend.search import SearchEngine
    from backend.report_generator import generate_intel_report

    app = FastAPI()
    engine = ClaimEngine()
    search = SearchEngine()

    @app.get("/verify")
    def verify(claim: str):
        docs = search.search(claim)
        result = engine.run(claim, docs)
        report = generate_intel_report(claim, result)
        return report

except Exception as e:
    # If the app crashes on startup, create an emergency app to show you the error
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse
    
    app = FastAPI()
    error_trace = traceback.format_exc()
    
    @app.get("/{catchall:path}")
    def crash_report(catchall: str = ""):
        return PlainTextResponse(f"CRITICAL STARTUP ERROR:\n\n{error_trace}", status_code=500)
