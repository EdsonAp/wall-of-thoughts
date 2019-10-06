from flask import Flask, render_template, request, session, flash, redirect
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt #NEW LINE
import re #re : regular expression


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')     
#INVALID_PASSWORD_REGEX = re.compile(r'^[^0-9]*|[^A-Z]*)$')

app = Flask(__name__)
bcrypt = Bcrypt(app) #NEW LINE
app.secret_key = "Keep it secret"

@app.route('/')
def registration_land():
    print("FUNCTION 1")
    return render_template('index.html')


@app.route('/register', methods = ['POST'])
def registered():
    is_valid = True
    if len(request.form['fname'])<2:
        is_valid=False
        flash('Please enter first name')
    if len(request.form['lname'])<2:
        is_valid=False
        flash('Please enter last name')
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Please enter a valid email')    
    if len(request.form['password'])<8:
        is_valid=False
        flash('Password must be at least 8 characters long')
    if request.form['c_password'] != request.form['password']:
        is_valid=False
        flash('Passwords do no match')
    if is_valid:
        print("*"*80)
        print("FUNCTION 2")
        
        pw_hash = bcrypt.generate_password_hash(request.form['password']) #NEW LINE
        mysql = connectToMySQL('thoughtsdb')
        query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES (%(nomb)s,%(lnomb)s, %(em)s, %(pass)s, NOW(),NOW());"

        data = {
        'nomb' : request.form['fname'],
        'lnomb' : request.form['lname'],
        'em' : request.form['email'],
        'pass' : pw_hash
        }
        print(query)
        register_id = mysql.query_db(query, data)
        session['user_id'] = register_id
        session['greeting'] = request.form['fname']
        session['greeting2'] = request.form['lname']
        return redirect('/thoughts')  
    return redirect('/')


@app.route('/login', methods = ['POST'])
def login():
    

    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Please enter your email')
    if len(request.form['password'])<1:
            is_valid = False
            flash('Please enter your password')
    if not is_valid:
        return redirect('/')
    
    else:
        mysql = connectToMySQL('thoughtsdb')
        query = 'SELECT * FROM users WHERE email = %(em)s;'
        data = {
                'em' : request.form['email']
            }  
        results = mysql.query_db(query,data)
        session['greeting'] = results[0]['first_name']
        session['greeting2'] = results[0]['last_name']
        session['user_id'] = results[0]['id']
        print(results)
        if len(results) > 0:
            if bcrypt.check_password_hash(results[0]['password'], request.form['password']):
                return redirect('/thoughts')
            else: 
                flash('Email and password do not match')
        else:
            flash('Email has not been registered')
        
        return redirect('/')


@app.route('/thoughts')
def approved():
    if 'user_id' not in session:
        return redirect('/')

    mysql = connectToMySQL('thoughtsdb')
    query = 'SELECT first_name, last_name FROM users WHERE id=%(id)s;'
    data={'id': session['user_id']}
    user = mysql.query_db(query, data)
    print(user)

    print("^#"*80)

    mysql = connectToMySQL('thoughtsdb')
    query= 'select users.first_name, thoughts.id ,users.last_name, thoughts.message from thoughts LEFT JOIN users ON thoughts.user_id = users.id ;'
    # query = 'SELECT users.first_name, users.id ,users.last_name, thoughts.message, count(like_thoughts.users_id) FROM users JOIN thoughts ON users.id = thoughts.user_id left JOIN like_thoughts ON thoughts.id = like_thoughts.thoughts_id group by users.first_name, users.id ,users.last_name, thoughts.message;'
    thoughts = mysql.query_db(query)

    print(thoughts)

    mysql = connectToMySQL('thoughtsdb')
    query = 'SELECT * FROM followers WHERE follower = %(u_id)s'
    data = {
        'u_id' : session['user_id']
    }
    ids_im_following = mysql.query_db(query, data)
  
    return render_template('success.html',thoughts=thoughts)


@app.route('/thoughts', methods = ['POST'])
def thunk():
    is_valid = True
    if len(request.form['thoughttxt']) < 5:
        flash('Think between longer than 5 characters long')
    
    else: 
        mysql = connectToMySQL('thoughtsdb')
        query = 'INSERT INTO thoughts (message, created_at, updated_at, user_id) VALUES (%(msg)s, NOW(), NOW(), %(id)s);'
        data = {
            'msg' : request.form['thoughttxt'],
            'id' : session['user_id']
        }
        newtwt_id = mysql.query_db(query, data)
        
    return redirect('/thoughts')


@app.route('/thoughts/<twt_id>/delete')
def delete(twt_id):
    print("DELETE FUNCTION!!!!!!!")
    if 'user_id' not in session:
        flash('You cannot delete this thought')
        return redirect('/thoughts')
    else:
        query = 'DELETE from like_thoughts WHERE id = %(twt_id)s'
        data = { 'twt_id' : twt_id }
        mysql = connectToMySQL('thoughtsdb')
        mysql.query_db(query, data)

        query = 'DELETE FROM thoughts WHERE id = %(twt_id)s and user_id = %(sesh_id)s' #updated
        mysql = connectToMySQL('thoughtsdb')
        data = {
            'twt_id' : twt_id,
            'sesh_id' : session['user_id']
        }
        mysql.query_db(query, data)
        return redirect('/thoughts')


@app.route('/thoughts/<twt_id>/details')
def thought_detail(twt_id):
    
    mysql = connectToMySQL('thoughtsdb')
    query = 'select users.first_name, thoughts.id, thoughts.user_id ,users.last_name, thoughts.message from thoughts left JOIN users ON thoughts.user_id = users.id where thoughts.id = %(twt_id)s'
    data = {
        'twt_id' : twt_id
    }
    pensar = mysql.query_db(query,data)
    print('&'*80)
    print(pensar)

    mysql = connectToMySQL('thoughtsdb')
    query = 'select users.first_name, users.last_name, like_thoughts.users_id from users left JOIN like_thoughts ON users.id = like_thoughts.users_id where thoughts_id = %(twt_id)s'
    data = {
        'twt_id' : twt_id
    }
    user_likes = mysql.query_db(query,data)
    print(user_likes)

    return render_template('edit.html', pensar=pensar, user_likes=user_likes)
    


@app.route('/thoughts/<twt_id>/like')
def liked_tweet(twt_id):
    print('x'*80)
    mysql = connectToMySQL('thoughtsdb')
    query = 'INSERT INTO like_thoughts (thoughts_id, users_id) VALUES (%(twt_id)s, %(user_id)s);'
    data = {
        'twt_id' : twt_id ,
        'user_id' : session['user_id']
    }
    resulta = mysql.query_db(query, data)


    print('*'*80)
    return redirect('/thoughts/{}/details'.format(twt_id))
    #return redirect('/thoughts')
    

@app.route('/thoughts/<twt_id>/unlike')
def unlike(twt_id):
    
    print('YOU ARE IN THE UNLIKE FUNCTION')
    print(twt_id)

    mysql = connectToMySQL('thoughtsdb')
    query = 'DELETE from like_thoughts WHERE users_id = %(user_id)s and thoughts_id = %(t_id)s'
    data = { 
        'user_id' : session['user_id'],
        't_id' : twt_id
    }
    unliked = mysql.query_db(query, data)
    print(unliked)

    #return redirect('/thoughts')
    return redirect('/thoughts/{}/details'.format(twt_id))



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

    


if __name__ == "__main__":
    app.run(debug=True)