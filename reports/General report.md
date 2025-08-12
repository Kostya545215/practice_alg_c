## Оглавление

- [Настройка Simulink для STM32](#настройка-simulink-для-stm32)
- [Написание С/С++ кода в simulink](#C/C++)
- [Real-time](#real-time)
- [Параметры инвертора взятые из data sheet](#Параметры-инвертора)
- [Настройка Eth. Передача данных по UPD](#Eth-udp)
- [Некоторые важные особенности](#interesting-facts)

### Настройка-Simulink-для-STM32

Для работы с stm32 через simulink необходимо устанавливать вспомогательную библиотеку stmicroelectronicsstm32f4discovery. Без лицензионного matlab невозможно устанавливать библиотеки через интерфейс matlab, поэтому придется скачивать их со [стороннего сайта](https://www.mathworks.com/matlabcentral/fileexchange/)
Если же при такой установке возникает ошибка Something Unexpected Occurred, можно попробовать следовать руководству из следующей [статьи](https://www.mathworks.com/matlabcentral/answers/489806-why-do-i-see-the-error-something-unexpected-occurred-when-installing-mathworks-products?s_tid=pi_suoe_uai_R2024a_win64#add_on_toolboxes)

После установки необходимого пакеты, нужно правильно настроить среду для работы.

- Выбор платы (HARDWARE -> HARDWARE Setings -> Hardware implementation -> Hardware Board)

- Выбор необходимого ioc файла (HARDWARE -> HARDWARE Setings -> Hardware implementation -> Hardware Board -> Hardware board setings -> target hardware resources -> build options -> STM32CubeMX project file(Browse) )

- Необходимо выбрать канал и порт UART для обмена данными между stm32 и компьютером ( HARDWARE -> HARDWARE Setings -> Hardware implementation -> Hardware Board -> Hardware board setings -> target hardware resources -> connectivity)

- Необходимо поставить галочки у visibility(static) в СubeMX project Manager -> Advanced Settings -> Generated Funcion Calls. (если галочки не кликабельны, то необходимо пересоздать проект, и при его создании отжать все галочки). 

### C/C++

В simulink можно использовать C/C++ код для тестов. Изначально нам необходимо иметь файл с c/c++ кодом и header файл. С помощью команды sltest.testmanager.view открываем Test Manager. Далее нажимаем New -> test fot c/c++ code. Ставим галочку integration testing. Выбираем файл с c++ кодом и header файл. Такой подход позволяет проводить изолированные тесты 
Если необходим блок, который будет исполняться в simulink модели, то можно использовать блок S-function Builder. При написании функции, необходимо соблюдать следующий синтаксис: в качестве входных аргументов необходимо указывать обычные параметры, а в качестве выходных указатели.
```
#include <simplecode.h>

void generation_sin(int a, int b, int* c, int* d)

{
    *c = a + b;

    *d = a - b;
}
```
### Real-time

Режим real-time необходим для проверки работы нашей модели в условиях, максимально приближенных к реальным. Real-time позволяет синхронизировать симуляцию системы с реальными тактами системы(8 кГц). Процесс исполняется с жёсткой частотой, и если модель не успевает за отведённое время, то возникать ошибка. 
С real-time возникла следующая проблема: для корректной симуляции модели на 8 кГц, необходим достаточно малый шаг решателя(порядка 1е-7). С таким sample time модель работает медленнее, чем идет реальное время - на расчеты на хватает мощности процесса ПК. Чтобы избежать этой проблемы, было принято замедлить модель в 1000 раз(такой порядок был выведен эмпирическим путем). Все процессы протекают таким же образом, только в 1000 раз медленнее. Для достижения такого эффекта была уменьшена частота шим сигнала и частота генерируемой синусоиды в 1000 раз ( с 8кГц до 8 Гц; с 50 Гц до 0.05 Гц), увеличены индуктивность и емкость нагрузки в 1000 раз(RLC нагрузка). 

### Eth-udp

При настройке в CubeMX подключения stm32 по ethernet, необходимо включать LVIP и прописывать статический адрес.

Настройка СubeMX - [Ethernet configuration for Simulink & Stm32](https://www.mathworks.com/help/ecoder/stmicroelectronicsstm32f4discovery/ug/ethernet-options.html)
!!Важно помнить, что при работе с ethernet необходимо использовать более старую версию CubeMX, которую поддерживают блоки Simulink. Ошибка возникает на уровне сборки. Ошибка вида "поменяете адрес буфера на 0х30040200". При смене адреса буфера ошибка не уходит. 
Нужно изначально создать проект в Hardware Implementation, а не использовать готовый. Тогда он по умолчанию будет создавать в старой версии. Главное на всплывающих окнах CubeMX нажимать Continue, а не Migrate. Тогда старая версия CubeMX будет сохраняться.

Отправка данных по udp через ethernet работает на частоте sample time.
### Параметры-инвертора

Параметры из data sheet:

Gate-Emitter threshold Voltage - Threshold voltage - (5+6.8)/2 = 5.9 V
Diode Forward Voltage - Forward Voltage diod - 1.7 V
Collector-Emitter Cut off Current - Off-state conductance - 1e-6 S
Module lead resistance - Drain-source on resistance - 0.8 mOhm

### Interesting-facts

- При составлении модели, которая впоследствии будет загружать на stm32, необходимо следить за тем, чтобы все блоки были дискретными и имели sample time
- Нельзя создавать несколько одинаковых блоков, ссылающихся на один и тот же пин stm32. (Например, нельзя создать 2 блока GPIOE1, и настроить логику так, чтобы в разное время отправлялся на него разный сигнал. Такой блок должен быть один,  а сигнал должен меняться, например, с помощью блока switch.)
- В CubeIDE можно работать с генерируемым simulink кодом для stm32, но важно не оставлять функцию main в main файле. Возникает конфликт. 
- simscape нельзя использовать для генерации кода для загрузки на stm32. решатели simscape оптимизированы для ПК и continuos time, а не для микроконтроллера. 
