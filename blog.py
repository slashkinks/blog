from flask import request, url_for, redirect, render_template, session, jsonify
from models import *
from hashlib import md5
import os
import json
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import join
# В менеджере файлов добавить возможности по манипуляции файлами.


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads/blog/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'gif', 'jpg', 'png', 'jpeg', 'bmp'}


# ###################URL-ADMIN######################
@app.route('/admin/main')
def admin_main():
    if 'username' not in session:
        return redirect("/login", code=302)
    else:
        #return render_template("admin/main_admin.html")
        return redirect("/admin/posts", code=302)


#@app.route('/admin/<path:argument>')
@app.route('/admin/posts')
def admin_posts():
    if 'username' not in session:
        return redirect("/login", code=302)
    else:
        posts = Post.query.all()
        return render_template("admin/posts_admin.html", posts=posts, delete_message=request.args.get('delete_message'), 
            publicate_message=request.args.get('publicate_message'), unpublicate_message=request.args.get('unpublicate_message'))


# Переход на страницу создания нового поста
@app.route('/admin/new_post')
def admin_new_post():
    if 'username' not in session:
        return redirect("/login", code=302)
    else:
        directory = os.path.join(APP_ROOT, 'static/uploads/blog/')
        dirs = []
        files = []
        tags = Tag.query.all()
        for dirname, dirnames, filenames in os.walk(directory):
            dirs.append(dirname)
            for subdirname in dirnames:
                dirs.append(os.path.join(dirname, subdirname))
            for filename in filenames:
                size = ((int(os.path.getsize(os.path.join(directory, filename)))) / 1024) / 1024
                size = round(size, 2)
                files.append([filename, size])
        return render_template("admin/new_post_admin.html", files=files, tags=tags)


@app.route('/admin/file_manager')
def file_manager():
    if 'username' not in session:
        return redirect("/login", code=302)
    else:
        directory = os.path.join(APP_ROOT, 'static/uploads/blog/')
        filess = os.listdir(directory)
        dirs = []
        files = []
        i = 0
        for dirname, dirnames, filenames in os.walk(directory):
            dirs.append(dirname)

            for subdirname in dirnames:
                dirs.append(os.path.join(dirname, subdirname))

            for filename in filenames:
                size = ((int(os.path.getsize(os.path.join(directory, filename)))) / 1024) / 1024
                size = round(size, 2)
                files.append([filename, size])
        return render_template("admin/file_manager_admin.html", files=files, file_name=request.args.get('file_name'))


# Редактирование  поста
@app.route('/admin/edit/<int:id>')
def edit_post(id):
    if 'username' not in session:
        return redirect("/login", code=302)
    else:
        post = Post.query.filter_by(id=id).first()
        tags = Tag.query.all()
        directory = os.path.join(APP_ROOT, 'static/uploads/blog/')
        dirs = []
        files = []
        for dirname, dirnames, filenames in os.walk(directory):
            dirs.append(dirname)
            for subdirname in dirnames:
                dirs.append(os.path.join(dirname, subdirname))
            for filename in filenames:
                size = ((int(os.path.getsize(os.path.join(directory, filename)))) / 1024) / 1024
                size = round(size, 2)
                files.append([filename, size])
        return render_template("admin/edit_post_admin.html", post=post, files=files, tags=tags)
# ###################URL-ADMIN######################


# ###################URL-MAIN#######################
# Загрузка главной страницы блога
@app.route('/')
@app.route('/main')  # @app.route('/main/<int:page>', methods=['GET', 'POST'])
def main_page_load():
    posts = Post.query.filter_by(published=True).all()

    for post in posts:
        post.body = Post.make_description(post.body)

    check = check_login()
    return render_template("main.html", posts=posts, check=check)


# Загрузка страницы со всеми тегами/вывод всех постов отсортированных по категориям
@app.route('/tags')
def tags_page_load():
    posts = Post.query.filter_by(published=True).all()
    tags_list = Tag.query.join(tags).all()
    only_published_posts = []

    for tag in tags_list:
        for post in tag.post:
            if post.published == True:
                if tag not in only_published_posts:
                    only_published_posts.append(tag)
            else:
                tag.post.remove(post)
           
    check = check_login()
    return render_template('tags.html', posts=posts, tags=only_published_posts, check=check)


# Загрузка страницы логинизации
@app.route('/login')
def login_page_load():
    if 'username' in session:
        return redirect("/main", code=302)
    return render_template('login.html')


# Отображение записей по категориям
@app.route('/tag/<tag>')
def tag_page_load(tag):
    posts = Post.query.filter_by(published=True).all()
    tag_posts = []
    for post in posts:
        post.body = Post.make_description(post.body)
        for needed_tag in post.tags:
            if tag in needed_tag.tag_name:
                tag_posts.append(post)

    check = check_login()
    return render_template("main.html", title='Home', posts=tag_posts, check=check)


# Загрузка отдельного поста
@app.route('/post/<int:id>')
def post_page_load(id):
    post = Post.query.filter_by(id=id, published=True).first()
    check = check_login()
    return render_template('post_page.html', post=post, check=check)
# ###################URL-MAIN#######################


