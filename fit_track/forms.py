
def validate_positive_number(form, field):
    # эта функция будет использоваться как валидатор для
    # положительных чисел используя field.data для получения значения
    # возвращайте raise ValidationError с сообщением в параметрах в случае ошибки
    # используйте этот валидатор как аргумент для параметра validators в форме


class WorkoutForm():
    # Опишите здесь поля формы, согласно заданию
    # Не забудьте правильно унаследовать этот класс
    # Используйте валидатор InputRequired
    # Для изменения отображения в форме формата времени используйте параметр format="%H:%M:%S"
