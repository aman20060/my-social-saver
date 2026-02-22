from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import db

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request, q: str = None): # Add q parameter
    links = db.get_all_links()
    
    grouped_data = {}
    for link in links:
        try:
            url, category, summary, title, date = link[1], link[2], link[3], link[4], link[5]
        except:
            url, category, summary, title, date = link[1], link[2], link[3], link[4], "Unknown"

        # --- SEARCH FILTERING LOGIC ---
        if q:
            search_term = q.lower()
            if search_term not in summary.lower() and \
               search_term not in category.lower() and \
               search_term not in title.lower():
                continue # Skip this link if it doesn't match
        
        if category not in grouped_data:
            grouped_data[category] = []
        
        grouped_data[category].append({
            "url": url, 
            "summary": summary, 
            "title": title, 
            "date": date
        })

    return templates.TemplateResponse("index.html", {"request": request, "grouped_data": grouped_data, "search_query": q})