from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Класс для пагинации результатов.

    Атрибуты:
        page_size (int): Количество элементов на странице по умолчанию.
        page_size_query_param (str): Название параметра запроса для указания размера страницы.
        max_page_size (int): Максимально допустимое количество элементов на странице.
    """
    page_size = 10  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Позволяет клиенту указывать размер страницы
    max_page_size = 100  # Максимально допустимый размер страницы
