from PIL import Image
from poppler import load_from_file, PageRenderer, load_from_data
import  pdf2image 


def pdf_to_image2(pdf_file, page_num):
    images = pdf2image.convert_from_bytes(pdf_file.getvalue(), first_page=page_num+1, last_page=page_num+1)

    return images[0]