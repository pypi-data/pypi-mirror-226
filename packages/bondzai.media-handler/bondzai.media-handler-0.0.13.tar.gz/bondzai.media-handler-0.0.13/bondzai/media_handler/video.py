import imageio
from pathlib import Path

import numpy as np
from imageio.v3 import immeta, improps

from .image import process_raw_img_data
from .base import check_mime


VIDEO_ALLOWED_MIME = [
    "video/mp4",
    "video/quicktime",
    "video/webm"
]


def get_video_metadata(file_path: Path) -> dict:
    mime = check_mime(file_path, VIDEO_ALLOWED_MIME)
    img = immeta(file_path)
    props = improps(file_path)
    return {
        "mime": mime,
        "width": img['size'][0],
        "height": img['size'][1],
        "fps": img['fps'],
        "channels": props.shape[-1]  # Useful ?
    }


def get_video_raw_data(file_path: Path) -> list[float]:
    video = imageio.get_reader(file_path) 
    results = []
    for frame in video.iter_data(): 
        results += process_raw_img_data(frame)
    return results


def save_video_raw_data(raw_data: list, metadata: dict, file_path: Path):
    video = imageio.get_writer(file_path, mode="I", fps=metadata["fps"])
    dim = [metadata["height"], metadata["width"], 3]  # FIXME : wrong dimension (get max(dim) * max(dim))
    dim = [(int(len(raw_data) / np.prod(dim)))] + dim
    vid = (np.reshape(raw_data, dim) * (2 ** 8)).astype("uint8")
    for image in vid:
        video.append_data(image)
    video.close()
