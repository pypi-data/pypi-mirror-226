from pathlib import Path
import tempfile
import yaml
import shutil
import tarfile
from . import get_raw_data, get_metadata, save_binary, iter_data, save_raw_data

UNKNOWN = "unknown"


def get_files_from_tar(tar_path: Path):
    with tarfile.open(tar_path, "r:gz") as tar:
        m = tar.next()
        while m:
            print(m.name)
            m = tar.next()


def create_tar_from_folder(tar_path: Path, folder_path: Path):
    """
    Create tar from one folder, take all files within this folder and add to tar.gz file
    Args:
        tar_path: output tar.gz file
        folder_path: input folder path
    """
    with tarfile.open(tar_path, "w:gz") as tar:
        for file in folder_path.iterdir():
            tar.add(file, arcname=file.name)


def _parse_folder_recursive(data_folder: Path, output_list: list):
    """
    Get recursively list of file in a nested folder organisation, extracting output info by folder names
    Args:
        data_folder: main folder name
        output_list: list of label type in the same order as tree depth
    Returns:
        file_list: list of file path with output labels
    """
    bottom = len(output_list) == 0
    file_list = []
    if bottom:
        for file in data_folder.iterdir():
            file_list.append({"data": file, "output": {}})
    else:
        for element in data_folder.iterdir():
            if element.is_dir():
                label_type = output_list[0]
                label = element.name
                _file_list = _parse_folder_recursive(element, output_list[1:])
                for file_dict in _file_list:
                    file_dict["output"][label_type] = label
                    file_list.append(file_dict)
    return file_list


def convert_to_binary(file_path: Path):
    """
    Convert file to binary, saving in same folder, deleting the initial file
    Args:
        file_path: input file path
    Returns:
        save_file_path: path of the .bin file

    """
    data = get_raw_data(file_path)
    save_file_path = file_path.with_suffix(".bin")
    save_binary(save_file_path, data)
    file_path.unlink()
    return save_file_path


def create_chunks(file_Path: Path, chunk_size: int, hop_len: int, save_folder: Path):
    """
    Create chunks for data file, in a given folder with name "<input_file.name>_<index>.<input_file.ext>"
    Args:
        file_Path: path of the input file
        chunk_size: size of one chunk (in raw_data sens)
        hop_len: number of sample to hop
        save_folder: folder where to save data
    """
    if save_folder.exists():
        shutil.rmtree(save_folder)
    save_folder.mkdir(parents=True, exist_ok=True)
    raw_data = get_raw_data(file_Path)
    metadata = get_metadata(file_Path)
    for index, _data in enumerate(iter_data(raw_data, chunk_size, hop_len)):
        _file_path = save_folder / f"{file_Path.stem}_{str(index).zfill(3)}"
        save_raw_data(_data, metadata, _file_path.with_suffix(file_Path.suffix))


def get_maestro_file_name(file_path: Path, output_dict: dict) -> str:
    """
    From file name and output label, create understandable name for Maestro
    Args:
        file_path: file path
        output_dict: output label dict
    Returns:
        file_name: file_name understandable by Maestro

    """
    output_name = "".join([f"[{key};{value}]" for key, value in output_dict.items()])
    file_name = f"{file_path.stem}{output_name}{file_path.suffix}"
    return file_name


def generate_dataset(data_folder: Path, output_list: list, source_name: str, save_folder: Path,
                     convert_to_bin: bool = True, output_dict: dict = None) -> dict:
    """
    Generate dataset folder from local data organised into nested folder representing labels
    Args:
        data_folder: folder containing all the data (should be .bin files)
        output_list: list of label type in the same order as tree depth
        source_name: name of the source for these files
        save_folder: path of the folder to save, if tar.gz file is given, save into this compressed form instead
        convert_to_bin: If True, convert data to binary
        output_dict: If given, initialise output_dict by that one
    Returns:
        output_dict: "outputs" section of the dataset.yml
    """
    compress = None
    if save_folder.suffixes == [".tar", ".gz"]:
        compress = save_folder
        save_folder = Path(tempfile.mkdtemp())
    else:
        if save_folder.exists():
            shutil.rmtree(save_folder)
        save_folder.mkdir(parents=True)

    if output_dict is None:
        output_dict = {output: {} for output in output_list}
    data_dict = {"dataset": [], "outputs": output_dict}
    file_list = _parse_folder_recursive(data_folder, output_list)
    file_list = sorted(file_list, key=lambda _file: _file["data"])
    for file in file_list:
        file_path = file["data"]
        file["metadata"] = get_metadata(file_path)
        new_file_name = get_maestro_file_name(file_path, file["output"])
        new_file_path = save_folder / new_file_name
        shutil.copy(file_path, new_file_path)
        if convert_to_bin:
            new_file_path = convert_to_binary(new_file_path)
        file["data"] = new_file_path.name
        file["source_id"] = source_name
        data_dict["dataset"].append(file)
        for key, value in file["output"].items():
            if value not in output_dict[key].keys():
                output_dict[key][value] = len(output_dict[key].keys()) + 1 if value.lower() != UNKNOWN else 0

    with open(save_folder / "dataset.yml", "w") as y:
        yaml.safe_dump(data_dict, y, sort_keys=False)

    if compress is not None:
        create_tar_from_folder(compress, save_folder)

    return output_dict
