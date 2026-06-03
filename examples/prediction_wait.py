from muapi import MuAPI

client = MuAPI()

job = client.videos.generate(
    prompt="A cinematic shot of a spaceship",
    wait=False
)

request_id = job["request_id"]

result = client.predictions.wait(
    request_id
)

print(result)