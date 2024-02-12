"""
Модуль для построения графика КПВ (комбинированной производственной функции).
"""

import matplotlib.pyplot as plt


def plot_PPF(A1, B1, A2, B2, user_id, timestamp):
    """
    Строит график КПВ для двух производителей товаров А и Б.

    Args:
        A1 (float): Максимальный объем производства товара А для производителя 1.
        B1 (float): Максимальный объем производства товара Б для производителя 1.
        A2 (float): Максимальный объем производства товара А для производителя 2.
        B2 (float): Максимальный объем производства товара Б для производителя 2.
        user_id (int): Идентификатор пользователя.
        timestamp (int): Временная метка для имени файла.

    Returns:
        None
    """

    plt.clf()  # Очищаем текущий график перед построением нового

    # Определяем точки максимума производства по осям
    x_max = B1 + B2
    y_max = A1 + A2

    # Определяем отношения А/В для каждого производителя
    ratio_1 = A1 / B1
    ratio_2 = A2 / B2

    # Строим линии в зависимости от отношений
    if ratio_1 < ratio_2:
        plt.plot([0, B1], [y_max, A2], 'r--')  # Линия до точки перегиба
        plt.plot([B1, x_max], [A2, 0], 'r--')  # Линия до максимума по оси Х
        plt.fill([B1, 0, 0], [A2, A2, y_max], color='lightgray',
                 alpha=0.5)  # Треугольник для цеха 1
        plt.fill([B1, B1, x_max], [A2, 0, 0], color='lightblue',
                 alpha=0.5)  # Треугольник для цеха 2

    elif ratio_1 > ratio_2:
        plt.plot([0, B2], [y_max, A1], 'r--')  # Линия до точки перегиба
        plt.plot([B2, x_max], [A1, 0], 'r--')  # Линия до максимума по оси Х
        plt.fill([0, 0, B2], [y_max, A1, A1], color='lightgray',
                 alpha=0.5)  # Треугольник для цеха 2
        plt.fill([x_max, B2, B2], [0, 0, A1], color='lightblue',
                 alpha=0.5)  # Треугольник для цеха 1

    else:
        # Прямая линия без точки перегиба
        plt.plot([0, x_max], [y_max, 0], 'r--')
        plt.fill([0, 0, x_max], [y_max, 0, 0], color='lightgray',
                 alpha=0.5)  # Треугольник общий

    plt.xlabel('Товар А')
    plt.ylabel('Товар Б')
    plt.title('График КПВ')
    plt.grid(True)

    plt.savefig(f'handlers/problems/{user_id}_{timestamp}.png', dpi=300)
