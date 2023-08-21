import os
import uuid
import requests
from ujson import dumps, load


def decodehex(hexdecimal):
    hexdecimal = hex(hexdecimal)

    if hexdecimal.startswith("0x"):
        hexdecimal = hexdecimal[2:]

    return bytes.fromhex(hexdecimal).decode("utf-8")


def get_api_key():
    return (
            decodehex(0x3963346362636331)[::-1] +
            decodehex(0x3765633463623331)[::-1] +
            decodehex(0x6564326130613538)[::-1] +
            decodehex(0x3664306161343434)[::-1]
    )


def get_encryption_key():
    return (
            decodehex(0x412f7838753572)[::-1] +
            decodehex(0x326e586a55665263)[::-1]
    )


def generate_device_id():
    return str(uuid.uuid4())


#  Not Implemented
"""
def decrypt_aes_gcm(token):
    key_bytes = get_encryption_key().encode('utf-8')
    token_bytes = base64.b64decode(token.encode('utf-8'))
    iv = token_bytes[:12]
    ciphertext = token_bytes[12:]
    secret_key = AES.new(key_bytes, AES.MODE_GCM, nonce=iv)
    plaintext = secret_key.decrypt(ciphertext)
    return plaintext.decode('utf-8')
"""

def ocr_solver(image_url, api_key):
    headers = {"apiKey": api_key}
    data = {
        "language": "eng",
        "url": image_url,
        "OCREngine": 5
    }

    response = requests.post("http://api.ocr.space/parse/image", data=data, headers=headers)
    return response.json()["ParsedResults"][0]["TextOverlay"]["Lines"][0]["LineText"]


def save_auth(access_token, refresh_token, handshake_token, userid, username):
    if not os.path.exists("auth.json"):
        with open("auth.json", "w") as f:
            f.write(dumps({}))

    with open("auth.json", "r+") as f:
        data = load(f)

        if username not in data:
            data[username] = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "handshake_token": handshake_token,
                "userId": userid,
                "username": username
            }

        else:
            data[username]["access_token"] = access_token
            data[username]["refresh_token"] = refresh_token
            data[username]["handshake_token"] = handshake_token
            data[username]["userId"] = userid
            data[username]["username"] = username

        f.seek(0)
        f.truncate()
        f.write(dumps(data))


def load_auth(number):
    if os.path.isfile("auth.json"):
        with open("auth.json", "r") as f:
            data = load(f)
            return data[number]

    return {}
