import hashlib
import os

import requests


def send_generation_request(host, params, files=None):
    api_key = os.environ["STABILITY_KEY"]
    headers = {"Accept": "image/*", "Authorization": f"Bearer {api_key}"}

    if files is None:
        files = {}

    # Encode parameters
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != "":
        files["image"] = open(image, "rb")
    if mask is not None and mask != "":
        files["mask"] = open(mask, "rb")
    if len(files) == 0:
        files["none"] = ""

    response = requests.post(host, headers=headers, files=files, data=params)
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response


def generate_prompt(term: str):
    return f'a simple illustration for language learning purposes of the concept "{term}". Include people in the image, performing an action or experiencing an emotion if possible'


negative_prompt = "ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, out of frame, ugly, extra limbs, bad anatomy, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, mutated hands, fused fingers, too many fingers, long neck, extra head, cloned head, extra body, cloned body, watermark. extra hands, clone hands, weird hand, weird finger, weird arm, (mutation:1.3), (deformed:1.3), (blurry), (bad anatomy:1.1), (bad proportions:1.2), out of frame, ugly, (long neck:1.2), (worst quality:1.4), (low quality:1.4), (monochrome:1.1), text, signature, watermark, bad anatomy, disfigured, jpeg artifacts, 3d max, grotesque, desaturated, blur, haze, polysyndactyly"  # @param {type:"string"}
aspect_ratio = (
    "1:1"  # @param ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]
)
output_format = "jpeg"  # @param ["jpeg", "png"]
model = "sd3.5-large"  # @param ["sd3.5-large", "sd3.5-large", "sd3-large-turbo", "sd3-medium"]

host = f"https://api.stability.ai/v2beta/stable-image/generate/sd3"


def generate_hashed_id(content: str) -> str:
    byte_string = content.encode("utf-8")
    hash_object = hashlib.md5(byte_string)
    return hash_object.hexdigest()


def generate_image(term: str):
    assets_dir = "./image_assets"

    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

    file_path = f"{assets_dir}/{generate_hashed_id(term)}.{output_format}"

    print(file_path)
    # Don't regenerate image if it already exists in assets folder
    if os.path.exists(file_path):
        print(f"Image already exists at {file_path}, returning early...")
        return file_path

    params = {
        "prompt": generate_prompt(term),
        "negative_prompt": negative_prompt if model == "sd3" else "",
        "aspect_ratio": aspect_ratio,
        "seed": 0,
        "output_format": output_format,
        "model": model,
        "mode": "text-to-image",
    }

    response = send_generation_request(host, params)

    # Decode response
    output_image = response.content
    finish_reason = response.headers.get("finish-reason")
    seed = response.headers.get("seed")

    if finish_reason == "CONTENT_FILTERED":
        raise Warning("Generation failed NSFW classifier")

    with open(file_path, "wb") as f:
        f.write(output_image)

    return file_path
