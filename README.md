#import "@preview/touying:0.5.4": *
#import themes.default: *

#show: default-theme.with(
  aspect-ratio: "16-9",
  footer: [Д.С. Цымбалюк \| Летняя практика 2026],
)

// ===== СЛАЙД 1: ТИТУЛЬНЫЙ =====
#slide[
  #align(center)[
    #text(size: 18pt, weight: "bold")[АЛТАЙСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ]
    #v(1em)
    #text(size: 14pt)[Институт Цифровых Технологий Электроники и Физики]
    #v(0.5em)
    #text(size: 12pt)[Кафедра вычислительной техники и электроники]
    #v(3em)
    #text(size: 20pt, weight: "bold")[Летняя практика]
    #v(1em)
    #text(size: 16pt)[Игра "Космический корабль с астероидами"]
    #v(3em)
    #text(size: 14pt)[Выполнил: Дмитрий Цымбалюк, гр. 5.506-2]
    #v(0.5em)
    #text(size: 14pt)[Роль: звуковое сопровождение]
    #v(2em)
    #text(size: 12pt)[Барнаул 2026]
  ]
]

// ===== СЛАЙД 2: СОДЕРЖАНИЕ =====
#slide[
  #text(size: 18pt, weight: "bold")[Содержание]
  #v(1em)
  
  #set align(left)
  #grid(
    columns: (1fr, 1fr),
    rows: 9,
    [
      • День 1. Понедельник 08.06
      
      • День 2. Вторник 09.06
      
      • День 3. Среда 10.06
      
      • День 4. Четверг 11.06

      • День 5. Понедельник 15.06
    ],
    [
      • День 6. Вторник 16.06
      
      • День 7. Среда 17.06
      
      • День 8. Четверг 18.06

      • День 9. Пятница 19.06
      
      • Итоги
    ],
  )
]

// ===== СЛАЙД 3: ДЕНЬ 1 =====
#slide[
  #text(size: 18pt, weight: "bold")[День 1. Понедельник 08.06]
  #v(1em)
  
  #text(weight: "bold", size: 14pt)[Задачи:]
  #v(0.5em)
  - Распределиться по группам
  - Выбрать проект, написать идею
  - Распределить роли
  - Составить план
  
  #text(weight: "bold", size: 14pt)[Выбранная идея:]
  Создать несколько игр и реализовать лаунчер для их запуска:
  - Змейка
  - Динозаврик
  - Сапёр
  
  #v(1em)
  #text(weight: "bold", size: 14pt)[Моя роль:]
  Создание лаунчера для запуска игр
]

// ===== СЛАЙД 4: ДЕНЬ 1 — ПОДРОБНОСТИ =====
#slide[
  #text(size: 16pt, weight: "bold")[День 1. Основная идея и изучение]
  #v(1em)
  
  #text(weight: "bold", size: 20pt)[Основная идея:]
  #v(0.5em)
  Папка содержит 3 файла с кодами игр и один файл-лаунчер.
  Преимущество — код каждой игры можно редактировать отдельно.
  
  #v(1em)
  #text(weight: "bold", size: 20pt)[Что необходимо изучить:]
  #v(0.5em)

  #set align(left)
  #grid(
    columns: (1fr, 1fr),
    rows: 9,
    [
        *Основы C\# и .NET:*
  - Создание классов
  - Пространства имён (namespace)
  - Методы и события
  - Работа с формами (Form)
  
    ],
    [
        *Архитектура приложения:*
  - Разделение кода на несколько файлов
  - Взаимодействие между формами
  - Точка входа (Main метод)
  - Жизненный цикл Windows Forms
    ],
  )
]

// ===== СЛАЙД 5: ДЕНЬ 2 =====
#slide[
  #text(size: 16pt, weight: "bold")[День 2. Вторник 09.06]
  #v(1em)
  
  #text(weight: "bold", size: 20pt)[Смена плана:]
  #v(0.5em)
  Решили создать игру *"Космический корабль с астероидами"*
  
  #v(1em)
  #text(weight: "bold", size: 14pt)[Суть игры:]
  Космический корабль стреляет по летящим астероидам.
  Можно подбирать бонусы для улучшения корабля.
  
  #v(1em)
  #text(weight: "bold", size: 20pt)[Моя роль:]
  Создание звуков элементов игры и музыкального сопровождения
]

