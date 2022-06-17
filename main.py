from fastapi.responses import JSONResponse
from fastapi import FastAPI
import uvicorn
from scrapper import scrap
from tauron import GetData, GetDataForSpecifiedDay
from datetime import datetime

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


@app.get("/tauron")
def read_tauron():
    val, success = GetData()

    if success:
        return {"tauron": val}
    else:
        return JSONResponse({"error": "Something went wrong"}, status_code=404)


@app.get("/tauron/{day}")
def read_tauron(day: str):
    try:
        day = datetime.strptime(day, "%Y-%m-%d")
    except:
        return JSONResponse({"error": "Invalid date format"}, status_code=404)

    val, success = GetDataForSpecifiedDay(day)

    if success == True:
        return {"tauron": val}
    else:
        return JSONResponse({"error": "Invalid day (the day cannot be today)"}, status_code=404)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
