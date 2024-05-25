from fastapi import FastAPI, HTTPException
from redis.asyncio import Redis
from typing import List

app = FastAPI()
REDIS_URL = "redis://default:fPisFPrTXA9PA3lzgROc4kr8e3jhb7oa@redis-17989.c52.us-east-1-4.ec2.redns.redis-cloud.com:17989"
redis = Redis.from_url(REDIS_URL, decode_responses=True)

# Загрузка Lua скриптов
with open("add.lua", "r") as f:
    add_script = f.read()

with open("remove.lua", "r") as f:
    remove_script = f.read()

with open("search.lua", "r") as f:
    search_script = f.read()

@app.post("/{tag}/")
async def add_tag(key: str, tag: str):
    add_tag_sha = await redis.script_load(add_script)
    result = await redis.evalsha(add_tag_sha, 1, key, tag)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to add tag")
    return {"status": "success", "key": key, "tag": tag}

@app.delete("/{tag}/")
async def remove_tag(key: str, tag: str):
    remove_tag_sha = await redis.script_load(remove_script)
    result = await redis.evalsha(remove_tag_sha, 1, key, tag)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to remove tag")
    return {"status": "success", "key": key, "tag": tag}

@app.get("/{tag}/", response_model=List[str])
async def search_by_tag(tag: str):
    search_by_tag_sha = await redis.script_load(search_script)
    keys = await redis.evalsha(search_by_tag_sha, 0, tag)
    return keys