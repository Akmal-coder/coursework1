import pandas as pd

from src.reports import spending_by_category
from src.services import simple_search
from src.utils import read_transactions_xlsx
from src.views import main_page

data = read_transactions_xlsx("../data/operations.xlsx")
df = pd.DataFrame(data)

# Проверка работы модуля views
print(main_page("2021-10-30 15:12:30"))

# Проверка работы модуля reports
print(simple_search("Продукты", "../data/operations.xlsx"))


# Проверка работы модуля services
df = pd.DataFrame(read_transactions_xlsx("../data/operations.xlsx"))
print(spending_by_category(df, "Супермаркеты", "2021-10-30 15:12:30"))


# print(spending_by_category(df, "Переводы", "2021-09-12 16:15:15"))


# import pandas as pd
#
# from src.reports import spending_by_category, spending_by_category_json
# from src.services import analyze_cashback, analyze_cashback_json
# from src.views import main_paige
#
#
# def main_page():
#     """Главная функция приложения."""
#     try:
#         print("=" * 50)
#         print("ФИНАНСОВЫЙ АНАЛИЗАТОР")
#         print("=" * 50)
#
#         # 1. Основная информация (обычная и JSON версия)
#         print("\n1. ОСНОВНАЯ ИНФОРМАЦИЯ")
#         print("-" * 30)
#
#         print("Обычная версия:")
#         result_view = main_info("2019-04-10 15:30:00")
#         print(result_view)
#
#         print("\nJSON версия:")
#         result_view_json = main_info_json("2019-04-10 15:30:00")
#         print(result_view_json)
#
#         # 2. Анализ кэшбэка (обычная и JSON версия)
#         print("\n2. АНАЛИЗ КЭШБЭКА")
#         print("-" * 30)
#
#         print("Обычная версия:")
#         result_services = analyze_cashback("../data/operations.xlsx", 2018, 3)
#         print(result_services)
#
#         print("\nJSON версия:")
#         result_services_json = analyze_cashback_json("../data/operations.xlsx", 2018, 3)
#         print(result_services_json)
#
#         # 3. Анализ категорий (обычная и JSON версия)
#         print("\n3. АНАЛИЗ КАТЕГОРИЙ")
#         print("-" * 30)
#
#         df = pd.read_excel("../data/operations.xlsx", sheet_name="Отчет по операциям")
#
#         print("Обычная версия:")
#         result_reports = spending_by_category(df, "Ж/д билеты", "2019-04-10")
#         print(result_reports)
#
#         print("\nJSON версия:")
#         result_reports_json = spending_by_category_json(df, "Ж/д билеты", "2019-04-10")
#         print(result_reports_json)
#
#     except FileNotFoundError:
#         print("Ошибка: Файл operations.xlsx не найден")
#     except Exception as e:
#         print(f"Ошибка: {e}")


# if __name__ == "__main__":
#     # Запуск основной функции
#     main()
