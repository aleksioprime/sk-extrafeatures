# Настроить доступ к файлу
# chmod u+x "devops/run_contestbot_mac.command"
# Отключить в настройках MacOS Ресивер AirPlay
source ~/venv/extrafeatures/bin/activate
# Установить в виртуальное окружение необходимые библиотеки
# pip3 install -r requirements.txt
export HOST=localhost
export PORT=5000
python3 ~/develop/extrafeatures/app.py