from flask import Blueprint, render_template, request, jsonify, abort
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html') 

films = [
    {
        "title": "Intouchables",
        "title_ru": "1+1",
        "year": 2011,
        "description": "Пострадав в результате несчастного случая, богатый аристократ Филипп нанимает в помощники человека, \
            который менее всего подходит для этой работы, – молодого жителя предместья Дрисса, только что освободившегося из тюрьмы. \
            Несмотря на то, что Филипп прикован к инвалидному креслу, Дриссу удается привнести в размеренную жизнь аристократа дух приключений."
    },
    {
        "title": "The Gentlemen",
        "title_ru": "Джентльмены",
        "year": 2019,
        "description": "Один ушлый американец ещё со студенческих лет приторговывал наркотиками, а теперь придумал схему нелегального \
            обогащения с использованием поместий обедневшей английской аристократии и очень неплохо на этом разбогател. Другой пронырливый \
            журналист приходит к Рэю, правой руке американца, и предлагает тому купить киносценарий, в котором подробно описаны преступления \
            его босса при участии других представителей лондонского криминального мира — партнёра-еврея, китайской диаспоры, чернокожих \
            спортсменов и даже русского олигарха."
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": "Сотрудник страховой компании страдает хронической бессонницей и отчаянно пытается вырваться из мучительно скучной жизни. \
            Однажды в очередной командировке он встречает некоего Тайлера Дёрдена — харизматического торговца мылом с извращенной философией. Тайлер уверен, \
            что самосовершенствование — удел слабых, а единственное, ради чего стоит жить, — саморазрушение. Проходит немного времени, и вот уже новые друзья лупят друг \
            друга почем зря на стоянке перед баром, и очищающий мордобой доставляет им высшее блаженство. Приобщая других мужчин к простым радостям \
            физической жестокости, они основывают тайный Бойцовский клуб, который начинает пользоваться невероятной популярностью."
    }
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)  # Используем jsonify для корректного ответа

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    # Проверка на принадлежность ID корректному диапазону
    if id < 0 or id >= len(films):
        abort(404, description="Фильм не найден")
    return jsonify(films[id])  # Используем jsonify

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    # Проверка на принадлежность ID корректному диапазону
    if id < 0 or id >= len(films):
        abort(404, description="Фильм не найден")
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404, description="Фильм не найден")
    
    film = request.get_json()
    
    # Проверка русского названия
    if not film.get('title_ru'):
        return jsonify({'description': 'Заполните русское название'}), 400
    
    # Если оригинальное пустое - копируем русское
    if not film.get('title'):
        film['title'] = film['title_ru']
    
    # Проверка года
    if not film.get('year'):
        return jsonify({'description': 'Укажите год'}), 400
    
    try:
        year = int(film['year'])
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            return jsonify({'description': f'Год должен быть от 1895 до {current_year}'}), 400
    except ValueError:
        return jsonify({'description': 'Год должен быть числом'}), 400
    
    # Проверка описания (как было)
    if not film.get('description'):
        return jsonify({'description': 'Заполните описание'}), 400
    
    if len(film.get('description', '')) > 2000:
        return jsonify({'description': 'Описание должно быть не более 2000 символов'}), 400
    
    films[id] = film
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    # Проверка русского названия
    if not film.get('title_ru'):
        return jsonify({'description': 'Заполните русское название'}), 400
    
    # Если оригинальное пустое - копируем русское
    if not film.get('title'):
        film['title'] = film['title_ru']
    
    # Проверка года
    if not film.get('year'):
        return jsonify({'description': 'Укажите год'}), 400
    
    try:
        year = int(film['year'])
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            return jsonify({'description': f'Год должен быть от 1895 до {current_year}'}), 400
    except ValueError:
        return jsonify({'description': 'Год должен быть числом'}), 400
    
    # Проверка описания
    if not film.get('description'):
        return jsonify({'description': 'Заполните описание'}), 400
    
    if len(film.get('description', '')) > 2000:
        return jsonify({'description': 'Описание должно быть не более 2000 символов'}), 400
    
    films.append(film)
    return jsonify(len(films) - 1)

