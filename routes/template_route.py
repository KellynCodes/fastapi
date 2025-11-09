


from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


class TemplateController:
    BASE_DIR: Path  = Path(__file__).resolve().parent.parent
    templates: Jinja2Templates = Jinja2Templates(directory=BASE_DIR / 'templates')   
    router: APIRouter = APIRouter()
    
    def __init__(self):
        self.router.get("/login", response_class=HTMLResponse)(self.render_login_template)
        self.router.post("/submit", response_class=HTMLResponse)(self.submit_form)
    
    async def render_login_template(self, request: Request):
        print(self.BASE_DIR)
        return self.templates.TemplateResponse("login.html", {"request": request, "username": "Kelly", "message": "Hello, World!"})
    
    
    async def submit_form(self, request: Request):
        form_data = await request.form()
        username = form_data.get("username")
        password = form_data.get("password")
        return self.templates.TemplateResponse("login.html", {"request": request, "message": f"Submitted username: {username}, password: {password}"})