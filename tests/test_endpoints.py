import pytest

from fit_track.models import WorkoutData


def test_get_all(client):
    got = client.get('/')

    assert got.status_code == 200, (
        'При переходе на главну страницу статус-код должен быть 200'
    )
    assert 'Дата' in got.data.decode(), (
        'Добавьте столбец с названием "Дата" в контекст страницы с помощью тегов <tr>, <th> в index.html.'
    )
    assert 'Упражнение' in got.data.decode(), (
        'Добавьте столбец с названием "Упражнение" в контекст страницы с помощью тегов <tr>, <th> в index.html.'
    )
    assert 'Вес' in got.data.decode(), (
        'Добавьте столбец с названием "Вес" в контекст страницы с помощью тегов <tr>, <th> в index.html.'
    )
    assert 'Количество кругов' in got.data.decode(), (
        'Добавьте столбец с названием "Количество кругов" в контекст страницы с помощью тегов <tr>, <th> в index.html.'
    )
    assert 'Количество повторов' in got.data.decode(), (
        'Добавьте столбец с названием "Количество повторов" в контекст страницы с помощью тегов <tr>, <th> в index.html.'
    )
    assert 'Время выполнения' in got.data.decode(), (
        'Добавьте столбец с названием "Время выполнения" в контекст страницы с помощью тегов <tr>, <th> в index.html.'
    )

@pytest.mark.add
def test_index_form_get(client):
    got = client.get('/add')
    assert got.status_code == 200, (
        'GET-запрос к странице c адресом /add должен возвращать статус `200`.'
    )
    assert b'form' in got.data, (
        'Добавьте форму в шаблон страницы `add_form`'
    )


@pytest.mark.err
def test_404_form_get(client):
    got = client.get('/adds')
    assert got.status_code == 404, (
        'GET-запрос к странице c адресом /add должен возвращать статус `200`.'
    )
    print(got.data.decode())
    assert 'Упс, ничего не найдено' in got.data.decode(), (
        'Добавьте кастомный обработчик ошибок  с шаблоном 404.html, '
        'который будет выводить сообщение "Упс, ничего не найдено".'
    )
    assert 'href="/">Вернуться на главную' in got.data.decode(), (
        'Добавьте в шаблон 404.html ссылку на главную страницу в виде строки: "Вернуться на главную".'
    )


@pytest.mark.add
@pytest.mark.parametrize('json_data', [
    ({'date': '2023-10-28', 'exercise': 'pull ups', 'weight': 10, 'num_circles': 0, 'num_reps': 100, 'time': '00:15:12'}),
    ({'date': '2023-10-27', 'exercise': 'pull ups', 'weight': 11, 'num_circles': 0, 'num_reps': 150, 'time': '00:15:12'}),
    ({'date': '2023-10-29', 'exercise': 'pull ups', 'weight': 13, 'num_circles': 0, 'num_reps': 200, 'time': '00:15:12'}),
    ({})
])
def test_post_add(json_data, client):
    got = client.post('/add', json=json_data)
    assert got.status_code == 200, (
        'При успешной обработке данных возвращайте, в данном случае, код ответа 200'
    )
    work = WorkoutData.query.filter_by(date='2023-10-28').first()
    assert not work, (
        'После отправки формы должно происходить сохранение в базу данных.'
        ' Если значения равные 0 не пропускает валидация формы: '
        'используйте InputRequired в параметрах валидации при определении формы WorkoutForm.'
    )


@pytest.mark.add
@pytest.mark.parametrize('json_data', [
    ({'date': '', 'exercise': 'pull ups', 'weight': 10, 'num_circles': 0, 'num_reps': 100, 'time': '00:15:12'}),
    ({'date': '2023-10-27', 'exercise': '', 'weight': 11, 'num_circles': 0, 'num_reps': 150, 'time': '00:15:12'}),
    ({'date': '2023-10-29', 'exercise': 'pull ups', 'weight': '', 'num_circles': 0, 'num_reps': 200, 'time': '00:15:12'}),
    ({'date': '2023-10-29', 'exercise': 'pull ups', 'weight': 13, 'num_circles': '', 'num_reps': 200, 'time': '00:15:12'}),
    ({'date': '2023-10-29', 'exercise': 'pull ups', 'weight': 13, 'num_circles': 0, 'num_reps': '', 'time': '00:15:12'}),
])
def test_post_none_add(json_data, client):
    got = client.post('/add', json=json_data)
    assert 'Обязательное поле' in got.data.decode(), (
        'При недопустимой отправке пустых значений должно выводится сообщение: "Обязательное поле". '
        'Добавьте этот вывод уведомления с помощью шаблонизатора в add_form.html,'
        ' предварительно определив его в параметре message валидатора поля в WorkoutForm'
    )


@pytest.mark.add
@pytest.mark.parametrize('json_data', [
    ({'date': '2023-10-29', 'exercise': 'burpee', 'weight': 13, 'num_circles': 0, 'num_reps': 200}),
])
def test_post_default_time(json_data, client):
    client.post('/add', json=json_data)
    work = WorkoutData.query.filter_by(exercise='burpee').first()
    assert not work, (
        'Поле time формы  WorkoutForm должно содержать значение по умолчанию.'
        ' Добавьте его при определении в WorkoutForm с помощью параметра default.'
    )


@pytest.mark.add
@pytest.mark.parametrize('json_data', [
    ({'date': '2023-10-29', 'exercise': 'pull ups', 'weight': -50, 'num_circles': 0, 'num_reps': 200, 'time': '00:15:12'}),
    ({'date': '2023-10-29', 'exercise': 'pull ups', 'weight': 50, 'num_circles': -2, 'num_reps': 200, 'time': '00:15:12'}),
    ({'date': '2023-10-29', 'exercise': 'pull ups', 'weight': 50, 'num_circles': 0, 'num_reps': -1, 'time': '00:15:12'}),
])
def test_post_none_add(json_data, client):
    got = client.post('/add', json=json_data)
    assert 'Число должно быть положительным' in got.data.decode(), (
        'При отправке отрацательных знчений в полях форм: weight, num_circles, num_reps должно выводится сообщение: '
        '"Число должно быть положительным". Добавьте этот вывод уведомления с помощью кастомного валидатора validate_positive_number '
        'и добавьте его в список параматра validators при опредления поля в WorkoutForm '
    )


@pytest.mark.add
@pytest.mark.parametrize('json_data', [
    ({'date': 'дддддд', 'exercise': 'pull ups', 'weight': 50, 'num_circles': 0, 'num_reps': 200, 'time': '00:15:12'}),
])
def test_post_inval_add(json_data, client):
    got = client.post('/add', json=json_data)
    assert 'Not a valid date' in got.data.decode(), (
        'При отправке невалидных знчениния в поле формы date должно выводится сообщение: '
        '"Невалидное значение". Добавьте этот вывод уведомления с помощью шаблонизатора в add_form.html, '
        'предварительно определив его в параметре message валидатора поля в WorkoutForm'
    )


@pytest.mark.add
@pytest.mark.parametrize('json_data', [
    ({'date': '2023-10-29', 'exercise': 'pull ups', 'weight': 50, 'num_circles': 2, 'num_reps': 200, 'time': 'ывывыы'}),
])
def test_post_inval_time_add(json_data, client):
    got = client.post('/add', json=json_data)
    assert 'Not a valid time' in got.data.decode(), (
        'При отправке невалидных знчениния в поле формы time должно выводится сообщение: '
        '"Невалидное значение". Добавьте этот вывод уведомления с помощью шаблонизатора в add_form.html, '
        'предварительно определив его в параметре message валидатора поля в WorkoutForm'
    )