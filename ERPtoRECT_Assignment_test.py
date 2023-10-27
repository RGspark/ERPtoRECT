import cv2
import numpy as np
import math

def erp2topview(src, pan=0, tilt=0, hfov=120, vfov=90):
    f = src.shape[1] / (2 * math.pi)
    dst_rows = int(2 * f * math.tan(math.radians(vfov) / 2) + 0.5)
    dst_cols = int(2 * f * math.tan(math.radians(hfov) / 2) + 0.5)
    dst = np.zeros((dst_rows, dst_cols, 3), dtype=np.uint8)
    dst_cx = dst_cols / 2
    dst_cy = dst_rows / 2

    for x in range(dst_cols):
        theta = (x - dst_cx) * (2 * math.pi) / dst_cols
        for y in range(dst_rows):
            phi = (y - dst_cy) * math.pi / dst_rows
            D = f / math.tan(phi)
            src_x = int((D * math.sin(theta) + dst_cx))
            src_y = int(dst_cy - (D * math.cos(theta) ))#* math.tan(phi)) + 0.5)
            if 0 <= src_x < src.shape[1] and 0 <= src_y < src.shape[0]:
                dst[y, x] = src[src_y, src_x]

    return dst
    
def erp2frontview(src, pan=0, tilt=0, hfov=120, vfov=90):
    f = src.shape[1] / (2 * math.pi)
    dst_rows = int(2 * f * math.tan(math.radians(vfov) / 2) + 0.5)
    dst_cols = int(2 * f * math.tan(math.radians(hfov) / 2) + 0.5)
    dst = np.zeros((dst_rows, dst_cols, 3), dtype=np.uint8)
    dst_cx = dst_cols / 2
    dst_cy = dst_rows / 2

    for x in range(dst_cols):
        xth = math.atan((x - dst_cx) / f)
        src_x = int((xth + math.radians(pan)) * src.shape[0] / math.pi + 0.5)
        for y in range(dst_rows):
            yth = math.atan((y - dst_cy) / (f / math.cos(xth)))
            src_y = int((yth + math.radians(tilt)) * src.shape[0] / math.pi + src.shape[0] / 2 + 0.5)
            dst[y, x] = src[src_y, src_x]

    return dst

# Load the ERP image
erp_image = cv2.imread('erp.png')

# Convert to front view
front_view = erp2frontview(erp_image, pan=90, tilt=0, hfov=120, vfov=90)

# Convert to top view
top_view = erp2topview(erp_image, pan=0, tilt=0, hfov=120, vfov=90)

# Display the front view image
cv2.imshow('Front View', front_view)

# Display the top view image
cv2.imshow('Top View', top_view)

cv2.waitKey(0)

# Close all OpenCV windows
cv2.destroyAllWindows()
