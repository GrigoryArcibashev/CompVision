import cv2
from rectangle import Rectangle, merge_rectangles


def _resize(frame, percent):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    return cv2.resize(frame, (width, height))


def _capture_from(cap):
    title_original = "Original + rectangles"  # окно для оригинального ролика с выделением объектов
    title_filter = "Binary filter"  # окно для бинарного фильтра
    _make_windows((title_filter, title_original))

    # Проверка: получилось ли захватить видео из файла/камеры
    if not cap.isOpened():
        print('Cannot open')
    while cap.isOpened():
        ret, frame = cap.read()
        # Если кадр считан успешно
        if ret:
            # получаем бинарное представление кадра
            filtered_frame = _filter_out_colors(frame)
            # находим контуры объектов с помощью бинарного представления
            contours = _find_contours(filtered_frame.copy())
            # убираем из найденных контуров лишние
            contours_for_rectangles = _extract_contours_for_rectangles(contours, len(contours) // 5)
            # каждый контур помещаем в прямоугольник
            rectangles = _create_rectangles(contours_for_rectangles)
            # рисуем каждый прямоугольник
            _draw_rectangles(frame, rectangles, (110, 240, 130))
            # отображение результатов
            _show(frame, title_original)
            _show(filtered_frame, title_filter)
            # остановка работы программы через нажатие клавиши q
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


def _show(frame, title_original):
    """
    Отображение кадра в окне
    :param frame: кадр
    :param title_original: название окна
    :return: None
    """
    cv2.imshow(title_original, frame)


def _make_windows(titles):
    """
    Создаёт окна
    :param titles: названия окон (сколько названий, столько и окон)
    :return: None
    """
    for title in titles:
        cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)


def _draw_rectangles(frame, rectangles, color):
    """
    Рисует в кадре прямоугольники
    :param frame: кадр
    :param rectangles: список прямоугольников
    :param color: цвет прямоугольников
    :return: None
    """
    for rec in merge_rectangles(rectangles):
        cv2.rectangle(frame, (rec.left, rec.top), (rec.right, rec.bottom), color, 2)


def _create_rectangles(contours):
    """
    Создаёт прямоугольники для контуров
    :param contours: контуры
    :return: прямоугольники
    """
    rectangles = []
    for contour in contours:
        # с помощью boundingRect получаем левый угол (x, y), ширину (w) и высоту (h)
        # прямоугольника, в который вписан контур
        x, y, w, h = cv2.boundingRect(contour)
        rectangles.append(Rectangle(x, y, x + w, y + h))
    return rectangles


def _extract_contours_for_rectangles(contours, count):
    """
    Выбор контуров, для которых будут рисоваться пр-ки
    :param contours: контуры
    :param count: количество контуров, для которых будут рисоваться прямоугольники
    :return: выбранные контуры
    """
    contours_for_draw = []
    if contours:
        # выборка контуров
        contours_for_draw = _sort_contours(contours)[:min(count, len(contours))]
        # аппроксимация контуров (для этого используется approxPolyDP)
        contours_for_draw = list(map(
            lambda cntr: cv2.approxPolyDP(
                cntr,
                # максимальное расстояние от контура до аппроксимируемого контура
                0.03 * cv2.arcLength(cntr, True),  # длина контура (True - закрытый контур)
                True),  # True - закрытый контур
            contours_for_draw))
    return contours_for_draw


def _sort_contours(contours):
    """
    Сортировка контуров в порядке убывания по их величине
    :param contours: контуры
    :return: отсортированные контуры
    """
    return sorted(contours, key=lambda contour: -cv2.arcLength(contour, True))


def _find_contours(filtered_frame):
    """
    Находит контуры в кадре
    :param filtered_frame: бинарный кадр
    :return: найденные контуры
    """
    # Находим границы объектов в кадре
    # (контуры будут находиться и в оригинальном бинарном кадре, но хуже;
    # опытным путём пришёл к тому, что лучше сначала найти границы объектов,
    # после чего выделить контуры)
    edged = cv2.Canny(filtered_frame, 0, 200)  # градиенты интенсивности (0 и 200) подобраны экспериментально
    # находим контуры и их иерархию (в данном случае она не нужна)
    contours, hierarchy = cv2.findContours(
        edged,
        cv2.RETR_EXTERNAL,  # нас интересуют только крайние внешние контуры
        cv2.CHAIN_APPROX_SIMPLE)  # контуры будут храниться в виде отрезков
    return contours


def _filter_out_colors(frame):
    """
    Переводит кадр в бинарный вид
    :param frame: кадр
    :return: бинарный кадр
    """
    # g, b, r
    min_p = (17, 35, 155)  # нижняя граница значений пикселя в формате RGB
    max_p = (97, 100, 255)  # верхняя граница значений пикселя в формате RGB
    blur = 1
    # inRange помечает белым пиксели, попавшие в диапазон [min_p, max_p], чёрным - пиксели вне этого диапазона
    # medianBlur снижает шум кадра, получаются более точные бинарные очертания объектов
    return cv2.inRange(cv2.medianBlur(frame, 1 + blur * 2), min_p, max_p)


def capture_from_camera():
    """
    Захват видео с камеры
    :return: None
    """
    _capture_from(cv2.VideoCapture(0))


def capture_from_file(filepath):
    """
    Захват видео из файла
    :param filepath: путь к файлу
    :return: None
    """
    _capture_from(cv2.VideoCapture(filepath))


if __name__ == '__main__':
    capture_from_file('../resources/video.mp4')
    # capture_from_camera()
