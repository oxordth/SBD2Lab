local key = KEYS[1]
local tag = ARGV[1]
local tag_key = "tag:" .. tag

redis.call("SADD", tag_key, key)
redis.call("SADD", "key:" .. key, tag)
return true