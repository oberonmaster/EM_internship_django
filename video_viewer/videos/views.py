from django.shortcuts import render

# Create your views here.
#TODO создать вью получения конкретного видео по ID
"/v1/videos/{video.id}/"

#TODO создать вью списка видео (должна быть пагинация)
"/v1/videos/"

#TODO создать вью списка идентификаторов опубликованных видео
"/v1/videos/ids/"

#TODO создать вью  добавления/удаления лайка (с ограничением - один пользователь может поставить только один лайк на видео)
"/v1/videos/{video.id}/likes/"

#TODO создать вью получения статистики по видео в двух вариантах
"/v1/videos/statistics-subquery/"
"/v1/videos/statistics-group-by/"