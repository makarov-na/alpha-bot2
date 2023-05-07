import time

import cv2

#cap = cv2.VideoCapture("./video_camera_on_line.h264")
cap = cv2.VideoCapture("/home/mna/Projects/Youtube/12_camera-video/line_follow.h264")

success, original_frame = cap.read()

# Уменьшаем кадр в два раза
scale_percent = 50
frame_width = int(original_frame.shape[1] * scale_percent / 100)
frame_height = int(original_frame.shape[0] * scale_percent / 100)
dir = '/home/mna/tmp/bot-video/camera-video/'

mask_for_black_colour_stream = cv2.VideoWriter(dir + 'mask_for_black_colour.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (frame_width, frame_height))
eroded_mask_stream = cv2.VideoWriter(dir + 'eroded_mask.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (frame_width, frame_height))
dilated_mask_stream = cv2.VideoWriter(dir + 'dilated_mask.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (frame_width, frame_height))
bgr_mask_stream = cv2.VideoWriter(dir + 'bgr_mask.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (frame_width, frame_height))
resized_frame_stream = cv2.VideoWriter(dir + 'resized_frame.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (frame_width, frame_height))

while success:

    resized_frame = cv2.resize(original_frame, (frame_width, frame_height))
    # resized_frame = resized_frame[int(height/3):int(height*2/3), 0:width]

    # Переводим кадр в HSV, чтобы отфильтровать черный цвет. Цветовая фильтрация в RGB работает плохо.
    hsv_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)

    # Выбираем диапазон для фильтрации
    black_color_low = (0, 0, 0)
    black_color_high = (255, 255, 110)
    mask_for_black_colour = cv2.inRange(hsv_frame, black_color_low, black_color_high)
    mask_for_black_colour_stream.write(cv2.cvtColor(mask_for_black_colour, cv2.COLOR_GRAY2BGR))
    cv2.imshow('mask_for_black_colour', mask_for_black_colour)

    # Вытравливаем мелкие элементы для устранения шума.
    erode_kernel = cv2.getStructuringElement(cv2.MORPH_ERODE, (50, 50))
    eroded_mask = mask_for_black_colour.copy()
    cv2.erode(mask_for_black_colour, erode_kernel, eroded_mask)
    eroded_mask_stream.write(cv2.cvtColor(eroded_mask, cv2.COLOR_GRAY2BGR))
    cv2.imshow('eroded_mask', eroded_mask)

    # Выполняем заливку оставшихся элементов для устранения избыточного вытравливания
    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_DILATE, (60, 60))
    dilated_mask = eroded_mask.copy()
    cv2.dilate(eroded_mask, dilate_kernel, dilated_mask)
    dilated_mask_stream.write(cv2.cvtColor(dilated_mask, cv2.COLOR_GRAY2BGR))
    cv2.imshow('dilated_mask', dilated_mask)

    # Находим на маске контуры
    # Не возвращать вложенные контуры cv2.RETR_EXTERNAL
    contours, hierarchy = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Для визуализации переводим маску в RGB и рисуем контур
    bgr_mask = cv2.cvtColor(dilated_mask, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(bgr_mask, contours, -1, (0, 255, 0), 3)
    bgr_mask_stream.write(bgr_mask)
    cv2.imshow('bgr_mask', bgr_mask)

    # Рисуем контуры на оригинальной картинке
    cv2.drawContours(resized_frame, contours, -1, (0, 255, 0), 3)

    # Находим контуры и берем самый большой по площади
    if len(contours) > 0:
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(resized_frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        deviation = x - (frame_width - (x + w))
        cv2.putText(resized_frame, "Deviation: " + str(deviation), (0, 0 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('resized_frame', resized_frame)
    resized_frame_stream.write(resized_frame)

    k = cv2.waitKey(1)
    if k == 27:  # Escape
        break

    if len(contours) > 1:
        time.sleep(2)
    success, original_frame = cap.read()

mask_for_black_colour_stream.release()
eroded_mask_stream.release()
dilated_mask_stream.release()
bgr_mask_stream.release()
resized_frame_stream.release()