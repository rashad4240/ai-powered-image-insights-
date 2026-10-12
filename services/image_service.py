from PIL import Image


class ImageService:

    @staticmethod
    def open_image(image_file):
        return Image.open(image_file)