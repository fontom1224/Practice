pygame фреймворк
(https://pythonist.ru/pygame-tutorial/?ysclid=mq63wafqwc424206911)

@startuml
title Логика игры "Asteroid Shooter"

start

:Запуск и загрузка;

while (Показ главного меню) is (true)
  :Главное меню;
  if (Выбор) is (Играть) then
    :Сброс игры + гид;
    while (Игра активна) is (true)
      :Ввод (движение, стрельба);
      :Обновление объектов;
      :Столкновения + спавн;
      :Отрисовка + подсказки;
      if (Жизни <= 0?) then
        break
      else
        :продолжить;
      endif
    endwhile
    :Выход в главное меню;
  elseif (Выбор) is (Сюжет) then
    :Показать сюжет;
    note right: возврат в меню
  elseif (Выбор) is (Настройки) then
    :Настройки;
    note right: возврат в меню
  else (Выход)
    stop
  endif
endwhile

stop
@enduml
