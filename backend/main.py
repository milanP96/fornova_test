from fastapi import FastAPI

from search_engine import SearchEngine
from pydantic import BaseModel, Field


class SearchModel(BaseModel):
    text: str = Field(None, min_length=3)


app = FastAPI()


@app.get("/all")
async def get_all(per_page: int = 10, page: int = 1):
    se = SearchEngine(source_path='test_data.csv')
    res, has_more = se.get_all(page=page, per_page=per_page)
    return {"res": res, "has_more": has_more}


@app.post("/search")
async def search_hotels(search: SearchModel, per_page: int = 10, page: int = 1):
    se = SearchEngine(source_path='test_data.csv')
    res, has_more = se.search(text=search.text, page=page, per_page=per_page)
    return {"res": res, "has_more": has_more}
