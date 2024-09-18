# https://aiokafka.readthedocs.io/en/stable/
import json
from collections import Counter

redis = await aioredis.create_redis(("localhost", 6379))
REDIS_HASH_KEY = "aggregated_count:my_topic:0"

tp = TopicPartition("my_topic", 0)
consumer = AIOKafkaConsumer(
    bootstrap_servers='localhost:9092',
    enable_auto_commit=False,
)
await consumer.start()
consumer.assign([tp])

# Load initial state of aggregation and last processed offset
offset = -1
counts = Counter()
initial_counts = await redis.hgetall(REDIS_HASH_KEY, encoding="utf-8")
for key, state in initial_counts.items():
    state = json.loads(state)
    offset = max([offset, state['offset']])
    counts[key] = state['count']

# Same as with manual commit, you need to fetch next message, so +1
consumer.seek(tp, offset + 1)

async for msg in consumer:
    key = msg.key.decode("utf-8")
    counts[key] += 1
    value = json.dumps({
        "count": counts[key],
        "offset": msg.offset
    })
    await redis.hset(REDIS_HASH_KEY, key, value)