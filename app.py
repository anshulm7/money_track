from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.templating import Jinja2Templates

import pandas as pd

from src.c_a import clean_data, top_3, cc, month_t, date_range, search

templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/")
def home(
    request: Request
    ):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/upload")
async def upload_file(
    request : Request,
    file: UploadFile = File(),
    analysis : str = Form(),
    merchant : str = Form(default=""),
    start_date : str = Form(default=""),
    end_date : str = Form(default=""),
    action: str = Form()
):
    data = pd.read_csv(file.file)
    data = clean_data(data)
    if merchant:
            data = search(data, merchant)
    if start_date and end_date:
            data = date_range(data, start_date, end_date)

    if (action == "show"):
        table = data.to_html(index=False)
        return templates.TemplateResponse(request=request, name="index.html", context={"filtered":table})
    
    elif (action == "analyze"):

        if analysis == "top3":
            result = top_3(data)

        elif analysis == "monthly":
            result = month_t(data)

        elif analysis == "category":
            result = cc(data)
        
        table = result.to_html(index=False)

        return templates.TemplateResponse(request=request, name="result.html", context={"table":table, "name":analysis})