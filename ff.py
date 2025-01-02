import os
import random
import time
import platform

# Словник для збереження сніжинок (колонка: [рядок, символ, напрямок])
snowflakes = {}

try:
    # Windows Support
    from colorama import init
    init()
except ImportError:
    pass

def get_terminal_size():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return None
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)

    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])

columns, rows = get_terminal_size()

def clear_screen():
    if os.name == "posix":
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        os.system('cls')
    else:
        print('\n' * rows)

def get_random_flake():
    if not platform.system() == 'Windows':
        try:
            # python3 support
            try:
                cmd = unichr
            except NameError:
                cmd = chr

            flake = cmd(random.choice(range(0x2740, 0x2749)))

            return flake
        except:
            pass

    return " *"

def move_flake(col, direction):
    flake = snowflakes[col]
    current_row, symbol = flake

    # Стираємо сніжинку з поточного положення
    print(f"\033[{current_row};{col}H  ", end="")

    # Оновлюємо положення
    new_row = current_row + 1
    new_col = col + direction

    # Перевірка меж екрану
    if new_row >= rows:
        new_row = 1
        new_col = random.randint(1, columns - 1)
    if new_col < 1:
        new_col = 1
        direction *= -1
    if new_col >= columns:
        new_col = columns - 1
        direction *= -1

    # Зберігаємо нове положення
    snowflakes[col] = [new_row, symbol]

    # Малюємо сніжинку у новій позиції
    print(f"\033[{new_row};{new_col}H{symbol}", end="")
    print("\033[1;1H", end="")

    return direction

if __name__ == "__main__":
    clear_screen()

    direction = 1  # Початковий напрямок по діагоналі
    cycle_count = 0

    # Генеруємо початкові сніжинки
    for _ in range(columns // 2):  # Кількість сніжинок на екрані
        col = random.randint(1, columns - 1)
        snowflakes[col] = [1, get_random_flake()]

    while True:
        # Додаємо нові сніжинки з певною ймовірністю
        if random.random() < 0.2:  # Ймовірність появи нової сніжинки
            col = random.randint(1, columns - 1)
            if col not in snowflakes:
                snowflakes[col] = [1, get_random_flake()]

        # Переміщуємо кожну сніжинку
        for col in list(snowflakes.keys()):
            direction = move_flake(col, direction)

        time.sleep(0.1)

        # Зміна напрямку після 4 циклів
        cycle_count += 1
        if cycle_count >= 4:
            direction *= -1
            cycle_count = 0

