from bondzai.media_handler import save_video_raw_data, get_video_raw_data, get_video_metadata
import tempfile
import pytest
from pathlib import Path
import numpy as np

# FIXME : save video not working properly


@pytest.mark.parametrize("format", [(".mov", "video/quicktime")])  # Not test for (".jpg", "image/jpeg") because lossy
def test_video(format):
    TOLERANCE = 1e-4

    width = 32
    height = 24
    depth = 3
    frame_nb = 7
    fps = 20

    save_dir = Path(tempfile.mkdtemp())
    data = np.random.random_integers(0, 2 ** 16 - 1, width * height * depth * frame_nb)
    data = (data.astype("float32") / 2 ** 16).tolist()
    file_path = save_dir / ("test" + format[0])
    save_video_raw_data(data, {"mime": format[1], "width": width, "height": height, "fps": fps}, file_path)
    raw_data = get_video_raw_data(file_path)
    metadata = get_video_metadata(file_path)
    assert metadata["fps"] == fps
    assert metadata["width"] == width
    assert metadata["height"] == height
    assert metadata["mime"] == format[1]
    assert np.max(np.abs(np.asarray(raw_data) - np.asarray(data))) < TOLERANCE