// ===== СЛАЙД 6: ДЕНЬ 2 — ЗВУКИ =====
#slide[
  #text(size: 20pt, weight: "bold")[День 2. Создание звуков]
  #v(1em)
  
  #set align(left)
  #grid(
    columns: (1fr, 1fr),
    rows: 9,
    [
  
  #text(weight: "bold", size: 17pt)[Созданные звуки:]
  #v(0.5em)
  - Выстрела
  - Фоновая музыка
  - Взрыв корабля (столкновение с астероидом)
  - Раскол астероидов (попадание выстрелом)
  - Тройной выстрел (бонус)
  - Подбор бонуса скорости
  - Подбор бонуса тройного выстрела
], [
  #v(1em)
  
  #text(weight: "bold", size: 20pt)[Выполненные действия:]
  
  #v(0.5em)
  - Создана папка Sounds
  - Проведён поиск, обрезка и конвертация звуков
  - Каждый файл помещён на GitHub
  - Участие в обсуждениях
  ]
)
]
// ===== СЛАЙД 7: ДЕНЬ 3 =====
#slide[
  #text(size: 16pt, weight: "bold")[День 3. Среда 10.06]
  #v(1em)
  
  #text(weight: "bold", size: 18pt)[Задачи:]
  #v(0.5em)
  - Помочь внедрить аудиофайлы в игру
  - Нарисовать спрайты
  - Добавить звуки подбора бонусов
  
  #v(1em)
  #text(weight: "bold", size: 18pt)[Выполнение:]

  - Нарисован спрайт аптечки и добавлен на GitHub
  - Добавлен звук подбора аптечки
  - Нарисован спрайт бонуса скорости
  - Добавлен звук подбора бонуса скорости
  - Обновлён спрайт корабля
]

// ===== СЛАЙД 8: ДЕНЬ 3 — КОД =====
#slide[
  #text(size: 20pt, weight: "bold")[День 3. Внедрение звуков в Python]
  
  #v(1em)

  #text(weight: "bold", size: 16.8pt)[Инициализация:]
  ```py
  pygame.mixer.init()
  ```
#v(0.5em)
#text(weight: "bold", size: 19pt)[Загрузка звуков:]
#text(weight: "medium", size: 17pt)[
```py
shoot_sound = pygame.mixer.Sound('assets/shoot.mp3')
boom_sound = pygame.mixer.Sound('assets/boom.mp3')
dead_asteroid_sound = pygame.mixer.Sound('assets/dead_asteroid.mp3')
pygame.mixer.music.load('assets/music.mp3')
```
]
#text(weight: "bold", size: 19pt)[Воспроизведение:]
#text(weight: "medium", size: 17pt)[
```py
if shoot_sound:
    shoot_sound.play()
pygame.mixer.music.play(-1)
]
```
]
]
// ===== СЛАЙД 9: ДЕНЬ 4 =====
#slide[
#text(size: 20pt, weight: "bold")[День 4. Четверг 11.06]
#v(1em)

  #set align(left)
  #grid(
    columns: (1fr, 1fr),
    rows: 9,
    [

#text(weight: "bold", size: 18pt)[Задачи:]

Найти информацию по созданию главного меню

Создать главное меню

Добавить звуки для босса
], [

#text(weight: "bold", size: 17pt)[Выполнение:]
#v(-0.5em)
Добавлен звук подбора аптечки

Добавлен звук появления босса

Добавлен звук появления снарядов босса
#v(-0.5em)
Добавлена музыка для сражения с боссом
#v(-0.5em)
Добавлен звук подбора бонуса скорости атаки
#v(-0.5em)
Сделано возвращение обычной музыки после босса
]
)
]
// ===== СЛАЙД 10: ДЕНЬ 4 — КОД =====
#slide[
#text(size: 20pt, weight: "bold")[День 4. Примеры кода]
#v(0.5em)

#text(weight: "bold")[Звук появления босса:]

py
spawning_sound = pygame.mixer.Sound('assets/terraria.mp3')
spawning_sound.play()
#v(0.5em)
#text(weight: "bold")[Музыка для босса:]

py
dark_sound = pygame.mixer.Sound('assets/DarkSouls.mp3')
dark_sound.set_volume(0.5)
dark_sound.play()
#v(0.5em)
#text(weight: "bold")[Звук подбора бонуса:]

py
powerup_sound = pygame.mixer.Sound('assets/PowerUp.mp3')
if powerup_sound:
    powerup_sound.play()
]

