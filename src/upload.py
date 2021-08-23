import requests
from PIL import Image
import io
from src.grpc import upload


def get_content_type(content):
    content_kind = {'image': 0, 'video': 1, 'audio': 2, 'file': 3, 'skyloveFile': 4, 'testFile': 5}
    for item in content_kind:
        if item in content:
            return content_kind[item]


def upload_file(file_url, stub):
    max_size = 104857600  # 100 mb
    max_image_size = 7000000  # ~7 mb
    request = requests.request(method='GET', url=file_url)
    file_name = request.url.replace("https://static.skylove.su/", "")
    file_name = file_name[file_name.find('/') + 1:]

    attachment = {
        "content": request.content,
        "file_name": file_name,
        "content_kind": get_content_type(request.headers['Content-Type']),  # 5
        "content_type": request.headers['Content-Type']
    }

    byte_size = len(attachment.get("content"))
    # Проверка изображения на размер  и сжатие.
    if byte_size > max_image_size and "image" in attachment['content_type']:
        image = Image.open(io.BytesIO(attachment.get('content')))
        width = image.size[0]
        height = image.size[1]

        koef = width / height
        if koef > 1:
            if width > 3840:  # resolution 4k
                width = 3840
                height = int(width / koef)
                image = image.resize((width, height))
        else:
            if height > 3840:  # resolution 4k
                height = 3840
                width = int(height * koef)
                image = image.resize((width, height))
        attachment['content'] = image.tobytes()

        byte_size = len(image.tobytes())
        if byte_size > max_image_size:
            result_file = io.BytesIO()
            image.save(result_file, format="JPEG", optimizer=True, quality=85)
            attachment['content'] = result_file.getvalue()
            attachment['content_type'] = "image/jpeg"

    # file size > 100mb
    if len(attachment['content']) > max_size:
        return None
    try:
        file = upload(
            stub=stub,
            file_name=attachment["file_name"],
            content_kind=attachment["content_kind"],
            content=attachment['content'],
            content_type=attachment['content_type']
        )
        if file is not None:
            return file
        return None
    except Exception as e:
        print(e, flush=True)

