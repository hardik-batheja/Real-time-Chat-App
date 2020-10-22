
import io
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
import os
from django.conf import settings



def BytesToImg(image_data):
    image = ImageFile(io.BytesIO(image_data), name='foo.jpg')  # << the answer!
    return image


def BytesToFile(obj,name):
    print(name)
    obj = io.BytesIO(obj)
    file_content = ContentFile(obj.read())
    filename = os.path.join(settings.MEDIA_ROOT, 'msgs', name)
    print(file_content)
    return {'file_content':file_content,'filename':filename}


