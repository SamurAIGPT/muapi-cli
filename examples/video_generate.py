from muapi import MuAPI

client = MuAPI()

result = client.videos.generate(
    prompt="A dragon flying through clouds",
    model="kling-master",
    wait=False
)

print(result)