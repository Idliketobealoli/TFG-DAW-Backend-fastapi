import os
import aiofiles
from fastapi import HTTPException, status, UploadFile


def get_resources_directory() -> str:
    # Cogemos la ruta de este archivo
    current_file = os.path.abspath(__file__)
    # Y una vez que la tenemos, navegamos por los padres hasta encontrar la carpeta resources
    while not os.path.isdir(os.path.join(current_file, "resources")):
        current_file = os.path.dirname(current_file)
    return os.path.join(current_file, "resources")


async def upload_file(file: UploadFile, directory_from_resources: str, image_id: str) -> str:
    _, extension = os.path.splitext(file.filename)
    new_image_name = f"{image_id}.{extension}"
    path = os.path.join(get_resources_directory(), directory_from_resources, new_image_name)
    try:
        async with aiofiles.open(path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        return new_image_name
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Exception while uploading file: {e}")


def delete_file(path_from_resources: str) -> bool:
    try:
        os.remove(os.path.join(get_resources_directory(), path_from_resources))
        return True
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"File not found for path: {path_from_resources}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Exception while retrieving file: {e}")


def get_file_full_path(directory: str, name: str) -> str:
    path = os.path.join(get_resources_directory(), directory, name)
    print(path)
    if os.path.isfile(path):
        return path
    else:
        return os.path.join(get_resources_directory(), directory, "base.png")
