"""
auto_vasarely: videoenc.py module
Author: Marek Dohnal
Date: 20/03/2023
"""
import cv2
import numpy as np
import os


def imgs_to_video(save_path, frames_path, imgs, orig_height, orig_width, scale_factor=1):
    """
    Converts an array of image into a video output
    :param frames_path: The path, where frames are saved
    :param orig_width: The width of the original grid
    :param orig_height: The height of the original grid
    :param save_path: the path to save the video in
    :param imgs: the array of images constituting the video
    :param scale_factor: a factor by which the resolution of the video is
            enlarged or shrinked relative to the original input image
    """
    if len(imgs) > 0:
        height = int(orig_height*scale_factor)
        width = int(orig_width*scale_factor)
        out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'DIVX'), 1, (width, height))

        for i, img in enumerate(imgs):
            print(width, height)
            img = cv2.resize(img, (width, height), interpolation=cv2.INTER_NEAREST)
            cv2.imwrite(os.path.join(frames_path, f"frame_{i}.png"), img)
            out.write(img)

        out.release()
