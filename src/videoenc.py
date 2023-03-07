import cv2
import numpy as np


def imgs_to_video(save_path, scale_factor, imgs):
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