# ###################Функционал-ADMIN###################
# Изменение поста
@app.route('/apply_changes', methods=['POST'])
def apply_changes():
    if 'username' not in session:
        return redirect("/login", code=302)
    else:
        index = request.form['id']
        title = request.form['title']
        text = request.form['text']
        tags = request.form['tags']
        last_edit_date = datetime.utcnow()

        tags_splited = tags.split(',')
        new_tags = []
        tag_names = []
        tags = Tag.query.all()  
        
        for tag in tags:
            tag_names.append(tag.tag_name)

        # Добавление нового тега в справочник в базе
        for tag in tags_splited:
            if tag not in tag_names:
                new_tags.append(tag)  
                new_tag = Tag(tag)
                db.session.add(new_tag)
                db.session.commit()

        # Теги поста, без повторяющихся
        all_post_tags = []
        for tag in tags_splited:
            if tag not in all_post_tags:
                all_post_tags.append(tag)

        #print("all_post_tags1:")
        #print(all_post_tags)



        default_tag_names = []
        post_x = Post.query.filter_by(id=index).first()
        #print("query2.0:")
        #print(post_x.tags)
        for needed_tag in post_x.tags:
            default_tag_names.append(needed_tag.tag_name)

        #print("default_tag_names2:")
        #print(default_tag_names)

        complete_tags_names = []
        for tag in all_post_tags:
            if tag not in default_tag_names:
                complete_tags_names.append(tag)

        #print("complete_tags_names3:")
        #print(complete_tags_names)

        tags_id = []
        for tag in complete_tags_names:
            tags_id.append(Tag.query.filter(Tag.tag_name == tag).first())


        post = Post.query.filter_by(id = index)
        post=post.first()
      
        post.tags.extend(tags_id)
        db.session.add(post)
        db.session.commit()

        Post.query.filter_by(id = index).update({'title': title, 'body': text, 'last_edit_date': last_edit_date})
        db.session.commit()
        return jsonify(1)


# Удаление поста
@app.route('/delete_post', methods=['POST'])
def delete_post():
    if 'username' not in session:
        return redirect("/login", code=302)
    else:
        id=request.form['postid']
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
        posts = Post.query.all()
        return redirect(url_for('admin_posts', delete_message=post.title))


# Удаление поста
@app.route('/delete_file', methods=['POST'])
def delete_file():
    if 'username' not in session:
        return redirect("/login", code=302)
    else:
        file_name=request.form['file_name']
        directory = os.path.join(APP_ROOT, 'static/uploads/blog/')
        path = os.path.join(directory, file_name)
        # print(file_name)
        # print(directory)
        # print(path)
        os.remove(path)
        return redirect(url_for('file_manager', file_name=file_name))


# Создание нового поста
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    text = request.form['text']
    tags = request.form['tags']
    last_edit_date = datetime.utcnow()
    tags_splited = tags.split(',')

    tag_names = []
    tags = Tag.query.all()  
    
    for tag in tags:
        tag_names.append(tag.tag_name)

    # Добавление нового тега в справочник в базе
    for tag in tags_splited:
        if tag not in tag_names:
            new_tag = Tag(tag)
            db.session.add(new_tag)
            db.session.commit()

    # Теги поста, без повторяющихся
    all_post_tags = []
    for tag in tags_splited:
        if tag not in all_post_tags:
            all_post_tags.append(tag)

    tags_id = []
    for tag in all_post_tags:
        tags_id.append(Tag.query.filter(Tag.tag_name == tag).first())
    
    post = Post(title, text, False)
    post.tags.extend(tags_id)
    db.session.add(post)
    db.session.commit()
    return jsonify(True)


# Публикация  поста
@app.route('/publicate_post', methods=['POST'])
def publicate_post():
    if 'username' not in session:
        return redirect("/login", code=302)
    else:
        parameters = request.form['arguments'].split(',')
        publicated = parameters[1]
        id = parameters[0]
        single_post = Post.query.filter_by(id=id).first()
        if publicated == 'False':
            Post.query.filter_by(id=id).update({'published': True})
            db.session.commit()
            return redirect(url_for('admin_posts', publicate_message=single_post.title))
        Post.query.filter_by(id=id).update({'published': False})
        db.session.commit()
        return redirect(url_for('admin_posts', unpublicate_message=single_post.title))


# Загрузка фото на серв
@app.route('/upload', methods=['POST'])
def upload():
    if 'username' not in session:
        return redirect("/login", code=302)
    else:
        file_val = request.files['SelectedFile']
        if file_val and allowed_file(file_val.filename):
            file_val.save(os.path.join(app.config['UPLOAD_FOLDER'], file_val.filename))
        return jsonify('OK', 'success')
# ###################Функционал-ADMIN###################


# ###################Функционал-MAIN####################
# Обработка выхода из сесссии
@app.route('/admin/logout')
@app.route('/logout')
def log_out():
    if 'username' in session:
        session.pop('username', None)
        session.pop('user_id', None)
        session.clear()
        return redirect("/main", code=302)
    return redirect("/login", code=302)


# Обработка запроса авторизации
@app.route('/login_ajax', methods=['POST'])
def log_in():
        admin = User.query.filter_by(email='slashkinks@gmail.com').first()
        user_data = {'login':request.form['login'], 'password': request.form['password']}
        if user_data['login'] == admin.email:
            if md5(user_data['password'].encode()).hexdigest() == admin.password:
                session['username'] = admin.username
                session['user_id'] = admin.id
                return jsonify(1) #all good
            return jsonify(2)     #bad-pass
        return jsonify(3)         #bad-login
# ###################Функционал-MAIN####################


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def check_login():
    if 'username' in session:
        return True
    return False


def sql_debug(response):
    queries = list(get_debug_queries())
    query_str = ''
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        stmt = str(q.statement % q.parameters).replace('\n', '\n       ')
        query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(q.duration * 1000, 2))
    print ('=' * 80)
    print (' SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    print ('=' * 80)
    print (query_str.rstrip('\n'))
    print ('=' * 80 + '\n')
    return response

#app.after_request(sql_debug)

if __name__ == '__main__':
    app.run()