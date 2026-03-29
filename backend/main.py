from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
import uvicorn

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from parsers.adilet_parser import AdiletParser
from parsers.egov_parser import EGovParser

app = FastAPI(title="GovTech Legal Parsers API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

adilet_parser = AdiletParser()
egov_parser = EGovParser()

@app.get("/api/search")
async def search_documents(q: str = Query(..., description="Keyword for searching legal documents")):
    """
    Search legal databases (Adilet & eGov) for the given keyword.
    """
    try:
        # Perform searches in parallel or sequentially. For simplicity, sequential here.
        adilet_results = adilet_parser.search(q, limit=5)
        egov_results = egov_parser.search(q, limit=5)
        
        all_results = adilet_results + egov_results
        
        return {
            "query": q,
            "total_results": len(all_results),
            "results": all_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/extract", response_model=Dict[str, str])
async def extract_document_text(url: Optional[str] = None, dataset_id: Optional[str] = None):
    """
    Extract the full text representation from a specific document.
    Must provide either 'url' (for Adilet) or 'dataset_id' (for eGov).
    """
    if url:
        text = adilet_parser.get_document_text(url)
        source = "Adilet"
    elif dataset_id:
        text = egov_parser.get_document_text(dataset_id)
        source = "eGov Data"
    else:
        raise HTTPException(status_code=400, detail="Must provide 'url' or 'dataset_id'")
        
    if text is None:
        raise HTTPException(status_code=404, detail="Could not extract text from document")
        
    return {
        "source": source,
        "text": text
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
