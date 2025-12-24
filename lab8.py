from flask import Blueprint, render_template, request, redirect, abort
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import or_

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    # Проверяем авторизацию через Flask-Login
    login = current_user.login if current_user.is_authenticated else None
    return render_template('lab8/lab8.html', login=login)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на пустые значения
    if not login_form:
        return render_template('lab8/register.html',
                               error='Логин не может быть пустым')
    
    if not password_form:
        return render_template('lab8/register.html',
                               error='Пароль не может быть пустым')

    # Поиск пользователя через
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    # Автоматический логин после регистрации
    login_user(new_user, remember=False)
    return redirect('/lab8/')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    # Галочка "запомнить меня"
    remember_me = request.form.get('remember_me')
    
    # Проверка на пустые значения
    if not login_form:
        return render_template('lab8/login.html',
                               error='Логин не может быть пустым')
    
    if not password_form:
        return render_template('lab8/login.html',
                               error='Пароль не может быть пустым')

    user = users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        # remember=True если установлена галочка
        remember = remember_me == 'on'
        login_user(user, remember=remember)
        return redirect('/lab8/')
        
    return render_template('lab8/login.html',
                           error='Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/public/')
def public_articles():
    search = request.args.get('search', '').strip() 
    
    base_query = articles.query.filter_by(is_public=True)
    
    if search:
        search_filter = or_(
            articles.title.ilike(f'%{search}%'),
            articles.article_text.ilike(f'%{search}%')
        )
        public_articles_list = base_query.filter(search_filter).all()
    else:
        public_articles_list = base_query.all()
    
    return render_template('lab8/public.html', 
                          articles=public_articles_list, 
                          search=search)

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    search = request.args.get('search', '').strip()
    
    base_query = articles.query.filter_by(login_id=current_user.id)
    
    if search:
        search_filter = or_(
            articles.title.ilike(f'%{search}%'),
            articles.article_text.ilike(f'%{search}%')
        )
        user_articles = base_query.filter(search_filter).all()
    else:
        user_articles = base_query.all()
    
    return render_template('lab8/articles.html', 
                          articles=user_articles, 
                          search=search) 


@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = True if request.form.get('is_public') else False
    
    if not title:
        return render_template('lab8/create.html',
                               error='Заголовок не может быть пустым')
    
    if not article_text:
        return render_template('lab8/create.html',
                               error='Текст статьи не может быть пустым')
    
    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=False,
        is_public=True,
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles/')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    # Проверяем, принадлежит ли статья текущему пользователю
    if article.login_id != current_user.id:
        abort(403)  # Запрещено
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    
    if not title:
        return render_template('lab8/edit.html', article=article,
                               error='Заголовок не может быть пустым')
    
    if not article_text:
        return render_template('lab8/edit.html', article=article,
                               error='Текст статьи не может быть пустым')
    
    # Обновление статьи через ORM
    article.title = title
    article.article_text = article_text
    
    db.session.commit()
    
    return redirect('/lab8/articles/')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):

    article = articles.query.get_or_404(article_id)
    
    # Проверяем, принадлежит ли статья текущему пользователю
    if article.login_id != current_user.id:
        abort(403)  # Запрещено
    
    db.session.delete(article)
    db.session.commit()
    
    return redirect('/lab8/articles/')

@lab8.route('/lab8/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

