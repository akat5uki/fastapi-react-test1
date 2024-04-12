from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from securecookies import SecureCookiesMiddleware
# from securecookies.extras import csrf
from ..core.routers import users, auth, items, chat
from ..core.utilities.config import Settings

settings = Settings()

app = FastAPI(root_path="/api/v1")

origins = settings.cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # expose_headers=["set-cookie"],
)

# app.add_middleware(
#     SecureCookiesMiddleware,
#     secrets=["3BpRMW112WrKHag1Yml3sL5uDMKouW1GXfg-8zmK5p8="]
# )

# app.add_middleware(
#     csrf.SecureCSRFMiddleware,
#     secret="3BpRMW112WrKHag1Yml3sL5uDMKouW1GXfg-8zmK5p8=",
# )

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(chat.router)


@app.get("/", tags=["root"])
async def get_root() -> dict:
    return {"message": "Hello World"}
