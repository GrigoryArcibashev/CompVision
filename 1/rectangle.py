import itertools


class Rectangle:
    def __init__(self, left, top, right, bottom):
        self._left = left
        self._top = top
        self._right = right
        self._bottom = bottom

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def top(self):
        return self._top

    @property
    def bottom(self):
        return self._bottom

    def __str__(self):
        return f'({self.left}, {self.top})x({self.right}, {self.bottom})'


def merge_rectangles(recs: list[Rectangle]) -> list[Rectangle]:
    """
    Объединяет все пересекающиеся прямоугольники
    :param recs: список прямоугольников
    :return: список объединенных прямоугольников
    """
    while True:
        found = 0
        for r1, r2 in itertools.combinations(recs, 2):
            if _intersected(r1, r2):
                if r1 in recs:
                    recs.remove(r1)
                if r2 in recs:
                    recs.remove(r2)
                recs.append(_merge(r1, r2))
                found = 1
                break
        if found == 0:
            break
    return recs


def _merge(r1: Rectangle, r2: Rectangle) -> Rectangle:
    """
    Объединяет два прямоугольника
    :param r1: первый пр-ик
    :param r2: второй пр-ик
    :return: объединенный прямоугольник
    """
    return Rectangle(
        min(r1.left, r2.left),
        min(r1.top, r2.top),
        max(r1.right, r2.right),
        max(r1.bottom, r2.bottom)
    )


def _intersected(r1: Rectangle, r2: Rectangle) -> bool:
    """
    Пересекаются ли два прямоугольника
    :param r1: первый пр-ик
    :param r2: второй пр-ик
    :return: True, если пересекаются, False, если нет
    """
    return (_get_borders_intersection(r1.top, r2.top, max) <= _get_borders_intersection(r1.bottom, r2.bottom, min)
            and _get_borders_intersection(r1.left, r2.left, max) <= _get_borders_intersection(r1.right, r2.right, min))


def _get_borders_intersection(border1, border2, func_for_comparison) -> int:
    return func_for_comparison(border1, border2)


if __name__ == '__main__':
    # Демонстрация работы функции объединения прямоугольников
    rectangles = [
        Rectangle(1, 1, 3, 4),
        Rectangle(2, 3, 5, 6),
        Rectangle(3, 5, 4, 6),
        Rectangle(6, 1, 8, 4)
    ]
    result = merge_rectangles(rectangles)
    print(len(result))
