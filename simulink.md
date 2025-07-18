### Switch block: express conditional statements 

3 input:
		-> if conditional is True
		-> conditional for the signal
		->  if cond is False

### Ramp

Пример работы: у нас есть функция sqrt, и она выглядит как $\sqrt{u}$. С настройкой 2 блок ramp подставляет $2t$ вместо $u$ и выходит $\sqrt{2t}$. 

### Переменные 

Можно передавать переменные, арифметические выражения вместо значений в функции в simulink, если они определены в workspace в matlab. 

Введение новой переменной: 
- Двойной клик по блоку
- В поле value справа троеточие 

Изменение существующей переменной:
- Modeling
- Model Explorer
### Сборка PIL блока

!! Сначала необходимо настроить все остальные параметры системы(в частности возникала ошибка с неверным портом USART, так как он был изменен после формирования PIL блока)

- Правый клик по Subsystem
- C/C++ code 
- Deploy this subsystem to Hardware