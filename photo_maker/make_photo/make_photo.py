import os

import cv2
import numpy as np

from conf import save_dir
from photo_maker.config import photo_width, photo_height
from photo_maker.utils import insert_photo


def stack_photo(src1, src2, uid) -> str:
    im1 = cv2.imread(src1)
    im2 = cv2.imread(src2)
    contrast_image = np.hstack((im1, im2))

    result = insert_photo(contrast_image)
    file_path = os.path.join(save_dir, f'{uid}.jpg')

    cv2.imwrite(file_path, result)

    return file_path


def make_photo(src) -> None:
    input_image = cv2.imread(src)

    new_size = (photo_width, photo_height)

    input_image = _viniette(input_image)

    resized_image = cv2.resize(input_image, new_size)

    done_sepia_image = _sepia(resized_image)

    contrast_image = _increase_contrast(done_sepia_image)

    cv2.imwrite(src, contrast_image)


def _sepia(src_image):
    gray = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
    normalized_gray = np.array(gray, np.float32) / 255
    # solid color
    sepia = np.ones(src_image.shape)
    sepia[:, :, 0] *= 153  # B
    sepia[:, :, 1] *= 204  # G
    sepia[:, :, 2] *= 255  # R
    # hadamard
    sepia[:, :, 0] *= normalized_gray  # B
    sepia[:, :, 1] *= normalized_gray  # G
    sepia[:, :, 2] *= normalized_gray  # R
    return np.array(sepia, np.uint8)


def _increase_contrast(image):
    # converting to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=7.0, tileGridSize=(2, 8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl, a, b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Stacking the original image with the enhanced image
    return enhanced_img


def _viniette(image):
    # Extracting the height and width of an image
    image = cv2.resize(image, (480, 480))

    rows, cols = image.shape[:2]

    # generating vignette mask using Gaussian
    # resultant_kernels
    X_resultant_kernel = cv2.getGaussianKernel(cols, 800)
    Y_resultant_kernel = cv2.getGaussianKernel(rows, 600)

    # generating resultant_kernel matrix
    resultant_kernel = Y_resultant_kernel * X_resultant_kernel.T

    # creating mask and normalising by using np.linalg
    # function
    mask = 255 * resultant_kernel / np.linalg.norm(resultant_kernel)
    output = np.copy(image)

    # applying the mask to each channel in the input image
    for i in range(3):
        output[:, :, i] = output[:, :, i] * mask

    return output
