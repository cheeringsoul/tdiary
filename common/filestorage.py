import os
import io
import base64
import hashlib
import whatimage
from flask import current_app
from werkzeug.datastructures import FileStorage


class ImageFileStorage(object):
    """存储通过form表单提交过来图片文件"""

    def __init__(self, file_storage):
        assert isinstance(file_storage, FileStorage)
        self.file_storage = file_storage
        self._image_type = None
        self.image_uri_prefix = current_app.config['IMG_PREFIX']

    @property
    def image_type(self):
        if not self._image_type:
            self._image_type = whatimage.identify_image(self.file_storage.stream.read())
            self.file_storage.stream.seek(0)
        return self._image_type

    @property
    def image_name(self):
        md5 = hashlib.md5()
        md5.update(self.file_storage.stream.read())
        self.file_storage.stream.seek(0)
        hash_code = md5.hexdigest()
        return str(hash_code).lower()

    def check_image_type(self):
        allowed = current_app.config['ALLOW_IMAGE_TYPE']
        return self.image_type in allowed

    def save(self):
        filename = self.file_storage.filename
        if not self.file_storage or filename == '':
            return
        local_image_path = current_app.config['UPLOAD_FOLDER']
        image_full_path = os.path.join(local_image_path, self.image_name) + '.' + self.image_type
        img_uri = self.image_uri_prefix + self.image_name + '.' + self.image_type
        if not os.path.exists(image_full_path):
            self.file_storage.save(image_full_path)
        return img_uri


class ImageBase64Storage(object):

    def __init__(self, b64_string):
        b64_data = b64_string.split(',')[-1]  # 去掉data:image/jpeg;base64头部
        self.b64_data = base64.b64decode(b64_data)
        self._image_type = None

    @property
    def image_type(self):
        if not self._image_type:
            image = io.BytesIO(self.b64_data)
            self._image_type = whatimage.identify_image(image)
            # self._image_type = imghdr.what(image)
        return self._image_type

    def check_image_type(self):
        allowed = current_app.config['ALLOW_IMAGE_TYPE']
        return self.image_type in allowed

    def save(self):
        local_image_path = current_app.config['UPLOAD_FOLDER']
        md5 = hashlib.md5()
        md5.update(self.b64_data)
        hash_code = md5.hexdigest()
        new_filename = str(hash_code).lower()
        image_full_path = os.path.join(local_image_path, new_filename) + '.' + self.image_type
        if not os.path.exists(image_full_path):
            with open(image_full_path, "wb") as f:
                f.write(self.b64_data)
        return image_full_path



