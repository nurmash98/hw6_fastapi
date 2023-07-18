import json
from fastapi import Cookie, FastAPI, Form, Request, Response, templating
from fastapi.responses import RedirectResponse

from .flowers_repository import Flower, FlowersRepository
from .purchases_repository import Purchase, PurchasesRepository
from .users_repository import User, UsersRepository
from jose import jwt

app = FastAPI()
templates = templating.Jinja2Templates("templates")


flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository()


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ваше решение сюда
@app.get("/signup")
def get_signup(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@app.post("/signup")
def post_signup(email: str = Form(), full_name: str = Form(), password: str = Form()):
    users_repository.save(email, full_name, password)
    return RedirectResponse("/login", status_code = 303)

@app.get("/login")
def get_login(request: Request):
    print (users_repository.getAll())
    return templates.TemplateResponse("auth/login.html", {"request": request})

def encode_jwt(user_id: int) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "Nurmash", "HS256")
    return token
def decode_jwt(token: str) -> int:
    data = jwt.decode(token, "Nurmash", "HS256")
    return data['user_id']


@app.post("/login")
def post_login(request: Request, 
               email: str = Form(), 
               password: str = Form()):
    user = users_repository.get_by_email(email)
    if not user:
        return Response("You didn't authorize")
    if user.password == password:
        response = RedirectResponse("/profile", status_code = 303)
        token = encode_jwt(user.id)
        response.set_cookie("token", token)
        return response
    return Response("Permission denied")

@app.get("/profile")
def get_profile(request: Request, 
                token: str = Cookie()):
    user_id = decode_jwt(token)
    user = users_repository.get_by_id(user_id)
    if not user:
        return RedirectResponse("/login", status_code = 303)
    return templates.TemplateResponse("/profile.html", {"request": request, "user" : user})


@app.get("/flowers")
def get_flowers(request: Request):
    flowers = flowers_repository.get_all()
    return templates.TemplateResponse("flowers/flowers.html", {"request": request, "flowers": flowers})

@app.post("/flowers")
def add_flower(request: Request, name: str = Form(), count: str = Form(), cost: str = Form()):
    flowers_repository.save(name, int(count), int(cost))
    print (flowers_repository.get_all())
    return RedirectResponse("/flowers", status_code = 303)

@app.get("/cart/items")
def get_cart(request: Request, cart: str = Cookie(default = "[]")):
    cart_json = json.loads(cart)
    flowers = flowers_repository.get_flowers_by_cart(cart_json)
    return templates.TemplateResponse("flowers/cart.html", {"request": request, "flowers": flowers})

@app.post("/cart/items")
def add_flower_to_cart(response: Response, flower_id: str = Form(), cart: str = Cookie(default = "[]")):
    cart_json = json.loads(cart)
    if flower_id not in cart_json:
        cart_json.append(flower_id)
    new_cart = json.dumps(cart_json)
    response = RedirectResponse("/flowers", status_code = 303)
    response.set_cookie(key = "cart", value = new_cart)
    return response




# @app.get("/cart/items")
# def get_flowers_from_cart(request: Request):
#     return templates
# конец решения

