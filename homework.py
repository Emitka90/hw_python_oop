from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TEXT: str = ('Тип тренировки: {}; '
                 'Длительность: {:.3f} ч.; '
                 'Дистанция: {:.3f} км; '
                 'Ср. скорость: {:.3f} км/ч; '
                 'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.TEXT.format(self.training_type,
                                self.duration,
                                self.distance,
                                self.speed,
                                self.calories)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOUR_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / super().M_IN_KM
                * (self.duration * super().HOUR_IN_MIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    SM_IN_M: int = 100
    KOEFF_1: float = 0.035
    KOEFF_2: float = 0.029
    KM_IN_H_M_IN_S: float = 0.278

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int):
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        return ((self.KOEFF_1 * self.weight
                + ((self.get_mean_speed() * self.KM_IN_H_M_IN_S)**2
                   / (self.height / self.SM_IN_M))
                * self.KOEFF_2 * self.weight)
                * (self.duration * super().HOUR_IN_MIN))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    KOEFF_1: float = 1.1
    KOEFF_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP) / super().M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / super().M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.KOEFF_1)
                * self.KOEFF_2 * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in training_type:
        return training_type[workout_type](*data)
    else:
        Training(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = Training.show_training_info(training)
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages: list[tuple] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
