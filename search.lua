local tag = ARGV[1]
local tag_key = "tag:" .. tag

return redis.call("SMEMBERS", tag_key)