from sqlalchemy import inspect

from fit_track.models import WorkoutData


def test_fields(_app):
    inspector = inspect(WorkoutData)
    fields = [column.name for column in inspector.columns]
    print(fields)
    assert all(field in fields for field in ['date', 'exercise', 'weight', 'num_circles', 'num_reps', 'time']), (
        'В модели не найдены все необходимые поля. '
        'Проверьте модель: в ней должны быть поля id, date, exercise, num_circles, num_reps, time, weight.'
    )