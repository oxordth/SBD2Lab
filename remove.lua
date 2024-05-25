local key = KEYS[1]
local tag = ARGV[1]
local tag_key = "tag:" .. tag

redis.call("SREM", tag_key, key)
redis.call("SREM", "key:" .. key, tag)
return true