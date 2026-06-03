from muapi import MuAPI

client = MuAPI()

result = client.images.edit(
    prompt="Convert this image into anime style",
    image="https://example.com/image.jpg",
    model="flux-kontext-dev"
)

print(result)