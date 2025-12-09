function fillFilmList() {
    fetch(`/lab7/rest-api/films/`)
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitleRu = document.createElement('td');  // Русское название
            let tdTitleOrig = document.createElement('td');  // Оригинальное название
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            // ПЕРВЫЙ столбец: русское название
            tdTitleRu.innerText = films[i].title_ru;
            
            // ВТОРОЙ столбец: оригинальное название
            // Всегда показываем оригинальное название, даже если оно совпадает с русским
            tdTitleOrig.innerText = films[i].title;
            
            // Добавляем стиль курсива и серый цвет
            tdTitleOrig.style.fontStyle = 'italic';
            tdTitleOrig.style.color = '#666';
            
            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.onclick = function() {
                editFilm(i);
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(i, films[i].title_ru);
            };

            tdActions.append(editButton);
            tdActions.append(delButton);  

            // Порядок: русское, оригинальное, год, действия
            tr.append(tdTitleRu);     // Русское название ПЕРВЫМ
            tr.append(tdTitleOrig);   // Оригинальное название ВТОРЫМ
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    })
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function () {
            fillFilmList();
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
    // Очищаем ошибку при открытии модального окна
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
    }

    // Очищаем ошибку перед отправкой
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
    .then(function (errors) {
        if(errors.description)
            document.getElementById('description-error').innerText = errors.description;
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return  data.json();
    })
    .then(function (film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        // Очищаем ошибку при открытии модального окна для редактирования
        document.getElementById('description-error').innerText = '';
        showModal();
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return  data.json();
    })
    .then(function (film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    });
}
