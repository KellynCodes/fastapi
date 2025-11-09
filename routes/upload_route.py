import os
import shutil
from fastapi import APIRouter, FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from exceptions.exception_handler import NotFoundException


class FileUploadController:
    templates = Jinja2Templates(directory="templates")
    UPLOAD_DIR: str = "static/uploads"
    router: APIRouter = APIRouter()
    
    def __init__(self, app: FastAPI):
        app.mount("/static", StaticFiles(directory="static"), name="static")
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        self.router.get("/", response_class=HTMLResponse)(self.form_page)
        self.router.post("/upload", response_class=HTMLResponse)(self.upload_file)

    def form_page(self, request: Request):
        return self.templates.TemplateResponse("upload.html", {"request": request})

    async def upload_file(self, request: Request):
        form = await request.form()
        file: UploadFile = form.get("file")
        if not file:
            raise NotFoundException("No file uploaded")
        
        file_location = os.path.join(self.UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        file_info: dict[str, str] = {
            'file_name': file.filename,
            'file_size': file.size,
            'content_type': file.content_type,
            'image_url': f"/static/uploads/{file.filename}"
        }
        return self.templates.TemplateResponse("result_image.html", {'request': request, "file_info": file_info})