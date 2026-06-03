from muapi import MuAPI

client = MuAPI()

result = client.images.generate(
    prompt="A futuristic city at sunset",
    model="flux-dev"
)

print(result)