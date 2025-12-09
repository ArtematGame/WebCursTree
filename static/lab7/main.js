function fillFilmList() {
    fetch(`/lab7/rest-api/films/`)
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        
        // Используем forEach вместо for, чтобы избежать проблем с замыканием
        films.forEach(function(film) {
            let tr = document.createElement('tr');

            let tdTitleRu = document.createElement('td');
            let tdTitleOrig = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            // Русское название
            tdTitleRu.innerText = film.title_ru;
            
            // Оригинальное название
            tdTitleOrig.innerText = film.title;
            tdTitleOrig.style.fontStyle = 'italic';
            tdTitleOrig.style.color = '#666';
            
            tdYear.innerText = film.year;

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            // Передаем реальный ID фильма из базы данных
            editButton.onclick = function() {
                editFilm(film.id);
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            // Передаем реальный ID фильма из базы данных
            delButton.onclick = function() {
                deleteFilm(film.id, film.title_ru);
            };

            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitleRu);
            tr.append(tdTitleOrig);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        });
    });
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function(response) {
            if (response.ok) {
                fillFilmList();
            } else {
                console.error('Ошибка при удалении:', response.status);
                alert('Ошибка при удалении фильма');
            }
        })
        .catch(function(error) {
            console.error('Ошибка:', error);
            alert('Ошибка при удалении фильма');
        });
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    document.getElementById('description-error').innerText = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };

    document.getElementById('description-error').innerText = '';

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if (resp.ok) {
            fillFilmList();
            hideModal();
            return {};    
        }
        return resp.json();
    })
    .then(function(data) {
        if (data && data.description) {
            document.getElementById('description-error').innerText = data.description;
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        alert('Ошибка при сохранении фильма');
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function(response) {
        if (!response.ok) {
            throw new Error('Фильм не найден');
        }
        return response.json();
    })
    .then(function(film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        document.getElementById('description-error').innerText = '';
        showModal();
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        alert('Не удалось загрузить данные фильма');
    });
}