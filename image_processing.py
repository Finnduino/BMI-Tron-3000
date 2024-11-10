from pdf2image import convert_from_path
from PIL import Image
import cv2 as cv
import numpy as np
import logging
import tqdm
from sklearn.cluster import DBSCAN

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

def resize_image(image, scale=0.2):
    scaled = cv.resize(image, None, fx=scale, fy=scale, interpolation=cv.INTER_LINEAR)
    return scaled


def image_to_points(image):
    pts = []
    for i in tqdm.trange(len(image)):
        for j in range(len(image[i])):
            if image[i][j] == 0:
                pts.append((i, j))
    return pts



def clusterize(points,
               image_shape,
               eps=5,
               min_samples=5,
               output_color_filename="default-clustering.jpg",
               output_final_filename="default-clustering-final.jpg"
               ):
    """
    NB! expects grayscaled image
    :param points:
    :param image_shape:
    :param output_final_filename:
    :param output_color_filename:
    :param eps:
    :param min_samples:
    :return:
    """
    # points = image_to_points(image)
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
    labels = clustering.labels_
    classes = max(labels) - min(labels) + 1
    print(max(labels))

    output = np.full((*image_shape, 3), (255, 255, 255))

    for index, (i, j) in enumerate(points):
        diff = (labels[index] + 1) * 255 / classes
        output[i][j] = (0, 255 - diff, diff)

    cv.imwrite(f"IMAGES/{output_color_filename}", output)

    cnt = dict()
    for i in labels:
        if i not in cnt:
            cnt[i] = 0
        cnt[i] += 1
    prs = list(cnt.items())
    prs.sort(key=lambda x: x[1], reverse=True)

    final = np.full(image_shape, 255, dtype=np.uint8)
    good = set()
    i = 0
    while prs[i][1] >= 1000:
        if prs[i][0] != -1:
            good.add(prs[i][0])
        i += 1
    for index, (i, j) in enumerate(points):
        if labels[index] in good:
            final[i, j] = 0
    cv.imwrite(f"IMAGES/{output_final_filename}", final)
    return prs, final

def remove_page_details(
        image,
        eps=5,
        min_samples=12,
        scale_log_filename=None,
):
    """
    Expects a full-sized page.
    :param scale_log_filename:
    :param image:
    :return:
    """
    main_image = to_grayscale(resize_image(image, 0.2))

    if scale_log_filename is not None:
        cv.imwrite(f"IMAGES/{scale_log_filename}", main_image)

    points = image_to_points(main_image)

    p, final = clusterize(points, main_image.shape, eps=eps, min_samples=min_samples)
    print(p[:10])

    return final


def main():
    init()
    opencv_image = to_grayscale(floor_plan_to_opencv_image("floor_1.pdf"))
    logger.info("started writing")
    cv.imwrite("IMAGES/floor_1.png", opencv_image)
    logger.info("finished writing")

if __name__ == '__main__':
    main()