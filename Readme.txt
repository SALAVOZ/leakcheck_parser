Парсер leakcheck с использованием библиотеки selenium.
Поддерживает только браузеры Google Chrome и Firefox.
После запуска скрипта пройти каптчу и когда появится dashboard страница, в консоли нажать Enter.
В качестве входного параметра принимается csv файл, в котором один столбец(первый) с электронными почтами. 
Файл должен лежать в одной директории со скриптом.
Для декодрайвера указывать путь
Если в консоли программа заедает, нажать Enter
options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Название csv файла. Пример, -f result.csv
  -e EMAILS, --emails EMAILS
                        Путь к csv файлу с электронным почтами
  -l LOGIN, --login LOGIN
                        Логин для leakcheck.
  -p PASSWORD, --password PASSWORD
                        Пароль для leakcheck. 
  -d DECODRIVER, --decodriver DECODRIVER
                        Путь к декодрайверу. Пока используется только firefox
  -b BROWSER, --browser BROWSER
                        Тип браузера. {firefox, chrome}

Пример запуска
python leakcheck_parser.py -f salavat.csv -e emails.csv -b chrome -d chromedriver.exe