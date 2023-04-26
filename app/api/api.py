from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

#time user is used parking
#count times user used parking
@app.get("/user_stats/{id}")
async def user_stats(id: str):
    return id

#time parking was available
#time parking was used
@app.get("/city_stats/{city}")
async def city_stats():
    return {"message": "Hello World"}

#time parking was available
#time parking was used
@app.get("/parking_stats/{id}")
async def parking_stats():
    return {"message": "Hello World"}

@app.get("/is_parking_available/{external_id}")
async def is_parking_available():
    return {"message": "Hello World"}