

import cv2
import numpy as np
import random
import matplotlib.pyplot as plt

M = 6
test_images = []


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
                gray_code[x, col, row] = 0 if pixel_value > 0.4 else 1


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

    for x in range(M*2):
        filename = f"gray_code_images/NORMAL{x + 50:05d}.JPG"
        #filename = f"IMG_{x+4360}.JPG"
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


    # cv2.imshow("test", test_images[0])
    # cv2.imshow("test1", test_images[1])
    # cv2.imshow("test2", test_images[2])
    # cv2.imshow("test3", test_images[3])
    # cv2.imshow("test4", test_images[4])
    # cv2.imshow("test5", test_images[5])

    #binary_code = decode_gray(test_images,height_final, width_final)

    #cv2.imshow("good camera", binary_code.astype(np.uint8))

    binary_code_hori = decode_gray(test_images[0:M-1], height_final, width_final)
    binary_code_veri = decode_gray(test_images[M:-1], height_final, width_final)
    #
    decoded_combine = np.stack((binary_code_hori, binary_code_veri,np.zeros_like(binary_code_hori)), axis=-1)

    plt.figure(figsize=(8, 8))
    plt.imshow(decoded_combine)
    plt.title("decoded layered")
    plt.show()

    # cv2.imshow("badcamera", binary_code_veri.astype(np.uint8))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
