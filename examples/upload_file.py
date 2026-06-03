from muapi import MuAPI

client = MuAPI()

result = client.uploads.upload(
    "image.png"
)

print(result)