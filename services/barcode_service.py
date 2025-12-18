from pyzbar.pyzbar import decode
from PIL import Image

class BarcodeService:
    @staticmethod
    def read_barcode(image_path):
        img = Image.open(image_path)
        barcodes = decode(img)
        if barcodes:
            return barcodes[0].data.decode('utf-8')
        return None