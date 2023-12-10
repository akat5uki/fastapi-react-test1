from uvicorn import run

if __name__ == "__main__":
    run("v1.main:app", reload=True)