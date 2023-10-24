import cv2
from PIL import Image, ImageDraw, ImageFont

from photo_maker.config import photo_height, photo_width


def add_text(src, text: dict):
    got_image = Image.open(src)
    draw_name(got_image, text['name'], text['surname'])
    draw_descr(got_image, text['info'],
               text['descr'],
               text['beh'],
               text['status'])

    got_image.save(src)

    input_image = cv2.imread(src)
    compression_params = [cv2.IMWRITE_JPEG_QUALITY, 30]

    cv2.imwrite(src, input_image, compression_params)


def draw_name(image, name, surname, spacing=20):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("fonts/Oswald-Bold.ttf", 80)
    font_color = (0, 0, 0)

    name_box = draw.textbbox((0, 0), name, font)
    name_width = name_box[2] - name_box[0]
    name_height = name_box[3] - name_box[1]

    surname_box = draw.textbbox((0, 0), surname, font)
    surname_width = surname_box[2] - surname_box[0]
    surname_height = surname_box[3] - surname_box[1]

    sum_height = surname_height + name_height + spacing
    start_height = (photo_height - sum_height) // 2
    if name_width > surname_width:
        delta = name_width - surname_width
        position = (photo_width * 2 + 100, start_height)
        draw.text(position, name, font=font, fill=font_color)
        position = (photo_width * 2 + 100 + delta, start_height + name_height + spacing)
        draw.text(position, surname, font=font, fill=font_color)
    else:
        delta = surname_width - name_width
        position = (photo_width * 2 + 100 + delta, start_height)
        draw.text(position, name, font=font, fill=font_color)
        position = (photo_width * 2 + 100, start_height + name_height + spacing)
        draw.text(position, surname, font=font, fill=font_color)


def draw_descr(image, info="", detail_info="", beh="", status="", spacing=10):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("fonts/SofiaSansExtraCondensed-Medium.ttf", 72)
    font_color = (0, 0, 0)
    text = "\n".join([info, detail_info, beh, status])

    text_box = draw.textbbox((0, 0), text, font)
    text_width = text_box[2] - text_box[0]
    text_height = text_box[3] - text_box[1]

    lines = text.split("\n")
    text_height += (len(lines) - 1) * spacing
    width_pos = (image.width - text_width) // 2
    prev_line_y = photo_height + ((image.height - photo_height - text_height) // 2)
    for line in lines:
        line_box = draw.textbbox((0, 0), line, font)
        line_height = line_box[3] - line_box[1]
        position = (width_pos, prev_line_y)
        prev_line_y += line_height + spacing
        draw.text(position, line, font=font, fill=font_color)
