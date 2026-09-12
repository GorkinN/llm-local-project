"""
Модуль для парсинга CSV файлов.
Предоставляет функции для чтения, проверки и извлечения данных из CSV.
"""

import csv
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set


def read_csv(
    filepath: str,
    delimiter: str = ',',
    has_header: bool = True,
    encoding: str = 'utf-8',
) -> List[Dict[str, str]]:
    """
    Читайте CSV файл и возвращите список словарей.

    Args:
        filepath: Путь к CSV файлу.
        delimiter: Символ разделителя по умолчанию ','.
        has_header: Если True, первая строка считается заголовком.
        encoding: Кодировка файла по умолчанию 'utf-8'.

    Returns:
        Список словарей с данными из CSV.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если в пути к файлу есть ошибки.
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {filepath}")

    data = []

    with open(path, 'r', encoding=encoding, newline='') as f:
        csv_reader = csv.DictReader(f, delimiter=delimiter)

        for row in csv_reader:
            if has_header and row.get('') is None:  # Первая строка с заголовками
                continue
            data.append(dict(row))

    return data


def clean_csv_data(
    data: List[Dict[str, str]],
    empty_value: Optional[str] = '',
    strip_whitespace: bool = True,
) -> List[Dict[str, Any]]:
    """
    Очистите данные из CSV и примените преобразования типов.

    Args:
        data: Список словарей с данными.
        empty_value: Значение по умолчанию для пустых ячеек.
        strip_whitespace: Удаляет лишние пробелы вокруг значений.

    Returns:
        Очищенные данные с значениями, преобразованными к типам данных (по возможности).
    """
    cleaned_data = []

    for row in data:
        cleaned_row = {}

        for key, value in row.items():
            if strip_whitespace and value is not None:
                value = value.strip()

        cleaned_row = {key: _convert_value(val=empty_value, value=val) 
                      for key, val in row.items()}

        cleaned_data.append(cleaned_row)

    return cleaned_data


def _convert_value(val: Optional[str], empty_value: str = '') -> Any:
    """
    Превратите строковое значение в соответствующий тип данных.

    Args:
        empty_value: Значение по умолчанию для пустых полей.
        value: Строковое значение из CSV.

    Returns:
        Преобразованное значение (None, int, float или str).
    """
    if val is None or val == '':
        return empty_value

    # Попытайся преобразовать в число
    if not val.startswith('NaN'):  # Исключи NaN
        try:
            if '.' in val and 'e' not in val.lower():
                return float(val)
            return int(val)
        except ValueError:
            pass

    return str(val)


def read_and_clean_csv(
    filepath: str,
    delimiter: str = ',',
    has_header: bool = True,
    encoding: str = 'utf-8',
    empty_value: Optional[str] = '',
    strip_whitespace: bool = True,
) -> List[Dict[str, Any]]:
    """
    Сочетите чтение и очистку данных CSV в одной операции.

    Args:
        filepath: Путь к CSV файлу.
        delimiter: Символ разделителя по умолчанию ','.
        has_header: Если True, первая строка считается заголовком.
        encoding: Кодировка файла по умолчанию 'utf-8'.
        empty_value: Значение по умолчанию для пустых ячеек.
        strip_whitespace: Удаляет лишние пробелы вокруг значений.

    Returns:
        Очищенные данные с предсказанными типами данных.
    """
    data = read_csv(
        filepath=filepath,
        delimiter=delimiter,
        has_header=has_header,
        encoding=encoding,
    )
    return clean_csv_data(
        data=data,
        empty_value=empty_value if empty_value is not None else '',
        strip_whitespace=strip_whitespace,
    )


def get_column_names(filepath: str, delimiter: str = ',', encoding: str = 'utf-8') -> List[str]:
    """
    Возвращает список имен столбцов из CSV файла.

    Args:
        filepath: Путь к CSV файлу.
        delimiter: Символ разделителя по умолчанию ','.
        encoding: Кодировка файла по умолчанию 'utf-8'.

    Returns:
        Список строк с именами столбцов.
    """
    with open(filepath, 'r', encoding=encoding, newline='') as f:
        reader = csv.reader(f, delimiter=delimiter)
        return next(reader)


def filter_by_column(
    data: List[Dict[str, str]],
    column: str,
    value: Any,
    exact_match: bool = True,
    case_sensitive: bool = False,
) -> List[Dict[str, str]]:
    """
    Фильтруйте данные по значению столбца.

    Args:
        data: Список словарей с данными.
        column: Имя столбца для фильтрации.
        value: Значение для поиска.
        exact_match: Если True, точное совпадение значения.
        case_sensitive: Если True, поиск не чувствителен к регистру.

    Returns:
        Отфильтрованные данные.
    """
    filtered = []

    for row in data:
        row_value = row.get(column, '')
        target_value = str(value) if value is not None else ''

        if exact_match and case_sensitive:
            if row_value == target_value:
                filtered.append(row)
        elif exact_match and not case_sensitive:
            if row_value.lower() == target_value.lower():
                filtered.append(row)
        else:
            filtered.append(row)

    return filtered


def find_duplicates(data: List[Dict[str, str]]) -> List[Set]:
    """
    Найти все наборы повторяющихся строк (по всем ключам).

    Args:
        data: Список словарей с данными.

    Returns:
        Список наборов ключей для повторяющихся строк.
    """
    dupes = []
    seen = {}

    for row in data:
        row_tuple = tuple(sorted(row.items()))

        if row_tuple in seen:
            dupes.append(seen[row_tuple])
        else:
            seen[row_tuple] = row

    # Удалите дубликаты из самих данных
    dupes_set = set(frozenset(tuple(sorted(row.items()))) for row in data 
                    if tuple(sorted(row.items())) in seen)


def read_json_to_csv(filepath_json: str, csv_output: str) -> Dict[str, List]:
    """
    Читайте JSON и записываете данные в CSV.

    Args:
        filepath_json: Путь к JSON файлу.
        csv_output: Путь к выходному CSV файлу.

    Raises:
        ValueError: Если входные данные не действительны.
    """
    import json

    with open(filepath_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, list):
        # Список словарей или список списков
        if data and isinstance(data[0], dict):
            column_names = list(data[0].keys())
            with open(csv_output, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(column_names)

                for row in data:
                    if isinstance(row, dict):
                        row_dict = row if column_names else {}
                        row_list = [row_dict.get(name, '') for name in column_names]
                        writer.writerow(row_list)
        elif data and isinstance(data[0], list):
            # Трансформируйте список списков в словарный формат
            pass

    elif isinstance(data, dict):
        # Один словарь — создайте CSV с одним рядом
        with open(csv_output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(list(data.keys()))
            writer.writerow([str(v) for v in data.values()])

    return None


if __name__ == '__main__':
    # Пример использования
    print("Модуль CSV-парсера")
    print("Функции: read_csv, clean_csv_data, get_column_names и т. д.")
