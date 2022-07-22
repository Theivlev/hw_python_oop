from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    messag_trainig: str = ('Тип тренировки: {training_type}; '
                           'Длительность: {duration:.3f} ч.; '
                           'Дистанция: {distance:.3f} км; '
                           'Ср. скорость: {speed:.3f} км/ч; '
                           'Потрачено ккал: {calories:.3f}.'
                           )

    def get_message(self) -> str:
        return self.messag_trainig.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('метод get_spent_calories нуждается'
                                  'в переопределении')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    COEF_FOR_CALC_CALORIES_RUN_1: int = 18
    COEF_FOR_CALC_CALORIES_RUN_2: int = 20
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        return ((self.COEF_FOR_CALC_CALORIES_RUN_1 * self.get_mean_speed()
                - self.COEF_FOR_CALC_CALORIES_RUN_2) * self.weight_kg
                / self.M_IN_KM * self.duration_h * self.M_IN_HOUR)


class SportsWalking(Training):
    COEF_FOR_CALC_CALORIES_WLK_1: float = 0.035
    COEF_FOR_CALC_CALORIES_WLK_2: float = 0.029
    COEF_FOR_CALC_CALORIES_WLK_3: int = 2
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEF_FOR_CALC_CALORIES_WLK_1 * self.weight_kg
                + (self.get_mean_speed() ** self.COEF_FOR_CALC_CALORIES_WLK_3)
                // self.height * self.weight_kg
                * self.COEF_FOR_CALC_CALORIES_WLK_2)
                * self.duration_h * self.M_IN_HOUR)


class Swimming(Training):
    LEN_STEP: float = 1.38
    COEF_FOR_CALC_CALORIES_SWIM_1: float = 1.1
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration_h)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.COEF_FOR_CALC_CALORIES_SWIM_1) * 2 * self.weight_kg)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_type: dict = {'SWM': Swimming,
                        'RUN': Running,
                        'WLK': SportsWalking,
                        }
    if workout_type not in train_type:
        raise TypeError('Неизвестный тип тренировки')
    else:
        return train_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
