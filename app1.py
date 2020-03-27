from flask import Flask, render_template, url_for, request, session, redirect
#from flask.ext.pymongo import PyMongo
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
import pymongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb://slohani001:Pwcwelcome1!13.90.173.138:27017/test'

app.config['SECRET_KEY'] = 'thisisthesecretkey'

#mongo = PyMongo(app)
#mongo = pymongo(app)
mongo = pymongo.MongoClient("13.90.173.138", 27017)

twitter_blueprint = make_twitter_blueprint(api_key='V6FNK8EvFlTM8rkzzngYTeSEr', api_secret='i38Cz5srPe3PIYbuqlQ05p6BJapT4019vy49ZfMtOuxt6we482')

app.register_blueprint(twitter_blueprint, url_prefix='/twitter_login')


@app.route('/twitter')
def twitter_login():
      if not twitter.authorized:
	      return redirect(url_for('twitter.login'))
      account_info = twitter.get('account/settings.json')

      if account_info.ok:
            return 'your twitter name is @{}'
      return 'request failed'
@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']+render_template('index.html')

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        #if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            #session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'+render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'+render_template('index.html')

    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)