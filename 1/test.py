import cv2
import numpy as np


def main():
    min_p = (17, 55, 155)
    max_p = (97, 100, 255)
    blur = 1
    color = (255, 255, 255)
    frame = cv2.imread('resources/1.png')
    frame_bl = cv2.medianBlur(frame, 1 + blur * 2)
    frame_rng = cv2.inRange(frame_bl, min_p, max_p)

    image = frame_rng
    edged = cv2.Canny(image, 199, 200, 7)
    contours, hierarchy = cv2.findContours(
        edged,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    number_of_contours = len(contours)
    print(f'Number of Contours found = {number_of_contours}')

    contours_for_draw = sort_contours(contours)[:6]
    contours_for_draw = list(map(
        lambda c: cv2.approxPolyDP(c, 0.03 * cv2.arcLength(c, True), True),
        contours_for_draw))

    img_recs = np.uint8(np.zeros((image.shape[0], image.shape[1])))
    for contour in contours_for_draw:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img_recs, (x, y), (x + w, y + h), color, 1)
    cv2.imshow('Rectangles', img_recs)

    # img_contours = np.uint8(np.zeros((image.shape[0], image.shape[1])))
    # cv2.drawContours(
    #     img_contours,
    #     contours_for_draw,
    #     -1,
    #     color,
    #     1)
    # cv2.imshow('Contours', img_contours)

    # cv2.drawContours(frame, contours_for_draw, -1, color, 1)

    # cv2.imshow('Result', frame)
    cv2.waitKey(0)


def sort_contours(contours):
    return sorted(contours, key=lambda contour: -contour.shape[0])


def main2():
    def nothing(args):
        pass

    cv2.namedWindow("setup")
    cv2.namedWindow("setup2")
    cv2.createTrackbar("b1", "setup", 0, 255, nothing)
    cv2.createTrackbar("g1", "setup", 0, 255, nothing)
    cv2.createTrackbar("r1", "setup", 0, 255, nothing)
    cv2.createTrackbar("b2", "setup", 255, 255, nothing)
    cv2.createTrackbar("g2", "setup", 255, 255, nothing)
    cv2.createTrackbar("r2", "setup", 255, 255, nothing)
    cv2.createTrackbar("blur", "setup2", 0, 10, nothing)
    img = cv2.imread('resources/1.png')  # загрузка изображения
    # percent = 50
    # width = int(img.shape[1] * percent / 100)
    # height = int(img.shape[0] * percent / 100)
    # dim = (width, height)
    # img = cv2.resize(img, dim)
    while True:
        r1 = cv2.getTrackbarPos('r1', 'setup')
        g1 = cv2.getTrackbarPos('g1', 'setup')
        b1 = cv2.getTrackbarPos('b1', 'setup')
        r2 = cv2.getTrackbarPos('r2', 'setup')
        g2 = cv2.getTrackbarPos('g2', 'setup')
        b2 = cv2.getTrackbarPos('b2', 'setup')
        blur = cv2.getTrackbarPos('blur', 'setup2')
        min_p = (g1, b1, r1)
        max_p = (g2, b2, r2)
        img_bl = cv2.medianBlur(img, 1 + blur * 2)  # сглаживание изображения
        img_mask = cv2.inRange(img_bl, min_p, max_p)
        # img_m = cv2.bitwise_and(img, img, mask=img_mask)
        cv2.imshow('img', img_mask)
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
