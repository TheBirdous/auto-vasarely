"""
auto_vasarely: videoenc.py module
Author: Marek Dohnal
Date: 20/03/2023
"""
import cv2
import numpy as np


def imgs_to_video(save_path, imgs, scale_factor=1):
    """
    Converts an array of image into a video output
    :param save_path: the path to save the video in
    :param imgs: the array of images constituting the video
    :param scale_factor: a factor by which the resolution of the video is
            enlarged or shrinked relative to the original input image
    """
    if len(imgs) > 0:
        height, width, rgb = imgs[0].shape
        height = int(height*scale_factor)
        width = int(width*scale_factor)
        out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'DIVX'), 1, (width, height))

        for img in imgs:
            resized = img
            if scale_factor != 1:
                resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_NEAREST)
            out.write(resized)

        out.release()
