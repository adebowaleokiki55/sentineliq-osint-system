from fastapi import FastAPI

from backend.engine import ClaimEngine
from backend.search import SearchEngine
from backend.report_generator import generate_intel_report

app = FastAPI()

engine = ClaimEngine()
search = SearchEngine()


@app.get("/verify")
def verify(claim: str):

    # 1. get articles
    docs = search.search(claim)

    # 2. run scoring engine
    result = engine.run(claim, docs)

    # 3. generate intelligence report
    report = generate_intel_report(claim, result)

    return report