#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    if sys.version_info.major != 3 or sys.version_info.minor < 8:
        raise Exception(
            "Python version should be >= 3.8"
            "-" * 10 +
            "Версия питона должна быть >= 3.8"
        )
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_votings.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
            "-" * 10 +
            "Нельзя импортировать Django. Вы уверены что он установлен и "
            "доступен в вашей переменной окружения PYTHONPATH? Не забыли "
            "ли вы активировать виртуальное окружение?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
