import redis
import os
import dotenv

dotenv.load_dotenv()

redispassword = os.getenv('RAILWAYREDIS')#os.getenv('REDISPASSWORD')
users = redis.Redis(
        host='containers-us-west-132.railway.app',
        password=redispassword,
        port=6696,
    )
""" users = redis.Redis(
  host='redis-18876.c232.us-east-1-2.ec2.cloud.redislabs.com',
  port=18876,
  password=redispassword) """


print(users)
#users.set('test', 'test')
print(users.get('test'))
users.set('lol', 'lol')