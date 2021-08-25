from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag
from helper import query_all, query_by_id

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'secret-goes-here'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def users_page_redirect():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = query_all(User)
    return render_template('/list.html', users=users)

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    user = query_by_id(User, user_id)
    return render_template('/user/details.html', user=user)

@app.route('/users/new')
def show_new_user_form():
    return render_template('/user/new.html')

@app.route('/users/new', methods=['POST'])
def submit_new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    flash('User created!')

    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    user = query_by_id(User, user_id)
    return render_template('/user/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def submit_edited_user(user_id):
    user = query_by_id(User, user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    flash(f'{user.first_name} {user.last_name} updated!')
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = query_by_id(User, user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f'{user.first_name} {user.last_name} deleted')
    
    return redirect('/users')

# posts

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    post = query_by_id(Post, post_id)
    return render_template('/post/details.html', post=post)

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    user = query_by_id(User, user_id)
    tags = query_all(Tag)

    return render_template('/post/new.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def submit_new_post(user_id):
    user = query_by_id(User, user_id)
    
    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user=user)
    flash('Post created!')

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = query_by_id(Post, post_id)
    tags = query_all(Tag)
    return render_template('/post/edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_edited_post(post_id):
    post = query_by_id(Post, post_id)

    post.title = request.form['title']
    post.content = request.form['content']
    
    tag_ids = [int(num) for num in request.form.getlist('tag')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    flash('Post Updated!')

    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = query_by_id(Post, post_id)
    
    db.session.delete(post)
    db.session.commit()

    flash('Post deleted')

    return redirect(f'/users/{post.user_id}')

# Tags 

@app.route('/tags')
def show_tags():
    all_tags = query_all(Tag)
    return render_template('tag/list.html', tags=all_tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    tag = query_by_id(Tag, tag_id)
    return render_template('tag/details.html', tag=tag)

@app.route('/tags/new')
def show_new_tag_form():
    return render_template('tag/new.html')

@app.route('/tags/new', methods=['POST'])
def submit_new_tag():
    name = request.form['name']
    tag = Tag(name=name)

    flash('Tag created!')

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    tag = query_by_id(Tag, tag_id)
    return render_template('tag/edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def submit_edited_tag(tag_id):
    tag = query_by_id(Tag, tag_id)
    tag.name = request.form['name']

    flash('Tag updated!')

    db.session.commit()

    return redirect(f'/tags/{tag.id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = query_by_id(Tag, tag_id)

    db.session.delete(tag)
    db.session.commit()

    flash('Tag deleted')

    return redirect('/tags')