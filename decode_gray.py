
import open3d as o3d
import cv2
import numpy as np
import random
import matplotlib.pyplot as plt
from depthMap import triangulate_points
from instrinsic_calibraton import calibration
from matplotlib.colors import ListedColormap, BoundaryNorm


M = 6
test_images = []

def visualize_projector_mapping(camera_to_projector_mapping, axis='x'):
    if axis not in ['x', 'y']:
        raise ValueError("Axis must be 'x' or 'y'.")

    coord_index = 0 if axis == 'x' else 1
    projector_coords = camera_to_projector_mapping[:, :, coord_index]


    valid_mask = projector_coords >= 0
    projector_coords[~valid_mask] = -1


    unique_values = np.unique(projector_coords[valid_mask])
    num_unique_values = len(unique_values)

    cmap = plt.cm.get_cmap('tab20', num_unique_values)  # Use a discrete colormap with unique colors
    norm = BoundaryNorm(boundaries=np.arange(-1, num_unique_values), ncolors=num_unique_values)


    value_to_index = {v: i for i, v in enumerate(unique_values)}
    indexed_map = np.full_like(projector_coords, -1)
    for value, index in value_to_index.items():
        indexed_map[projector_coords == value] = index

    indexed_map[~valid_mask] = -1


    plt.figure(figsize=(10, 6))
    plt.title(f"Projector {axis}-coordinate Mapping (Unique Values)")
    im = plt.imshow(indexed_map, cmap=cmap, norm=norm)
    plt.axis('off')


    cbar = plt.colorbar(im, orientation='vertical', ticks=np.arange(num_unique_values))
    cbar.ax.set_yticklabels(unique_values)
    cbar.set_label(f"Projector {axis}-coordinate")
    plt.show()

# relook at this
def gray_to_binary(gray_code):
    binary_code = gray_code[0]
    for i in range(1, len(gray_code)):
        binary_code = binary_code + str(int(binary_code[-1]) ^ int(gray_code[i]))
    return int(binary_code, 2)



def decode_gray(test_images, height, width):

    # height, width = test_images[0].shape

    gray_code = np.zeros((M, height, width), dtype=int)

    for x in range(M-1):
        for col in range(height):
            for row in range(width):

                pixel_value = test_images[x][col, row] / 255.0

                #need a better algorithmn for this as well... this is not ideal
                gray_code[x, col, row] = 0 if pixel_value > 0.5 else 1


    gray_code_sequence = np.empty((height, width), dtype=object)
    binary_sequence = np.zeros((height, width), dtype=int)



    for col in range(height):
        for row in range(width):
            gray_code_sequence[col, row] = ''.join(str(gray_code[x, col, row]) for x in range(M))
            binary_sequence[col, row] = gray_to_binary(gray_code_sequence[col, row])


    # cv2.imshow("Altered", binary_sequence_left.astype(np.uint8))
    # cv2.imshow("Original", binary_sequence.astype(np.uint8))

    return binary_sequence


def main():

    for x in range(M):
        #filename = f"gray_code_images/NORMAL{x + 50:05d}.JPG"
        filename = f"IMG_{x+4360}.JPG"
        img = cv2.imread(filename)
        if img is None:
            raise FileNotFoundError(f"Image not found: {filename}")
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        height_new, width_new, channel = img.shape

        width_final = 300
        aspect_ratio = height_new/width_new
        height_final = int(width_final*aspect_ratio)

        K = cv2.resize(img_grey, (width_final, height_final))
        test_images.append(K)


    #binary_code = decode_gray(test_images,height_final, width_final)

    #cv2.imshow("good camera", binary_code.astype(np.uint8))

    binary = decode_gray(test_images, height_final, width_final)

    combine = np.stack((binary, binary,np.zeros_like(binary)), axis=-1)

    #binary_code_hori = decode_gray(test_images[0:M-1], height_final, width_final)
    #binary_code_veri = decode_gray(test_images[M:-1], height_final, width_final)

    #
    #decoded_combine = np.stack((binary_code_hori, binary_code_veri,np.zeros_like(binary_code_hori)), axis=-1)

    visualize_projector_mapping(combine, axis = 'x')
    #
    # plt.figure(figsize=(8, 8))
    # plt.imshow(decoded_combine)
    # plt.title("decoded layered")
    # plt.show()
    #
    # # cv2.imshow("badcamera", binary_code_veri.astype(np.uint8))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # camera_mtx = calibration()
    # #placeholder
    # proj_mtx = np.array([[850, 0, 340], [0, 900, 360], [0, 0, 1]], dtype=np.float32)
    # R_camera = np.eye(3)
    # t_camera = np.zeros((3, 1))
    #
    # print(R_camera)
    # print(t_camera)
    # points = triangulate_points(binary_code_hori, binary_code_veri, camera_mtx, proj_mtx, R_camera, t_camera)
    # print(points)




if __name__ == '__main__':
    main()