// ===== СЛАЙД 11: ДЕНЬ 5 =====
#slide[
#text(size: 16pt, weight: "bold")[День 5. Понедельник 15.06]
#v(1em)

#text(weight: "bold", size: 14pt)[Задачи:]
#v(0.5em)

Исправить баг со звуками

Добавить исправленные звуки в обновлённую версию

#v(1em)
#text(weight: "bold", size: 14pt)[Выполнение:]
#v(0.5em)

Исправлены ошибки со звуками

Проведено тестирование — успешно

Выложена последняя версия на GitHub

#v(1em)
#text(weight: "bold", size: 14pt)[Обновления:]

Звук подбора аптечки с регулировкой громкости

Звуки выстрелов для второго босса

Звук перехода на вторую стадию
]

// ===== СЛАЙД 12: ДЕНЬ 6 =====
#slide[
#text(size: 16pt, weight: "bold")[День 6. Вторник 16.06]
#v(1em)

#text(weight: "bold", size: 14pt)[Задачи:]
#v(0.5em)

Тестирование каждой версии

Найти и добавить звуки для третьего босса

#v(1em)
#text(weight: "bold", size: 14pt)[Выполнение:]
#v(0.5em)

Найден и обрезан звук победы над боссами

Исправлен баг с прохождением сквозь босса

Протестирована версия с третьим боссом — ошибок нет

Изменён звук разрушения юнитов

Исправлен баг с диалогами (удалён show_next_popup())
]

// ===== СЛАЙД 13: ДЕНЬ 7 =====
#slide[
#text(size: 16pt, weight: "bold")[День 7. Среда 17.06]
#v(1em)

#text(weight: "bold", size: 14pt)[Задачи:]
#v(0.5em)

Обновить звуки

Заменить звук после первой стадии второго босса

Добавить звук победы над боссами

#v(1em)
#text(weight: "bold", size: 14pt)[Выполнение:]
#v(0.5em)

Добавлен звук победы над боссом

Исправлена опечатка: return Nones → return None

Увеличен порог громкости (макс. 3 вместо 1)

Увеличена громкость тихих звуков
]

// ===== СЛАЙД 14: ДЕНЬ 7 — КОД =====
#slide[
#text(size: 16pt, weight: "bold")[День 7. Константы громкости]
#v(1em)

#text(weight: "bold")[Создание констант:]

py
VOLUME_SHOOT = 0.2
VOLUME_MEDKIT = 3.0
VOLUME_SPAWN = 3.0
VOLUME_DARK = 0.2
VOLUME_BOOM = 0.5
VOLUME_DEAD_ASTEROID = 1.0
VOLUME_POWERUP = 1.0
VOLUME_TRANSFORM = 1.0
VOLUME_VICTORY_BOSS = 3.0
#v(0.5em)
#text(weight: "bold")[Функция установки громкости:]

py
def set_volumes():
    boom_sound.set_volume(VOLUME_BOOM * sfx_volume)
    shoot_sound.set_volume(VOLUME_SHOOT * sfx_volume)
    medkit_sound.set_volume(VOLUME_MEDKIT * sfx_volume)
    victory_boss_sound.set_volume(VOLUME_VICTORY_BOSS * sfx_volume)
]

// ===== СЛАЙД 15: ДЕНЬ 8 =====
#slide[
#text(size: 16pt, weight: "bold")[День 8. Четверг 18.06]
#v(1em)

#text(weight: "bold", size: 14pt)[Задачи:]
#v(0.5em)

Перенести звуки в новую версию

Доделать отчёт

Создать презентацию

#v(1em)
#text(weight: "bold", size: 14pt)[Выполнение:]
#v(0.5em)

Доработка отчёта

Создание многоуровневого списка

Работа над презентацией
]

// ===== СЛАЙД 16: ИТОГИ =====
#slide[
#text(size: 16pt, weight: "bold")[Итоги практики]
#v(1em)

#text(weight: "bold", size: 14pt)[Результаты:]
#v(0.5em)

Разработана игра "Космический корабль с астероидами"

Создано полное звуковое сопровождение:

Фоновая музыка

Звуки выстрелов и взрывов

Звуки бонусов и аптечки

Звуки боссов и победы

Реализована система регулировки громкости

Написаны спрайты: аптечка, ускорение, корабль

Исправлено множество ошибок в коде

Проект выложен на GitHub
]
