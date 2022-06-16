from fastapi.responses import JSONResponse
from fastapi import FastAPI
import uvicorn
from scrapper import scrap

cache = {"power_now": 0}

app = FastAPI()


@app.get("/")
def root():
    return {"hello": "/data"}


@app.get("/data")
def read_default():
    return read_root()


@app.get("/data/{arg_}")
def read_root(arg_="webdata_now_p") -> str:

    if len(arg_) - arg_.count(' ') < 1:
        return {"error": "Invalid name"}

    value, success = scrap(arg_)

    arg_ = str(arg_)

    if success:
        cache[arg_] = value
        return {arg_: value, "cache": False}
    else:
        if arg_ in cache.keys():
            return {arg_: cache[arg_], "cached": True}
        else:
            return JSONResponse({"error": "Invalid argument or value is not cached yet"}, status_code=404)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)