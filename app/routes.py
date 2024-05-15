from app import db, app
from app.models import User, Item, Category, Status, Cart
from app.forms import RegistrationForm, LoginForm, ItemForm, CartForm, UpdateProfileForm, UpdateItemForm, SearchForm
from flask import render_template, url_for, request, flash, redirect, g, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from flask_babel import _, get_locale
import stripe
from urllib.parse import urlsplit
from werkzeug.utils import secure_filename
import os

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51PDMxxHvA8h6eG8EFRCNngzmZtH3bKsJeLYdZgu9geWYPk0AsdzRuYACz4Aj1XD4rgcyEaFHslO26oFB2MKgtzGF000wZgaXb5'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51PDMxxHvA8h6eG8Ev9Y5m3q0qXeKLFEMSNi1yRjZlG7YjbFwQUeNbZ4IWaIgsNKGFabOXsSzsDBNdvTIAKU1oN7m0059I0hPYV'
stripe.api_key = app.config['STRIPE_SECRET_KEY']

@app.before_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()
    g.locale = str(get_locale())

@app.route('/')
@app.route('/home')
def home():
    items = db.session.query(Item).order_by(Item.timestamp.asc()).all()
    sorted_items = sorted(items, key=lambda x: x.timestamp)
    categories = db.session.query(Category).all()
    return render_template('home.html', items=items, categories=categories, sorted_items=sorted_items)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, phone_number=form.phone_number.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('User has been created!'))
        return redirect(url_for('home'))
    return render_template('registration_form.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('home')
            flash(_('Successfully logged in!'), 'success')
            return redirect(next_page)
        else:
            flash(_('Username or Password is incorrect'), 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/create_item', methods=['GET', 'POST'])
@login_required
def create_item():
    form = ItemForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    form.item_status.choices = [(item_status.id, item_status.status) for item_status in Status.query.all()]
    if form.validate_on_submit():
        img = form.images.data
        filename = secure_filename(img.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Save the file with its original filename in the UPLOAD_FOLDER directory
        form.images.data.save(file_path)

        # Get the parent directory of the file
        parent_directory = os.path.basename(os.path.dirname(file_path))
        # Update file_path to only hold the parent directory
        file_path = os.path.join(parent_directory, filename)
        category_id = form.category.data
        category = Category.query.get(category_id)
        item_status_id = form.item_status.data
        status = Status.query.get(item_status_id)

        item = Item(images=file_path, item_name=form.item_name.data, item_desc=form.item_desc.data,
        category=category, price=form.price.data, price_currency=form.price_currency.data, item_status=status ,seller=current_user)
        db.session.add(item)
        db.session.commit()
        flash(_('Successfully listed item'), 'success')
        return redirect(url_for('create_item'))
    return render_template('create_item.html', form=form)

@app.route('/collections')
def collections():
    categories = db.session.query(Category).all()
    return render_template('collections.html', categories=categories)

@app.route('/collections/<category>', methods=['GET', 'POST'])
def collection_category(category):
    page = request.args.get('page', 1, type=int)
    cart_form = CartForm()
    category = db.session.query(Category).filter_by(name=category).first()
    items_query = db.session.query(Item).filter_by(category=category)

    #Pagination
    items = db.paginate(items_query, page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
    print(items)
    next_url = url_for('collection_category', category=category.name, page=items.next_num)\
        if items.has_next else None
    prev_url = url_for('collection_category', category=category.name, page=items.prev_num)\
        if items.has_prev else None

    carts = db.session.query(Cart).all()
    return render_template('product_collection.html', items=items, category=category, cart_form=cart_form, carts=carts, next_url=next_url, prev_url=prev_url)

@app.route('/user/<username>')
def user(username):
    cart_form = CartForm()
    user = db.session.query(User).filter_by(username=username).first()
    items = user.items
    if user:
        return render_template('user.html', user=user, items=items, cart_form=cart_form)
    else:
        flash("Couldn't find User")
        return redirect(url_for('home'))
    
@app.route('/user/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm(
        current_user.username,
        current_user.email
    )
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.telegram_link = form.telegram_link.data
        current_user.instagram_link = form.instagram_link.data
        db.session.commit()
        flash('Profile Updated!', 'success')
        return redirect('update_profile')
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.telegram_link.data = current_user.telegram_link
        form.instagram_link.data = current_user.instagram_link

    return render_template('update_profile.html', form=form)

@app.route('/item/<item_name>')
def item(item_name):
    item = db.session.query(Item).filter_by(item_name=item_name).first()
    if item:
        return render_template('item.html', item=item)

@app.route('/item/<item_name>/update_item', methods=['GET', 'POST'])
@login_required
def update_item(item_name):
    item = db.session.query(Item).filter_by(item_name=item_name).first()
    if item in current_user.items:
        form = UpdateItemForm()
        form.item_status.choices = [(item_status.id, item_status.status) for item_status in Status.query.all()]
        if form.validate_on_submit():
            status_id = form.item_status.data
            status = db.session.query(Status).filter_by(id=status_id).first()
            item.item_name = form.item_name.data
            item.item_desc = form.item_desc.data
            item.item_status = status
            item.price = form.price.data
            item.price_currency = form.price_currency.data
            db.session.add(item)
            db.session.commit()
            
            flash('Successfully Updated Item!', 'success')
            return redirect(url_for('user', username=current_user.username))
        elif request.method == 'GET':
            form.item_name.data = item.item_name
            form.price.data = item.price
            form.price_currency.data = item.price_currency
            form.item_desc.data = item.item_desc
            form.item_status.data = item.item_status
        return render_template('update_item.html', form=form, item=item)
    else:
        flash("Item couldn't be accessed", "danger")
        return render_template('home.html')
    
@app.route('/item/<item_name>/delete')
@login_required
def delete_item(item_name):
    item = db.session.query(Item).filter_by(item_name=item_name).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Successfully deleted Item!", "success")
        return redirect(url_for('user', username=current_user.username))
    else:
        flash("Item couldn't be accessed", "danger")
        return render_template('home.html')


@app.route('/carts')
@app.route('/carts/<item_id>', methods=['GET', 'POST'])
@login_required
def carts(item_id=None):
    carts = db.session.query(Cart).all()
    total_price = 0
    for cart in carts:
        total_price += cart.items.price
    if item_id:
        item = db.session.query(Item).filter_by(id=item_id).first()
        cart_item = Cart(items=item, user=item.seller)
        db.session.add(cart_item)
        db.session.commit()
        flash('Item added to Cart!', 'success')
        return redirect(url_for('carts'))
    return render_template('carts.html', title='Carts', carts=carts, total_price=total_price)

@app.route('/carts/<cart_id>/delete')
@login_required
def delete_from_cart(cart_id=None):
    if cart_id:
        cart = db.session.query(Cart).filter_by(id=cart_id).first()
        db.session.delete(cart)
        db.session.commit()
        flash('Item removed from cart', 'success')
        return redirect(url_for('carts'))

@app.route('/checkout')
def checkout():
    carts = db.session.query(Cart).all()
    line_items = []
    for cart in carts:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'unit_amount': cart.items.price,
                'product_data': {
                    'name': cart.items.item_name,
                    'description': cart.items.item_desc,
                }
            },
            'quantity': 1,
        })
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('home', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

@app.route('/home/success')
def success():
    flash('Successfully purchased!', 'success')
    db.session.query(Cart).delete()
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/search', methods=['GET'])
@login_required
def search():
    if not g.search_form.validate():
        flash("Failed Search", 'danger')
        return redirect(url_for('home'))
    page = request.args.get('page', 1, type=int)
    items, total = Item.search(g.search_form.q.data, page, app.config['ITEMS_PER_PAGE'])
    
    next_url = url_for('search', q=g.search_form.q.data, page=page+1)\
        if total > page * app.config['ITEMS_PER_PAGE'] else None
    prev_url = url_for('search', q=g.search_form.q.data, page=page - 1)\
        if page > 1 else None
    return render_template('search.html', title='Search', items=items, next_url=next_url, prev_url=prev_url)
        
        