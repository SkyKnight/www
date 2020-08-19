#-*- coding: utf-8 -*-

from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image
import os

def _add_thumb(s):
    """
    Modyfikuje łańcuch znaków zawierający nazwę pliku, wstawiając rozszerzenie '.thumb' przed rozszerzeniem pliku (które przy okazji jest zmieniane na '.jpg').
    """
    parts = s.split(".")
    parts.insert(-1, "thumb")
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return ".".join(parts)

def _add_600px(s):
    """
    Modyfikuje łańcuch znaków zawierający nazwę pliku, wstawiając rozszerzenie '.600px' przed rozszerzeniem pliku (które przy okazji jest zmieniane na '.jpg').
    """
    parts = s.split(".")
    parts.insert(-1, "600px")
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return ".".join(parts)


class ThumbnailImageFieldFile(ImageFieldFile):
    def _get_thumb_path(self):
        return _add_thumb(self.path)
    thumb_path = property(_get_thumb_path)

    def _get_600px_path(self):
        return _add_600px(self.path)
    i600px_path = property(_get_600px_path)
    
    def _get_thumb_url(self):
        return _add_thumb(self.url)
    thumb_url = property(_get_thumb_url)

    def _get_600px_url(self):
        return _add_600px(self.url)
    i600px_url = property(_get_600px_url)

    def save(self, name, content, save=True):
        super(ThumbnailImageFieldFile, self).save(name, content, save)
        img = Image.open(self.path)
        img600 = Image.open(self.path)
        img.thumbnail(
            (self.field.thumb_width, self.field.thumb_height),
            Image.ANTIALIAS
        )
        img.save(self.thumb_path, 'JPEG')
        wpercent = (self.field.i600px_width/float(img600.size[0]))
        newheight = int((float(img600.size[1])*float(wpercent)))
        img600=img600.resize(
            (self.field.i600px_width, newheight),
            Image.ANTIALIAS
        )
        img600.save(self.i600px_path, 'JPEG')

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        if os.path.exists(self.i600px_path):
            os.remove(self.i600px_path)    
        super(ThumbnailImageFieldFile, self).delete(save)


class ThumbnailImageField(ImageField):
    """
    Działa jak zwykłe pole ImageField, a dodatkowo przechowuje plik miniatury (JPEG). Udostępnia ona dodatkowe metody get_FIELD_thumb_url() i get_FIELD_thumb_filename().
    Klasa przyjmuje dwa dodatkowe argumenty: thumb_width i thumb_height (szerokość i wysokość miniatury) przyjmujące wartości domyślne 128 (pikseli). Zmiana rozmiaru nie wpływa na zmianę proporcji przy jednoczesnym pozostaniu w obrębie żądanych wymiarów. Zapoznaj się z dokumentacją metody Image.thumbnail z biblioteki PIL.
    """
    attr_class = ThumbnailImageFieldFile

    def __init__(self, thumb_width=150, thumb_height=250, i600px_width=600, i600px_height=600, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        self.i600px_width = i600px_width
        self.i600px_height = i600px_height
        
        
        super(ThumbnailImageField, self).__init__(*args, **kwargs)
