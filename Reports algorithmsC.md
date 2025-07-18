[simulink](all/simulink,md)

[cubemx](all/CubeMX.md)

Настройка Simulink для работы через него с Stm32

 - Выбор платы (HARDWARE -> HARDWARE Setings -> Hardware implementation -> Hardware Board)
- Выбор необходимого ioc файла (HARDWARE -> HARDWARE Setings -> Hardware implementation -> Hardware Board -> Hardware board setings -> target hardware resources -> build options -> STM32CubeMX project file(Browse) )
- При работе с UART необходимо выбрать канал и порт ( HARDWARE -> HARDWARE Setings -> Hardware implementation -> Hardware Board -> Hardware board setings -> target hardware resources -> connectivity)
- При работе с ШИМ необходимо выставить continous time ( HARDWARE -> HARDWARE Setings -> Code Generation -> Interface  -> software enviromment)

### Ошибка visibility(static) 

Если галочки у visibility(static) в СubeMX project Manager -> Advanced Settings -> Generated Funcion Calls не кликабельны, то нужно пересоздать проект, и при создании проекта отжать все галочки. 

### Концепция PIL

Мы строим модель реальной системы в Simulink. Производим имитацию физических данных для микроконтроллера через Simulink. Контроллер не знает, что данные получены из эмуляции - для него данные выглядят как реальные физические сигналы. Контроллер отрабатывает заданный алгоритм, получая данные через Simulink. 

!! Требуется точная настройка таймингов(эмуляция может работать быстрее/медленнее реальной модели)

HIL - тестирование с реальными датчиками/ MIL - все на ПК.
