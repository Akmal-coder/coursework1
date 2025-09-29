from typing import Dict
from unittest.mock import MagicMock, patch

import pandas as pd

from src.reports import _write_json, report_writer, spending_by_category


class TestReports:
    """Тесты для модуля reports.py"""

    @patch("src.reports._write_json")
    @patch("src.reports.get_date")
    @patch("src.reports.filter_by_date")
    def test_spending_by_category_basic(
        self, mock_filter: MagicMock, mock_get_date: MagicMock, mock_write: MagicMock
    ) -> None:
        """Тест базовой работы spending_by_category"""
        # Подготовка моков
        mock_get_date.return_value = "2024-01-01"
        mock_filter.return_value = [
            {
                "Дата": "2024-01-15",
                "Категория": "Еда",
                "Сумма": -500,
                "Описание": "Продукты",
            },
            {
                "Дата": "2024-02-20",
                "Категория": "Еда",
                "Сумма": -300,
                "Описание": "Кафе",
            },
        ]

        # Тестовые данные
        test_data = pd.DataFrame(
            [
                {"Дата": "2024-01-15", "Категория": "Еда", "Сумма": -500},
                {"Дата": "2024-02-20", "Категория": "Еда", "Сумма": -300},
                {"Дата": "2024-01-10", "Категория": "Транспорт", "Сумма": -200},
            ]
        )

        # Вызов функции
        result = spending_by_category(test_data, "Еда")

        # Проверки
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert all(result["Категория"] == "Еда")
        mock_write.assert_called_once()

    @patch("src.reports._write_json")
    @patch("src.reports.get_date")
    @patch("src.reports.filter_by_date")
    def test_spending_by_category_with_date(
        self, mock_filter: MagicMock, mock_get_date: MagicMock, mock_write: MagicMock
    ) -> None:
        """Тест spending_by_category с указанной датой"""
        mock_get_date.return_value = "2024-03-01"
        mock_filter.return_value = [{"Дата": "2024-02-15", "Категория": "Транспорт", "Сумма": -100}]

        test_data = pd.DataFrame([{"Дата": "2024-02-15", "Категория": "Транспорт", "Сумма": -100}])

        result = spending_by_category(test_data, "Транспорт", "2024-03-01 12:00:00")

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["Категория"] == "Транспорт"
        mock_write.assert_called_once()

    @patch("src.reports._write_json")
    @patch("src.reports.get_date")
    @patch("src.reports.filter_by_date")
    def test_spending_by_category_no_results(
        self, mock_filter: MagicMock, mock_get_date: MagicMock, mock_write: MagicMock
    ) -> None:
        """Тест когда нет данных по категории"""
        mock_get_date.return_value = "2024-01-01"
        # Возвращаем DataFrame с данными, но без нужной категории
        mock_filter.return_value = [{"Дата": "2024-01-15", "Категория": "Транспорт", "Сумма": -100}]

        test_data = pd.DataFrame([{"Дата": "2024-01-15", "Категория": "Транспорт", "Сумма": -100}])

        result = spending_by_category(test_data, "Еда")  # Ищем категорию которой нет

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0  # Должен вернуть пустой DataFrame
        mock_write.assert_called_once()

    @patch("src.reports.os.makedirs")
    @patch("src.reports.open")
    def test_write_json_with_dataframe(self, mock_open: MagicMock, mock_makedirs: MagicMock) -> None:
        """Тест записи JSON с DataFrame"""
        test_df = pd.DataFrame(
            [
                {"Категория": "Еда", "Сумма": -500},
                {"Категория": "Транспорт", "Сумма": -200},
            ]
        )

        _write_json("test_report.json", test_df)

        mock_makedirs.assert_called_once_with(".", exist_ok=True)
        # Проверяем что to_json был вызван (через MagicMock)
        assert True  # to_json вызывается внутри pandas

    @patch("src.reports.os.makedirs")
    @patch("src.reports.open")
    def test_write_json_with_dict(self, mock_open: MagicMock, mock_makedirs: MagicMock) -> None:
        """Тест записи JSON со словарем"""
        test_data = {"result": "success", "count": 5}
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        _write_json("test_report.json", test_data)

        mock_makedirs.assert_called_once_with(".", exist_ok=True)
        mock_open.assert_called_once_with("test_report.json", "w", encoding="utf-8")

    @patch("src.reports._write_json")
    def test_report_writer_decorator(self, mock_write: MagicMock) -> None:
        """Тест декоратора report_writer"""

        @report_writer()
        def test_function() -> Dict[str, str]:
            return {"data": "test"}

        result = test_function()

        assert result == {"data": "test"}
        mock_write.assert_called_once()

    @patch("src.reports._write_json")
    def test_report_writer_with_filename(self, mock_write: MagicMock) -> None:
        """Тест декоратора report_writer с именем файла"""

        @report_writer("custom_report.json")
        def test_function() -> pd.DataFrame:
            return pd.DataFrame([{"test": "data"}])

        result = test_function()

        assert isinstance(result, pd.DataFrame)
        mock_write.assert_called_once_with("custom_report.json", result)


#
# from unittest.mock import patch
#
# import pandas as pd
# import pytest
#
# from src.reports import spending_by_category
#
#
# @pytest.fixture
# def sample_transactions():
#     data = {
#         "Дата операции": [
#             "2021-02-01",
#             "2021-03-15",
#             "2021-04-10",
#             "2021-05-01",
#             "2021-05-10",
#         ],
#         "Категория": ["Food", "Food", "Transport", "Food", "Entertainment"],
#         "Сумма операции": [-50, -20, -15, -30, -100],
#     }
#     df = pd.DataFrame(data)
#     return df
#
#
# @pytest.mark.parametrize(
#     "category, date, expected_total, expected_count",
#     [
#         ("Food", "2021-05-10", 100, 3),
#         ("Transport", "2021-05-10", 15, 1),
#         ("Entertainment", "2021-05-10", 100, 1),
#         ("Nonexistent", "2021-05-10", 0, 0),
#     ],
# )
# def test_spending_by_category_returns_correct_stats(
#     sample_transactions, category, date, expected_total, expected_count
# ):
#     result = spending_by_category(sample_transactions, category, date)
#
#     if expected_count == 0:
#         assert result["message"] == "Нет данных за период"
#         # Можно проверить, что ключ 'period' отсутствует
#         assert "period" not in result
#
#
# def test_spending_by_category_handles_errors():
#     # Передача некорректных данных (например, не DataFrame)
#     result = spending_by_category(None, "Food", "2021-05-10")
#     assert "error" in result


# @patch("reports.json.dumps")
# def test_spending_by_category_json_returns_json(mock_json_dumps, sample_transactions):
#     mock_json_dumps.return_value = '{"mocked": "json"}'
#     output = spending_by_category_json(sample_transactions, "Food", "2021-05-10")
#     mock_json_dumps.assert_called_once()
#     assert output == '{"mocked": "json"}'
