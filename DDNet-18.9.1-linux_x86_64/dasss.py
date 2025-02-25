import subprocess
import os
import platform
import time

def is_server_running(process_name):
    """Проверяет, запущен ли процесс с указанным именем."""
    if platform.system() == 'Windows':
        try:
            process = subprocess.check_output(['tasklist', '/FI', f'IMAGENAME eq {process_name}'], encoding='utf-8')
            return process_name in process
        except Exception:
            return False
    else: # Linux или macOS
        try:
            process = subprocess.check_output(['ps', '-A'], encoding='utf-8')
            return process_name in process
        except Exception:
            return False

def start_ddnet_server(server_path):
    """Запускает DDNet-сервер."""
    if not os.path.exists(server_path):
        print(f"Ошибка: Сервер не найден по пути: {server_path}")
        return

    # Проверка прав на выполнение
    if not os.access(server_path, os.X_OK):
        print(f"Ошибка: Нет прав на выполнение файла: {server_path}")
        print("Попытка установить права на выполнение...")
        try:
            subprocess.check_call(['chmod', '+x', server_path])
            print("Права на выполнение успешно установлены.")
        except subprocess.CalledProcessError as e:
            print(f"Не удалось установить права на выполнение: {e}")
            return

    print(f"Запускаю DDNet-сервер из: {server_path}...")
    try:
        if platform.system() == 'Windows':
           subprocess.Popen(server_path) #на винде не ждем завершения
        else:
            subprocess.Popen(server_path, preexec_fn=os.setsid)  # Запускаем в отдельном процессе на Linux/macOS
        print("DDNet-сервер успешно запущен")
    except Exception as e:
        print(f"Ошибка при запуске сервера: {e}")

def stop_ddnet_server(process_name):
    """Останавливает DDNet-сервер."""
    if not is_server_running(process_name):
        print("Сервер не запущен")
        return

    print("Останавливаю DDNet-сервер...")

    try:
        if platform.system() == 'Windows':
            subprocess.call(['taskkill', '/F', '/IM', process_name])
        else: # Linux or macOS
            subprocess.call(['pkill', process_name])
        print("DDNet-сервер успешно остановлен")
    except Exception as e:
        print(f"Ошибка при остановке сервера: {e}")


def main():
    downloads_path = os.path.join(os.path.expanduser("~"), "sukaaa")
    server_folder = os.path.join(downloads_path, "DDNet-18.7-linux_x86_64")
    server_executable_name = "DDNet-Server"  # Имя исполняемого файла
    if platform.system() == 'Windows':
        server_executable_name = "DDNet-Server.exe"
    server_path = os.path.join(server_folder, server_executable_name)


    if is_server_running(server_executable_name):
      print("Сервер уже запущен!")
      choice = input("Вы хотите остановить сервер? (y/n): ")
      if choice.lower() == 'y':
        stop_ddnet_server(server_executable_name)
    else:
      start_ddnet_server(server_path)
    while True:
      choice = input("Что вы хотите сделать? ('start', 'stop', 'exit'): ").lower()
      if choice == "start":
          if not is_server_running(server_executable_name):
            start_ddnet_server(server_path)
          else:
              print("Сервер уже запущен")
      elif choice == "stop":
        stop_ddnet_server(server_executable_name)
      elif choice == "exit":
          if is_server_running(server_executable_name):
            stop_ddnet_server(server_executable_name)
          break
      else:
          print("Некорректный ввод")
if __name__ == "__main__":
    main()
