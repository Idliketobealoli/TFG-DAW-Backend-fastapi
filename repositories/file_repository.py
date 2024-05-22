import os

import aiofiles
from fastapi import HTTPException, status, UploadFile


def get_resources_directory() -> str:
    # Cogemos la ruta de este archivo
    current_file = os.path.abspath(__file__)
    # Y una vez que la tenemos, navegamos por los padres hasta encontrar la carpeta resources
    while not os.path.isfile(os.path.join(current_file, "resources")):
        current_file = os.path.dirname(current_file)
    return current_file


async def upload_file(file: UploadFile, directory_from_resources: str, image_id: str) -> str:
    _, extension = os.path.splitext(file.filename)
    # new_image_name = f"{image_id}-{file.filename}"
    new_image_name = f"{image_id}.{extension}"
    path = os.path.join(get_resources_directory(), directory_from_resources, new_image_name)
    try:
        async with aiofiles.open(path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        print(new_image_name)
        print(path)
        return new_image_name
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Exception while uploading file: {e}")


async def delete_file(path_from_resources: str) -> bool:
    try:
        os.remove(os.path.join(get_resources_directory(), path_from_resources))
        return True
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"File not found for path: {path_from_resources}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Exception while retrieving file: {e}")


async def get_file(path_from_resources: str) -> bytes:
    try:
        path = os.path.join(get_resources_directory(), path_from_resources)
        async with aiofiles.open(path, 'rb') as file:
            file_data = await file.read()
        return file_data
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"File not found for path: {path_from_resources}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Exception while retrieving file: {e}")
