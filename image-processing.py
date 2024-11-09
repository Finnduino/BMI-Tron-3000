from pdf2image import convert_from_path
from PIL import Image
import cv2 as cv
import numpy as np
import logging
logger = logging.getLogger(__name__)

def init():
    Image.MAX_IMAGE_PIXELS = None # so that the pdf files can be read
    logging.basicConfig(level=logging.INFO)


def floor_plan_to_opencv_image(path: str):
    pdf_pages = convert_from_path(path, 500)
    if len(pdf_pages) != 1:
        logger.warning("More than 1 page found, ignoring everything but the first page")
    return np.array(pdf_pages[0])[:, :, ::-1]

def to_grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def main():
    init()
    opencv_image = to_grayscale(floor_plan_to_opencv_image("floor_1.pdf"))
    logger.info("started writing")
    cv.imwrite("floor_1.png", opencv_image)
    logger.info("finished writing")

if __name__ == '__main__':
    main()