import cv2


def insert_photo(image_to_insert):
    # Загрузите основное изображение (фон)
    background_image = cv2.imread("imgs/pd_background.png")

    # Получите размеры изображения, которое вы хотите вставить
    image_height, image_width, _ = image_to_insert.shape

    # Выберите координаты для вставки (левый верхний угол)
    x = 0
    y = 0

    # Вставьте изображение
    result = background_image.copy()
    result[y:y + image_height, x:x + image_width] = image_to_insert

    # Сохраните результат
    return result

