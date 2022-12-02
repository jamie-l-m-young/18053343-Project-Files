from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from operator import itemgetter
from passlib.hash import sha256_crypt
import mysql.connector
import requests
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__) 

app.secret_key = 'foxesmead'

conn = mysql.connector.connect(
user='helpinghands',
password='qjLPjp4reBk9NL8T',
host='127.0.0.1',
database='helpinghands')

mycursor = conn.cursor()

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if "loggedin" in session:
        return redirect(url_for('home'))
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mycursor
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        check = cursor.rowcount
        if check == 0:
            msg = "That username doesn't exist - please try again or register a new account"
            return render_template('login.html', msg=msg)
        cursor.reset()
        msg=account[0];        
        #verify user
        if(sha256_crypt.verify(password, account[3]) == True):
            msg = " Match"
            #create session
            if account:
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['is_charity'] = account[4]
                return redirect(url_for('home'))
            else:
                msg = "Session creation failed"
        else:
            msg = "That password is not recongnized"
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('is_charity', None)
   return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if "loggedin" in session:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        session.pop('is_charity', None)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'type' in request.form and 'phone' in request.form and 'dbs' in request.form and 'name' in request.form:
        username = request.form['username']
        password = request.form['password']
        rePassword = request.form['re-password']
        if len(password) < 8:
            msg = "Password must be at least 8 characters"
            return render_template('register.html', msg=msg)
        email = request.form['email']
        phone = request.form['phone']
        maxDis = request.form['dis']
        for i in maxDis:
            if i.isdigit():
                msg = ''
            else:
                msg = 'Distance must only contain numbers'
                return render_template('register.html', msg=msg)
        dbs = 0
        name = request.form['name']
        if(request.form['type'] == 'charity'):
            isCharity = 1
        elif(request.form['type'] == 'volunteer'):
            isCharity = 0
        else:
            msg = "Type not selected"
        if(request.form['dbs'] == 'yes' and isCharity == 0):
            dbs = 1
        elif(request.form['dbs'] == 'no' and isCharity == 0):
            dbs = 0
        else:
            msg = "DBS not selected"
        if isCharity == 1:
            maxDis = 0
        cursor = mycursor
        cursor.execute('SELECT * FROM users WHERE username = %s OR email = %s', (username,email,))
        account = cursor.fetchone()
        check = cursor.rowcount
        if check != 0:
            if account[1] == username:
                msg = 'There is already an account using this username'
            elif account[2] == email:
                msg = 'There is already an account using this email address'
            elif '@' not in email:
                msg = 'Not valid email address'
            elif password != rePassword:
                msg = "Passwords don't match"
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                password = sha256_crypt.hash(password)
                cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, NULL, %s, %s, %s, %s)', (username, email, password, isCharity, phone, dbs, name, maxDis))
                conn.commit()
                msg = 'You have successfully registered! Please login'
                return render_template('login.html', msg=msg)
        else:
            if '@' not in email:
                msg = 'Not valid email address'
            elif password != rePassword:
                msg = "Passwords don't match"
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                password = sha256_crypt.hash(password)
                cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, NULL, %s, %s, %s, %s)', (username, email, password, isCharity, phone, dbs, name, maxDis))
                conn.commit()
                msg = 'You have successfully registered! Please login'
                return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/chats', methods=['GET', 'POST'])
def chats():
    msg = ''
    
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if session.get('is_charity', 'not set') == 0:
            isCharity = 'no'
        else:
            isCharity = 'yes'
        cursor = mycursor
        if request.method == 'POST' and 'name' in request.form:
            chat_name = request.form['name']
            now = datetime.now()
            time = now.strftime("%Y/%m/%d %H:%M:%S")
            cursor.execute('INSERT INTO chats (chat_name, chat_admin_id, chat_creator_id, creation_time, update_time)VALUES (%s, %s, %s, %s, %s)',(chat_name, session.get('id', 'not set'), session.get('id', 'not set'), time, time,))
            conn.commit()
            cursor.execute('SELECT chat_id FROM chats WHERE creation_time = %s AND chat_creator_id = %s', (time, session.get('id', 'not set'),))
            chat = cursor.fetchone()
            cursor.execute('INSERT INTO participants (chat_id, user_id)VALUES (%s, %s)',(chat[0], session.get('id', 'not set'),))
            conn.commit()
            msg = 'CREATED'
        cursor.execute('SELECT chat_name, update_time, chat_id FROM chats WHERE chat_id IN (SELECT chat_id FROM participants WHERE user_id = %s) ORDER BY update_time DESC', (session.get('id', 'not set'),))
        chats = cursor.fetchall() 
        check = cursor.rowcount
        if check == 0:
            hasChat = False
        else:
            hasChat = True
    return render_template('chats.html', msg=msg,
                                        chats=chats,
                                        user_id=session.get('id', 'not set'),
                                        isCharity = isCharity,
                                        hasChat=hasChat)
    
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'chat_id' in request.form:
            if session.get('is_charity', 'not set') == 0:
                isCharity = 'no'
            else:
                isCharity = 'yes'
            cursor = mycursor
            chat_id = request.form['chat_id']
            cursor.execute('SELECT chat_name FROM chats WHERE chat_id = %s', (chat_id,))
            chat_name = cursor.fetchone()
            cursor.execute('SELECT users.real_name, messages.message_time, messages.content, users.user_id FROM messages INNER JOIN users ON messages.sender_id=users.user_id WHERE chat_id = %s ORDER BY message_time DESC', (chat_id,))
            chat = cursor.fetchall()
            return render_template('chat.html', 
                                    chat=chat,
                                    chat_name=chat_name,
                                    chat_id=chat_id,
                                    user_id=session.get('id', 'not set'),
                                    isCharity = isCharity)
        return redirect(url_for('chats'))
    return redirect(url_for('index'))
    
@app.route('/chatSent', methods=['GET', 'POST'])
def chatSent():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        cursor = mycursor
        cursor.execute('SELECT chat_id FROM participants WHERE user_id = %s', (session.get('id', 'not set'),))
        chats = cursor.fetchall()
        if request.args.get('chat_id') != None:
            if session.get('is_charity', 'not set') == 0:
                isCharity = 'no'
            else:
                isCharity = 'yes'
            chat_id = request.args.get('chat_id')
            for x in chats:
                if int(chat_id) in x:
                    cursor.execute('SELECT chat_name FROM chats WHERE chat_id = %s', (chat_id,))
                    chat_name = cursor.fetchone()
                    cursor.execute('SELECT users.real_name, messages.message_time, messages.content,users.user_id FROM messages INNER JOIN users ON messages.sender_id=users.user_id WHERE chat_id = %s ORDER BY message_time DESC', (chat_id,))
                    chat = cursor.fetchall()
                    return render_template('chat.html', 
                                            chat=chat,
                                            chat_name=chat_name,
                                            chat_id=chat_id,
                                            user_id=session.get('id', 'not set'),
                                            isCharity = isCharity)
            return redirect(url_for('chats'))
        return redirect(url_for('chats'))
    return redirect(url_for('index'))

@app.route('/sendMessage', methods=['GET', 'POST'])
def sendMessage():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'chat_id' in request.form and 'message' in request.form:
            cursor = mycursor
            chat_id = request.form['chat_id']
            message = request.form['message']
            now = datetime.now()
            time = now.strftime("%Y/%m/%d %H:%M:%S")
            cursor.execute('INSERT INTO messages (sender_id, chat_id, content, message_time)VALUES (%s, %s, %s, %s)',(session.get('id', 'not set'), chat_id, message, time,))
            conn.commit()
            cursor.execute('UPDATE chats SET update_time = %s WHERE chat_id = %s', (time, chat_id))
            conn.commit()
            return redirect(url_for('chatSent', chat_id=chat_id))
        return redirect(url_for('index'))
    return redirect(url_for('index'))
    
@app.route('/refreshChat', methods=['GET', 'POST'])
def refreshChat():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'chat_id' in request.form:
            chat_id = request.form['chat_id']
            return redirect(url_for('chatSent', chat_id=chat_id))
        return redirect(url_for('index'))
    return redirect(url_for('index'))
    
@app.route('/account')
def account():
    if "loggedin" in session:
        if(session.get('id', 'not set') != 'not set'):
            cursor = mycursor
            cursor.execute('SELECT user_id, username, email, is_charity, address_id, phone, real_name, has_dbs, max_distance FROM users WHERE user_id = %s', (session.get('id', 'not set'),))
            account = cursor.fetchone()
            
            if(account[3] == 1):
                isCharity = 'Charity'
            elif(account[3] == 0):
                isCharity = 'Volunteer'
            
            if(account[7] == 1):
                dbs = 'Yes'
            elif(account[7] == 0):
                dbs = 'No'
        address = '       '
        if(account[4] != None):
            cursor.execute('SELECT ad_line1, ad_line2, city, county, postcode FROM addresses WHERE address_id = %s', (account[4],))
            address = cursor.fetchone()
            
        cursor.execute('SELECT interests.interest, interests.interest_id FROM interests INNER JOIN user2interest ON interests.interest_id=user2interest.interest_id WHERE user2interest.user_id = %s', (session.get('id', 'not set'),))
        userInterests = cursor.fetchall()
        cursor.execute('SELECT interest_id, interest FROM interests')
        interests = cursor.fetchall()
        cursor.execute('SELECT * FROM avadibility WHERE user_id = %s', (session.get('id', 'not set'),))
        avadibility = cursor.fetchall()
        check = cursor.rowcount
        if check == 0:
            freshT = '00:00:00'
            cursor.execute('INSERT INTO avadibility VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (session.get('id', 'not set'), freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT,))
            conn.commit()
            cursor.execute('SELECT * FROM avadibility WHERE user_id = %s', (session.get('id', 'not set'),))
            avadibility = cursor.fetchall()
        avadibility = avadibility[0]
        mon = [avadibility[2],avadibility[3]]
        tue = [avadibility[4],avadibility[5]]
        wed = [avadibility[6],avadibility[7]]
        thur = [avadibility[8],avadibility[9]]
        fri = [avadibility[10],avadibility[11]]
        sat = [avadibility[12],avadibility[13]]
        sun = [avadibility[14],avadibility[15]]
        return render_template('account.html',
                                accountNumber = account[0],
                                username=account[1],
                                email=account[2],
                                phone=account[5],
                                name = account[6],
                                isCharity=isCharity, 
                                ad_line1=address[0],
                                ad_line2=address[1],
                                city=address[2],
                                county=address[3],
                                postcode=address[4],
                                maxDis = account[8],
                                interests=interests,
                                userInterests=userInterests,
                                avadibility=avadibility,
                                user_id=session.get('id', 'not set'),
                                mon=mon,
                                tue=tue,
                                wed=wed,
                                thur=thur,
                                fri=fri,
                                sat=sat,
                                sun=sun,
                                dbs=dbs)
    return render_template('login.html')

@app.route('/addInterest', methods=['GET', 'POST'])
def addInterest():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'newInterest' in request.form:
            isEmpty = 0
            cursor = mycursor
            newInterest = request.form['newInterest']
            cursor.execute('SELECT interest_id FROM user2interest WHERE user_id = %s AND interest_id = %s', (session.get('id', 'not set'),newInterest,))
            check = cursor.fetchall()
            isEmpty = cursor.rowcount
            msg=isEmpty
            if isEmpty == 0:
                cursor.execute('INSERT INTO user2interest (user_id,interest_id) VALUES (%s,%s)', (session.get('id', 'not set'),newInterest,))
                conn.commit()
                return redirect(url_for('account'))
            return redirect(url_for('account'))
    return render(url_for('home'))
    
@app.route('/addOpportunityInterest', methods=['GET', 'POST'])
def addOpportunityInterest():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'newInterest' in request.form:
            isEmpty = 0
            cursor = mycursor
            newInterest = request.form['newInterest']
            opportinity_id = request.form['opportinity_id']
            cursor.execute('SELECT opportunity2interest_id FROM opportunity2interest WHERE opportunity_id = %s AND interest_id = %s', (opportinity_id,newInterest,))
            check = cursor.fetchall()
            isEmpty = cursor.rowcount
            msg=isEmpty
            if isEmpty == 0:
                cursor.execute('INSERT INTO opportunity2interest (opportunity_id,interest_id) VALUES (%s,%s)', (opportinity_id,newInterest,))
                conn.commit()
                return redirect(url_for('opportunity',opportinity_id=opportinity_id))
            return redirect(url_for('opportunity',opportinity_id=opportinity_id))
    return redirect(url_for('home'))


@app.route('/removeOppotunityInterest', methods=['GET', 'POST'])
def removeOppotunityInterest():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'interest_id' in request.form and 'opportinity_id' in request.form:
            opportinity_id = request.form['opportinity_id']
            cursor=mycursor
            interest_id = request.form['interest_id']
            cursor.execute('SELECT interest_id FROM opportunity2interest WHERE opportunity_id = %s AND interest_id = %s', (opportinity_id,interest_id,))
            userInterests = cursor.fetchall()
            isEmpty = 0
            isEmpty = cursor.rowcount
            if isEmpty == 0:
                return redirect(url_for('opportunity',opportinity_id=opportinity_id))
            cursor.execute('DELETE FROM opportunity2interest WHERE opportunity_id = %s AND interest_id = %s', (opportinity_id,interest_id,))
            conn.commit()
            return redirect(url_for('opportunity',opportinity_id=opportinity_id))
        return redirect(url_for('index'))

@app.route('/removeInterest', methods=['GET', 'POST'])
def removeInterest():
    if "loggedin" not in session:
        return render_template('login.html')
    else: 
        if request.method == 'POST' and 'interest_id' in request.form:
            cursor=mycursor
            interest_id = request.form['interest_id']
            cursor.execute('SELECT interest_id FROM user2interest WHERE user_id = %s AND interest_id = %s', (session.get('id', 'not set'),interest_id,))
            userInterests = cursor.fetchall()
            isEmpty = 0
            isEmpty = cursor.rowcount
            if isEmpty == 0:
                return redirect(url_for('account'))
            cursor.execute('DELETE FROM user2interest WHERE user_id = %s AND interest_id = %s', (session.get('id', 'not set'),interest_id,))
            conn.commit()
            return redirect(url_for('account'))
        return redirect(url_for('account'))

@app.route('/editOpAddress', methods=['GET', 'POST'])
def editOpAddress():
    if "loggedin" not in session:
        return render_template('login.html')
    else: 
        if request.method == 'POST' and 'ad_line1' in request.form and 'ad_line2' in request.form and 'city' in request.form and 'county' in request.form and 'postcode' in request.form and 'opportinity_id' in request.form:
            if session.get('is_charity', 'not set') == 0:
                isCharity = 'no'
            else:
                isCharity = 'yes'
            ad_line1 = request.form['ad_line1']
            ad_line2 = request.form['ad_line2']
            city = request.form['city']
            county = request.form['county']
            postcode = request.form['postcode']
            opportinity_id = request.form['opportinity_id']
            cursor = mycursor
            cursor.execute('SELECT address_id FROM addresses WHERE ad_line1 = %s AND ad_line2 = %s AND city = %s AND county = %s AND postcode = %s', (ad_line1, ad_line2, city, county, postcode,))
            newAddress = cursor.fetchone()
            if(newAddress != None):
                cursor.execute('UPDATE opportunity SET address_id = %s WHERE opportunity_id = %s', (newAddress[0], opportinity_id))
                conn.commit()
                msg = 'You have successfully changed address!'
                return redirect(url_for('opportunity',opportinity_id=opportinity_id,msg=msg))
            elif(newAddress == None):
                URL = "https://geocode.search.hereapi.com/v1/geocode"
                location = postcode
                api_key = 'iBajSRjrBCvaoRI6O3v92A3j1CboFz624ZcHwq9Gyck'
                PARAMS = {'apikey':api_key,'q':location} 
                r = requests.get(url = URL, params = PARAMS) 
                data = r.json()
                latitude = data['items'][0]['position']['lat']
                longitude = data['items'][0]['position']['lng']
                cursor.execute('INSERT INTO addresses (ad_line1, ad_line2, city, county, postcode, latitude, longitude)VALUES (%s, %s, %s, %s, %s, %s, %s)',(ad_line1,ad_line2,city,county,postcode, latitude, longitude));
                conn.commit()
                cursor.execute('SELECT address_id FROM addresses WHERE ad_line1 = %s AND ad_line2 = %s AND city = %s AND county = %s AND postcode = %s', (ad_line1, ad_line2, city, county, postcode,))
                newAddress = cursor.fetchone()
                cursor.execute('UPDATE opportunity SET address_id = %s WHERE opportunity_id = %s', (newAddress[0], opportinity_id))
                conn.commit()
                msg = 'You have successfully changed address!'
                return redirect(url_for('opportunity',opportinity_id=opportinity_id,msg=msg))
        elif request.method == 'POST' and 'opportinity_id' in request.form:
            msg = 'Please fill out the form!'
            opportinity_id = request.form['opportinity_id']
            if session.get('is_charity', 'not set') == 0:
                isCharity = 'no'
            else:
                isCharity = 'yes'
            return render_template('editOpAddress.html', 
                                    opportinity_id=opportinity_id,
                                    user_id=session.get('id', 'not set'),
                                    isCharity = isCharity)
        return redirect(url_for('home'))
    
@app.route('/editaddress', methods=['GET', 'POST'])
def editAddress():
    if "loggedin" not in session:
        return render_template('login.html')
    else: 
        if request.method == 'POST' and 'ad_line1' in request.form and 'ad_line2' in request.form and 'city' in request.form and 'county' in request.form and 'postcode' in request.form:
            if session.get('is_charity', 'not set') == 0:
                isCharity = 'no'
            else:
                isCharity = 'yes'
            ad_line1 = request.form['ad_line1']
            ad_line2 = request.form['ad_line2']
            city = request.form['city']
            county = request.form['county']
            postcode = request.form['postcode']
            cursor = mycursor
            cursor.execute('SELECT address_id FROM addresses WHERE ad_line1 = %s AND ad_line2 = %s AND city = %s AND county = %s AND postcode = %s', (ad_line1, ad_line2, city, county, postcode,))
            newAddress = cursor.fetchone()
            if(newAddress != None):
                cursor.execute('UPDATE users SET address_id = %s WHERE user_id = %s', (newAddress[0], session.get('id', 'not set')))
                conn.commit()
                msg = 'You have successfully changed address!'
                return redirect(url_for('account'))
            elif(newAddress == None):
                URL = "https://geocode.search.hereapi.com/v1/geocode"
                location = postcode
                api_key = 'iBajSRjrBCvaoRI6O3v92A3j1CboFz624ZcHwq9Gyck'
                PARAMS = {'apikey':api_key,'q':location} 
                r = requests.get(url = URL, params = PARAMS) 
                data = r.json()
                latitude = data['items'][0]['position']['lat']
                longitude = data['items'][0]['position']['lng']
                cursor.execute('INSERT INTO addresses (ad_line1, ad_line2, city, county, postcode, latitude, longitude)VALUES (%s, %s, %s, %s, %s, %s, %s)',(ad_line1,ad_line2,city,county,postcode, latitude, longitude));
                conn.commit()
                cursor.execute('SELECT address_id FROM addresses WHERE ad_line1 = %s AND ad_line2 = %s AND city = %s AND county = %s AND postcode = %s', (ad_line1, ad_line2, city, county, postcode,))
                newAddress = cursor.fetchone()
                cursor.execute('UPDATE users SET address_id = %s WHERE user_id = %s', (newAddress[0], session.get('id', 'not set')))
                conn.commit()
                msg = 'You have successfully changed address!'
                return redirect(url_for('account'))
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        
        if session.get('is_charity', 'not set') == 0:
            isCharity = 'no'
        else:
            isCharity = 'yes'
        return render_template('editaddress.html',
                                user_id=session.get('id', 'not set'),
                                isCharity = isCharity)

@app.route('/editDetails', methods=['GET', 'POST'])
def editDetails():
    if "loggedin" not in session:
        return render_template('login.html')
    else: 
        if session.get('is_charity', 'not set') == 0:
            isCharity = 'no'
        else:
            isCharity = 'yes'
        if request.method == 'POST':
            msg = ''
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            maxDis = request.form['dis']
            cursor = mycursor
            if 'dbs' in request.form:
                dbs = request.form['dbs']
                if dbs == 'yes':
                    dbs = 1
                if dbs == 'no':
                    dbs = 0
                if dbs != '':
                    cursor.execute('UPDATE users SET has_dbs = %s WHERE user_id = %s', (dbs, session.get('id', 'not set'),))
                    conn.commit()
            if maxDis != '':
                cursor.execute('UPDATE users SET max_distance = %s WHERE user_id = %s', (maxDis, session.get('id', 'not set'),))
                conn.commit()
            if name != '':
                cursor.execute('UPDATE users SET real_name = %s WHERE user_id = %s', (name, session.get('id', 'not set'),))
                conn.commit()
            if phone != '':
                cursor.execute('UPDATE users SET phone = %s WHERE user_id = %s', (phone, session.get('id', 'not set'),))
                conn.commit()
            if email != '':
                if '@' not in email:
                    msg = 'Not valid email address'
                    return render_template('editDetails.html', 
                                            msg=msg,
                                            user_id=session.get('id', 'not set'),
                                            isCharity = isCharity)
                cursor.execute('UPDATE users SET email = %s WHERE user_id = %s', (email, session.get('id', 'not set'),))
                conn.commit()
            return redirect(url_for('account'))
        return render_template('editDetails.html',
                                user_id=session.get('id', 'not set'),
                                isCharity = isCharity)

@app.route('/postOpportunity', methods=['GET', 'POST'])
def postOpportunity():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        isCharity = 'no'
        if session.get('is_charity', 'not set') == 1:
            cursor = mycursor
            isCharity = 'yes'
            if request.method == 'POST' and 'title' in request.form and 'discription' in request.form and 'dbs' in request.form and 'day' in request.form and 's_hour' in request.form and 's_minute' in request.form and 'f_hour' in request.form and 'f_minute' in request.form and 'ad_line1' in request.form and 'ad_line2' in request.form and 'city' in request.form and 'county' in request.form and 'postcode' in request.form:
                #request form data            
                title = request.form['title']
                discription = request.form['discription']
                if '"' in title or '"' in discription:
                    msg = "Please don't use quotation marks"
                    return render_template('postOpportunity.html',
                                    user_id=session.get('id', 'not set'),
                                    isCharity = isCharity,
                                    msg=msg)
                dbs = None
                if(request.form['dbs'] == 'yes'):
                    dbs = 1
                elif(request.form['dbs'] == 'no'):
                    dbs = 0
                day = request.form['day']
                s_hour = request.form['s_hour']
                s_minute = request.form['s_minute']
                f_hour = request.form['f_hour']
                f_minute = request.form['f_minute']
                s_time = s_hour + ':' + s_minute + ':00'
                f_time = f_hour + ':' + f_minute + ':00'
                ad_line1 = request.form['ad_line1']
                ad_line2 = request.form['ad_line2']
                city = request.form['city']
                county = request.form['county']
                postcode = request.form['postcode']
                #check if address if in db
                cursor.execute('SELECT address_id FROM addresses WHERE ad_line1 = %s AND ad_line2 = %s AND city = %s AND county = %s AND postcode = %s', (ad_line1, ad_line2, city, county, postcode,))
                newAddress = cursor.fetchone()
                if(newAddress == None):
                    URL = "https://geocode.search.hereapi.com/v1/geocode"
                    location = postcode
                    api_key = 'iBajSRjrBCvaoRI6O3v92A3j1CboFz624ZcHwq9Gyck'
                    PARAMS = {'apikey':api_key,'q':location} 
                    r = requests.get(url = URL, params = PARAMS) 
                    data = r.json()
                    latitude = data['items'][0]['position']['lat']
                    longitude = data['items'][0]['position']['lng']
                    cursor.execute('INSERT INTO addresses (ad_line1, ad_line2, city, county, postcode,latitude,longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)',(ad_line1,ad_line2,city,county,postcode,latitude,longitude))
                    conn.commit()
                    cursor.execute('SELECT address_id FROM addresses WHERE ad_line1 = %s AND ad_line2 = %s AND city = %s AND county = %s AND postcode = %s', (ad_line1, ad_line2, city, county, postcode,))
                    newAddress = cursor.fetchone()
                #create record
                cursor.execute('INSERT INTO opportunity (title, discription, has_dbs, day_needed, start_time, finish_time, address_id, poster_id)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',(title,discription,dbs,day,s_time,f_time,newAddress[0],session.get('id', 'not set'),))
                conn.commit()
                cursor.execute('SELECT opportunity_id FROM opportunity WHERE title = %s AND discription = %s AND has_dbs = %s AND day_needed = %s AND start_time = %s AND finish_time = %s AND address_id = %s AND poster_id = %s',(title,discription,dbs,day,s_time,f_time,newAddress[0],session.get('id', 'not set'),))
                opportunity_id = cursor.fetchall()
                opportunity_id = opportunity_id[0]
                chat_name = title
                if len(chat_name) > 25:
                    hold = ''
                    for i in range(25):
                        hold += chat_name[i]
                    chat_name = hold
                chat_name += ' - group chat'
                now = datetime.now()
                time = now.strftime("%Y/%m/%d %H:%M:%S")
                cursor.execute('INSERT INTO chats (chat_name, chat_admin_id, chat_creator_id, creation_time, update_time) VALUES (%s, %s, %s, %s, %s)', (chat_name,session.get('id', 'not set'),session.get('id', 'not set'),time,time,))
                conn.commit()
                cursor.execute('SELECT chat_id FROM chats WHERE chat_creator_id = %s AND creation_time = %s',(session.get('id', 'not set'),time,))
                chat_id = cursor.fetchall()
                chat_id = chat_id[0]
                cursor.execute('INSERT INTO participants (chat_id,user_id) VALUES (%s,%s)', (chat_id[0],session.get('id', 'not set'),))
                conn.commit()
                cursor.execute('INSERT INTO opportunity2chat (opportunity_id,chat_id) VALUES (%s,%s)', (opportunity_id[0],chat_id[0]))
                conn.commit()
                msg = newAddress[0]
                return redirect(url_for('myOpportunities'))
            if session.get('is_charity', 'not set') == 0:
                isCharity = 'no'
            else:
                isCharity = 'yes'
            return render_template('postOpportunity.html',
                                    user_id=session.get('id', 'not set'),
                                    isCharity = isCharity)
        else:
            return redirect(url_for('logout'))
        return render_template('home')

@app.route('/myOpportunities')
def myOpportunities():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        cursor = mycursor
        if request.args.get('msg') != None:
            msg = request.args.get('msg')
        else:
            msg = ''
        if session.get('is_charity', 'not set') == 1:
            #charity path
            cursor.execute('SELECT opportunity_id, title, discription, day_needed, start_time, finish_time, poster_id FROM opportunity WHERE poster_id = %s', (session.get('id', 'not set'),))
            sqlopportunities = cursor.fetchall()
            check = cursor.rowcount
            opportunities = []
            if check != 0:
                hasOpportunity = True
                for opportunity in sqlopportunities:
                    length = 160
                    str2display = opportunity[2]
                    if len(opportunity[2]) > length:
                        str2display = ''
                        for i in range(length):
                            str2display += opportunity[2][i]
                        str2display += '...'
                    hold = [opportunity[0],opportunity[1],str2display,opportunity[3],opportunity[4],opportunity[5],opportunity[6]]  
                    opportunities += [hold]
            else:
                hasOpportunity = False
            return render_template('charityOpportunities.html',
                            opportunities=opportunities,
                            user_id=session.get('id', 'not set'),
                            isCharity = 'yes',
                            hasOpportunity=hasOpportunity,
                            msg=msg)
        elif session.get('is_charity', 'not set') == 0:
            #volunteer path
            cursor.execute('SELECT opportunity.opportunity_id, opportunity.title, opportunity.discription, opportunity.day_needed, opportunity.start_time, opportunity.finish_time, opportunity.poster_id FROM opportunity INNER JOIN enrolled ON opportunity.opportunity_id=enrolled.opportunity_id WHERE enrolled.user_id = %s', (session.get('id', 'not set'),))
            sqlopportunities = cursor.fetchall()
            check = cursor.rowcount
            opportunities = []
            if check != 0:
                hasOpportunity = True
                for opportunity in sqlopportunities:
                    length = 160
                    str2display = opportunity[2]
                    if len(opportunity[2]) > length:
                        str2display = ''
                        for i in range(length):
                            str2display += opportunity[2][i]
                        str2display += '...'
                    hold = [opportunity[0],opportunity[1],str2display,opportunity[3],opportunity[4],opportunity[5],opportunity[6]]  
                    opportunities += [hold]
            else:
                hasOpportunity = False
            return render_template('charityOpportunities.html',
                            opportunities=opportunities,
                            user_id=session.get('id', 'not set'),
                            isCharity = 'no',
                            hasOpportunity=hasOpportunity,
                            msg=msg)
        else:
            return redirect(url_for('logout'))
        msg = session.get('is_charity', 'not set')
        return redirect(url_for('home'))

@app.route('/opportunity', methods=['GET', 'POST'])
def opportunity():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if (request.method == 'POST' and 'opportinity_id' in request.form) or request.args.get('opportinity_id') != None:
            msg = ''
            if session.get('is_charity', 'not set') == 0:
                isCharity = 'no'
            else:
                isCharity = 'yes'
            if request.args.get('opportinity_id') != None:
                opportinity_id = request.args.get('opportinity_id')
            else:    
                opportinity_id = request.form['opportinity_id']
            if request.args.get('msg') != None:
                msg = request.args.get('msg')
            else:    
                msg = ''
            cursor = mycursor
            cursor.reset()
            cursor.execute('SELECT opportunity.poster_id, opportunity.title, opportunity.discription, opportunity.has_dbs, opportunity.day_needed, opportunity.start_time, opportunity.finish_time, opportunity.address_id, users.real_name FROM opportunity INNER JOIN users ON opportunity.poster_ID=users.user_ID WHERE opportunity.opportunity_id = %s', (opportinity_id,))
            opportinity = cursor.fetchone()
            isEmpty = 0
            cursor.execute('SELECT ad_line1, ad_line2, city, county, postcode FROM addresses WHERE address_id = %s', (opportinity[7],))
            addressFetch = cursor.fetchall()
            isEmpty = cursor.rowcount            
            address = [[],[],[],[],[]]
            if isEmpty != 0:
                addressFetch = addressFetch[0]
                c = 0
                for i in addressFetch:
                    address[c] = i
                    c += 1
            dbs = ''
            if opportinity[3] == 1:
                dbs = 'Yes'
            if opportinity[3] == 0:
                dbs = 'No'
            cursor.execute('SELECT interests.interest, interests.interest_id FROM interests INNER JOIN opportunity2interest ON interests.interest_id=opportunity2interest.interest_id WHERE opportunity2interest.opportunity_id = %s', (opportinity_id,))
            opportinityInterests = cursor.fetchall()
            if opportinity[0] == session.get('id', 'not set'):
                charity = session.get('username', 'not set')
                cursor.execute('SELECT users.username, applied.why, applied.user_id, applied.applied_id, applied.opportunity_id, users.real_name FROM applied INNER JOIN users ON applied.user_id=users.user_id WHERE applied.opportunity_id = %s', (opportinity_id,))
                sqlapplicants = cursor.fetchall()
                applicants = []
                check = cursor.rowcount
                if check == 0:
                    hasApplicant = False
                else:
                    hasApplicant = True
                cursor.execute('SELECT reference_request.reference_request_id, users.real_name, users.user_id FROM reference_request INNER JOIN users ON reference_request.user_id=users.user_id WHERE opportunity_id = %s', (opportinity_id,))
                referenceRequests = cursor.fetchall()
                check = cursor.rowcount
                if check == 0:
                    referenceRequests = []
                    hasRequest = False
                else:
                    hasRequest = True
                test = []
                for applicant in sqlapplicants:
                    length = 130
                    str2display = applicant[1]
                    if len(applicant[1]) > length:
                        str2display = ''
                        for i in range(length):
                            str2display += applicant[1][i]
                        str2display += '...'
                    hold = [applicant[5],str2display,applicant[2],applicant[3],applicant[4]]  
                    applicants += [hold]
                cursor.execute('SELECT interest_id, interest FROM interests')
                interests = cursor.fetchall()
                return render_template('myOpportunity.html',
                                opportinity=opportinity,
                                applicants=applicants,
                                opportinity_id=opportinity_id,
                                charity=charity,
                                interests=interests,
                                opportinityInterests=opportinityInterests,
                                address=address,
                                dbs=dbs,
                                referenceRequests=referenceRequests,
                                msg=msg,
                                user_id=session.get('id', 'not set'),
                                isCharity = isCharity,
                                hasRequest=hasRequest,
                                hasApplicant=hasApplicant)
            else:
                cursor.execute('SELECT opportunity_id FROM enrolled WHERE user_id = %s', (session.get('id', 'not set'),))
                enrolled = cursor.fetchall()
                enCheck = cursor.rowcount
                if enCheck == 0:
                    enrolled = [[0]]
                test = []
                for e in enrolled:
                    if int(opportinity_id) in e:
                        return render_template('enrolledOpportinity.html',
                                                opportinity=opportinity,
                                                opportinity_id=opportinity_id,
                                                opportinityInterests=opportinityInterests,
                                                address=address,
                                                dbs=dbs,
                                                msg=msg,
                                                user_id=session.get('id', 'not set'),
                                                isCharity = isCharity)
                return render_template('opportunity.html',
                                        opportinity=opportinity,
                                        opportinity_id=opportinity_id,
                                        opportinityInterests=opportinityInterests,
                                        address=address,
                                        dbs=dbs,
                                        msg=msg,
                                        user_id=session.get('id', 'not set'),
                                        isCharity = isCharity)
                msg = test
                return render_template('account.html', 
                                        msg=msg,
                                        user_id=session.get('id', 'not set'),
                                        isCharity = isCharity)
            return  redirect(url_for('home'))
        return redirect(url_for('home'))

@app.route('/editOpportunity', methods=['GET', 'POST'])
def editOpportunity():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'opportinity_id' in request.form:
            opportinity_id = request.form['opportinity_id']
            msg = ''
            if session.get('is_charity', 'not set') == 0:
                isCharity = 'no'
            else:
                isCharity = 'yes'
            change = False
            isFirst = True
            querry = 'UPDATE opportunity SET'
            inputs = '('
            if 'title' in request.form:
                title = request.form['title']
                change = True
                if title != '':
                    if '"' in title:
                        msg = "Please don't use quotation marks"
                        return render_template('editOpportunity.html', 
                                                opportinity_id=opportinity_id, 
                                                msg=msg,
                                                user_id=session.get('id', 'not set'),
                                                isCharity = isCharity)
                    else:
                        change = True
                        querry += ' title = '  
                        querry += "'" + title + "'"
                        isFirst = False
            if 'discription' in request.form:
                discription = request.form['discription']
                change = True
                if discription != '':
                    if '"' in discription:
                        msg = "Please don't use quotation marks"
                        return render_template('editOpportunity.html', 
                                                opportinity_id=opportinity_id, 
                                                msg=msg,
                                                user_id=session.get('id', 'not set'),
                                                isCharity = isCharity)
                    else:
                        if isFirst == False:
                            querry += ','  
                        querry += ' discription = ' 
                        querry += '"' + discription + '"'
                        isFirst = False
            if 'dbs' in request.form:
                dbs = request.form['dbs']
                if dbs == 'yes':
                    dbs = '1'
                if dbs == 'no':
                    dbs = '0'
                change = True
                if isFirst == False:
                    querry += ','  
                querry += " has_dbs = " 
                querry += dbs
                isFirst = False
            if 'day' in request.form:
                day = request.form['day']
                if day != 'Any':
                    change = True
                    if isFirst == False:
                        querry += ','  
                    querry += ' day_needed = ' 
                    querry += '"' + day + '"'
                    isFirst = False
            if 's_hour' in request.form and 's_minute' in request.form:
                s_hour = request.form['s_hour']
                s_minute = request.form['s_minute']
                if s_hour != 'Any' and s_minute != 'Any':
                    s_time = s_hour + ':' + s_minute + ':00'
                    change = True
                    if isFirst == False:
                        querry += ','  
                    querry += ' start_time = ' 
                    querry += '"' + s_time + '"'
                    isFirst = False
                elif (s_hour == 'Any' and s_minute != 'Any') or (s_hour != 'Any' and s_minute == 'Any'):
                    msg = "Please enter both hour and minute for start time"
                    return redirect(url_for('opportunity',opportinity_id=opportinity_id,msg=msg))
            if 'f_hour' in request.form and 'f_minute' in request.form:
                f_hour = request.form['f_hour']
                f_minute = request.form['f_minute']
                if f_hour != 'Any' and f_minute != 'Any':
                    f_time = f_hour + ':' + f_minute + ':00'
                    change = True
                    if isFirst == False:
                        querry += ','  
                    querry += ' finish_time = ' 
                    querry += '"' + f_time + '"'
                    isFirst = False
                elif (f_hour == 'Any' and f_minute != 'Any') or (f_hour != 'Any' and f_minute == 'Any'):
                    msg = "Please enter both hour and minute for end time"
                    return redirect(url_for('opportunity',opportinity_id=opportinity_id,msg=msg))
            cursor = mycursor
            cursor.execute('SELECT poster_id FROM opportunity WHERE opportunity_id = %s', (opportinity_id,))
            poster_id = cursor.fetchall()
            check = cursor.rowcount
            if check != 0:
                poster_id = poster_id[0][0]
                if poster_id == session.get('id', 'not set'):
                    if change == False:
                        msg = 'Fill out form'
                        return render_template('editOpportunity.html', 
                                                opportinity_id=opportinity_id, 
                                                msg=msg,
                                                user_id=session.get('id', 'not set'),
                                                isCharity = isCharity)
                    elif change == True:
                        querry += ' WHERE opportunity_id = '
                        querry += opportinity_id
                        cursor.execute(querry)
                        conn.commit()
                        return redirect(url_for('opportunity',opportinity_id=opportinity_id,msg=msg))
                msg = "You can't edit this opportunity"
                return redirect(url_for('opportunity',opportinity_id=opportinity_id,msg=msg))
            return redirect(url_for('home'))
        return redirect(url_for('home'))

@app.route('/viewApplication', methods=['GET', 'POST'])
def viewApplication():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'application_id' in request.form:
            if session.get('is_charity', 'not set') == 0:
                isCharity = 'no'
            else:
                isCharity = 'yes'
            cursor = mycursor
            application_id = request.form['application_id']
            cursor.execute('SELECT applied.applied_id, users.username, users.email, users.phone, users.real_name, applied.why, applied.opportunity_id FROM users INNER JOIN applied ON users.user_id = applied.user_id WHERE applied.applied_id = %s',(application_id,))
            application = cursor.fetchall()
            application = application[0]
            return render_template('viewApplication.html', application=application,
                                    user_id=session.get('id', 'not set'),
                                    isCharity = isCharity)
        return redirect(url_for('myOpportunities'))

@app.route('/requestReference', methods=['GET', 'POST'])
def requestReference():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'opportinity_id' in request.form: 
            cursor = mycursor
            opportinity_id = request.form['opportinity_id']
            cursor.execute('SELECT poster_id FROM opportunity WHERE opportunity_id = %s',(opportinity_id,))
            poster_id = cursor.fetchall()
            poster_id = poster_id[0]
            cursor.execute('SELECT reference_request_id FROM reference_request WHERE opportunity_id = %s AND charity_id = %s AND user_id = %s',(opportinity_id,poster_id[0],session.get('id', 'not set'),))
            collection = cursor.fetchall()
            isEmpty = cursor.rowcount
            if isEmpty == 0:
                
                cursor.execute('INSERT INTO reference_request (user_id,charity_id,opportunity_id) VALUES (%s,%s,%s)', (session.get('id', 'not set'),poster_id[0],opportinity_id,))
                conn.commit()
                
                #Find 1-2-1 chat
                cursor.execute('SELECT COUNT(user_id), chat_id FROM participants WHERE user_id = %s OR user_id = %s GROUP BY chat_id', (poster_id[0],session.get('id', 'not set'),)) 
                chats2look = cursor.fetchall()
                cursor.execute('SELECT chat_id FROM participants WHERE user_id = %s', (poster_id[0],))
                volenteerChats = cursor.fetchall()
                cursor.execute('SELECT participants.chat_id, users.real_name FROM participants INNER JOIN users ON users.user_id=participants.user_id WHERE participants.user_id = %s', (session.get('id', 'not set'),))
                charityChats = cursor.fetchall()
                real_name = charityChats[0][1]
                in121 = False 
                for chat in chats2look:
                    if in121 == True:
                        break
                    if chat[0] == 2:
                        for vChat in volenteerChats:
                            if in121 == True:
                                break
                            if vChat[0] == chat[1]:
                                foundVolunteer = True
                                for cChat in charityChats:
                                    if cChat[0] == chat[1]:
                                        in121 = True
                                        chat_id = cChat[0]
                                        break
            
                #Notify volunteer of enrollment
                cursor.execute('SELECT opportunity.poster_id, users.username, opportunity.title FROM opportunity INNER JOIN users ON opportunity.poster_id=users.user_id WHERE opportunity.opportunity_id = %s',(opportinity_id,))
                poster = cursor.fetchone()
                now = datetime.now()
                time = now.strftime("%Y/%m/%d %H:%M:%S")
                message = real_name
                message += ' has requested reference for '
                message += poster[2]
                cursor.execute('INSERT INTO messages (sender_id, chat_id, content, message_time)VALUES (%s, %s, %s, %s)',(session.get('id', 'not set'), chat_id, message, time,))
                conn.commit()
                cursor.execute('UPDATE chats SET update_time = %s WHERE chat_id = %s', (time, chat_id))
                conn.commit()
                msg = 'Reference requested'
                return redirect(url_for('opportunity',opportinity_id=opportinity_id,msg=msg))
            else:
                msg = 'You have already requested a reference'
                return redirect(url_for('opportunity',opportinity_id=opportinity_id,msg=msg))
            
@app.route('/writeReference', methods=['GET', 'POST'])
def writeReference():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'opportinity_id' in request.form:
            if 'request_id' in request.form:
                if session.get('is_charity', 'not set') == 0:
                    isCharity = 'no'
                else:
                    isCharity = 'yes'
                cursor = mycursor
                request_id = request.form['request_id']
                opportinity_id = request.form['opportinity_id']
                cursor.execute('SELECT reference_request_id, users.real_name, opportunity.title, users.user_id FROM reference_request INNER JOIN users ON reference_request.user_id=users.user_id INNER JOIN opportunity ON reference_request.charity_id=opportunity.poster_id WHERE opportunity.opportunity_id = %s',(opportinity_id,))
                results = cursor.fetchall()
                return render_template('writeReference.html',
                                        results=results,
                                        opportinity_id=opportinity_id,
                                        user_id=session.get('id', 'not set'),
                                        isCharity = isCharity)
            return redirect(url_for('opportunity',opportinity_id=opportinity_id))
        return redirect(url_for('opportunity'))

@app.route('/addReference', methods=['GET', 'POST'])
def addReference():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST'and 'opportinity_id' in request.form and 'reference_id' in request.form and 'user_id' in request.form and 'ref' in request.form and 'start' in request.form and 'finish' in request.form:                           
            reference_id = request.form['reference_id']
            discription = request.form['ref']
            start = request.form['start']
            finish = request.form['finish']
            user_id = request.form['user_id']
            opportinity_id = request.form['opportinity_id']
            cursor = mycursor
            cursor.execute('SELECT reference_request_id FROM reference_request WHERE reference_request_id = %s AND user_id = %s AND charity_id = %s AND opportunity_id = %s',(reference_id,user_id,session.get('id', 'not set'),opportinity_id,))
            collection = cursor.fetchall()
            check = cursor.rowcount
            if check == 0:
                redirect(url_for('opportunity',opportinity_id=opportinity_id))
            cursor.execute('INSERT INTO refs (user_id, referencer_id, content, started, finished) VALUES (%s, %s, %s, %s, %s)', (user_id,session.get('id', 'not set'),discription,start,finish,))
            conn.commit()
            cursor.execute('DELETE FROM reference_request WHERE reference_request_id = %s', (collection[0][0],))
            conn.commit()
                
            #Find 1-2-1 chat
            cursor.execute('SELECT COUNT(user_id), chat_id FROM participants WHERE user_id = %s OR user_id = %s GROUP BY chat_id', (user_id,session.get('id', 'not set'),)) 
            chats2look = cursor.fetchall()
            cursor.execute('SELECT chat_id FROM participants WHERE user_id = %s', (user_id,))
            volenteerChats = cursor.fetchall() 
            cursor.execute('SELECT participants.chat_id, users.real_name FROM participants INNER JOIN users ON users.user_id=participants.user_id WHERE participants.user_id = %s', (session.get('id', 'not set'),))
            charityChats = cursor.fetchall()
            real_name = charityChats[0][1]
            in121 = False     
            for chat in chats2look:
                if in121 == True:
                    break
                if chat[0] == 2:
                    for vChat in volenteerChats:
                        if in121 == True:
                            break
                        if vChat[0] == chat[1]:
                            foundVolunteer = True
                            for cChat in charityChats:
                                if cChat[0] == chat[1]:
                                    in121 = True
                                    chat_id = cChat[0]
                                    break
            
            #Notify volunteer of enrollment
            cursor.execute('SELECT opportunity.poster_id, users.username, opportunity.title FROM opportunity INNER JOIN users ON opportunity.poster_id=users.user_id WHERE opportunity.opportunity_id = %s',(opportinity_id,))
            poster = cursor.fetchone()
            now = datetime.now()
            time = now.strftime("%Y/%m/%d %H:%M:%S")
            message = real_name
            message += ' has writen a reference for '
            message += poster[2]
            cursor.execute('INSERT INTO messages (sender_id, chat_id, content, message_time)VALUES (%s, %s, %s, %s)',(session.get('id', 'not set'), chat_id, message, time,))
            conn.commit()
            cursor.execute('UPDATE chats SET update_time = %s WHERE chat_id = %s', (time, chat_id))
            conn.commit()
                
            return redirect(url_for('opportunity', opportinity_id=opportinity_id))
        return redirect(url_for('opportunity'))

@app.route('/myReferences', methods=['GET', 'POST'])
def myReferences():
    if "loggedin" not in session:
        return render_template('login.html')
    elif session.get('is_charity', 'not set'):
        return redirect(url_for('home')) 
        return redirect(url_for('home')) 
    else:
        if session.get('is_charity', 'not set') == 0:
            isCharity = 'no'
        else:
            isCharity = 'yes'
        cursor = mycursor
        cursor.execute('SELECT refs.referece_id, refs.content, refs.started, refs.finished, users.real_name FROM refs INNER JOIN users ON refs.referencer_id=users.user_id WHERE refs.user_id = %s', (session.get('id', 'not set'),))
        sqlreferences = cursor.fetchall()
        check = cursor.rowcount
        if check == 0:
            references = []
            hasReference = False
        else:
            references = []
            hasReference = True
            for reference in sqlreferences:
                length = 160
                str2display = ''
                if len(reference[1]) > length:
                    str2display = ''
                    for i in range(length):
                        str2display += reference[1][i]
                    str2display += '...'
                hold = [reference[0],str2display,reference[2],reference[3],reference[4]] 
                references += [hold]
            return render_template('myReferences.html', 
                                    references=references,
                                    user_id=session.get('id', 'not set'),
                                    isCharity = isCharity,
                                    hasReference=hasReference)
        return render_template('myReferences.html', 
                                references=references,
                                user_id=session.get('id', 'not set'),
                                isCharity = isCharity,
                                hasReference=hasReference)
        

@app.route('/reference', methods=['GET', 'POST'])
def reference():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'reference_id' in request.form:
            if session.get('is_charity', 'not set') == 0:
                isCharity = 'no'
            else:
                isCharity = 'yes'
            cursor = mycursor
            reference_id = request.form['reference_id']
            cursor.execute('SELECT refs.content, refs.started, refs.finished, users.real_name, refs.user_id FROM refs INNER JOIN users ON refs.referencer_id=users.user_id WHERE refs.referece_id = %s', (reference_id,))
            reference = cursor.fetchall()
            reference = reference[0]
            if reference[4] != session.get('id', 'not set'):
                return redirect(url_for('myReferences'))
            return render_template('reference.html',
                                    reference=reference,
                                    user_id=session.get('id', 'not set'),
                                    isCharity = isCharity)
        return redirect(url_for('myReferences'))

@app.route('/rejectReference', methods=['GET', 'POST'])
def rejectReference():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'request_id' in request.form and 'user_id' in request.form and 'opportinity_id' in request.form:
            cursor = mycursor
            request_id = request.form['request_id']
            user_id = request.form['user_id']
            opportinity_id = request.form['opportinity_id']
            cursor.execute('DELETE FROM reference_request WHERE reference_request_id = %s',(request_id,))
            conn.commit()
            
            #Find 1-2-1 chat
            cursor.execute('SELECT COUNT(user_id), chat_id FROM participants WHERE user_id = %s OR user_id = %s GROUP BY chat_id', (user_id,session.get('id', 'not set'),)) 
            chats2look = cursor.fetchall()
            cursor.execute('SELECT chat_id FROM participants WHERE user_id = %s', (user_id,))
            volenteerChats = cursor.fetchall() 
            cursor.execute('SELECT participants.chat_id, users.real_name FROM participants INNER JOIN users ON users.user_id=participants.user_id WHERE participants.user_id = %s', (session.get('id', 'not set'),))
            charityChats = cursor.fetchall()
            real_name = charityChats[0][1]
            in121 = False     
            for chat in chats2look:
                if in121 == True:
                    break
                if chat[0] == 2:
                    for vChat in volenteerChats:
                        if in121 == True:
                            break
                        if vChat[0] == chat[1]:
                            foundVolunteer = True
                            for cChat in charityChats:
                                if cChat[0] == chat[1]:
                                    in121 = True
                                    chat_id = cChat[0]
                                    break
        
            #Notify volunteer of enrollment
            cursor.execute('SELECT opportunity.poster_id, users.username, opportunity.title FROM opportunity INNER JOIN users ON opportunity.poster_id=users.user_id WHERE opportunity.opportunity_id = %s',(opportinity_id,))
            poster = cursor.fetchone()
            now = datetime.now()
            time = now.strftime("%Y/%m/%d %H:%M:%S")
            message = real_name
            message += ' has been rejected request for '
            message += poster[2]
            cursor.execute('INSERT INTO messages (sender_id, chat_id, content, message_time)VALUES (%s, %s, %s, %s)',(session.get('id', 'not set'), chat_id, message, time,))
            conn.commit()
            cursor.execute('UPDATE chats SET update_time = %s WHERE chat_id = %s', (time, chat_id))
            conn.commit()
            
            return redirect(url_for('opportunity',opportinity_id=opportinity_id))
        return redirect(url_for('home'))

@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'opportinity_id' in request.form and 'application_id' in request.form:
            if session.get('is_charity', 'not set') == 0:
                isCharity = 'no'
            else:
                isCharity = 'yes'
            cursor = mycursor
            opportinity_id = request.form['opportinity_id']
            application_id = request.form['application_id']
            cursor.execute('SELECT applied.user_id, users.real_name FROM applied INNER JOIN users ON applied.user_id = users.user_id WHERE applied_id = %s', (application_id,))
            user = cursor.fetchall()
            user = user[0]
            cursor.execute('INSERT INTO enrolled (user_id,opportunity_id) VALUES (%s,%s)', (user[0],opportinity_id,))
            conn.commit()
            cursor.execute('DELETE FROM applied WHERE applied_id=%s', (application_id,))
            conn.commit()

            #Find 1-2-1 chat
            cursor.execute('SELECT COUNT(user_id), chat_id FROM participants WHERE user_id = %s OR user_id = %s GROUP BY chat_id', (user[0],session.get('id', 'not set'),)) 
            chats2look = cursor.fetchall()
            cursor.execute('SELECT chat_id FROM participants WHERE user_id = %s', (user[0],))
            volenteerChats = cursor.fetchall()
            cursor.execute('SELECT chat_id FROM participants WHERE user_id = %s', (session.get('id', 'not set'),))
            charityChats = cursor.fetchall()
            in121 = False     
            for chat in chats2look:
                if in121 == True:
                    break
                if chat[0] == 2:
                    for vChat in volenteerChats:
                        if in121 == True:
                            break
                        if vChat[0] == chat[1]:
                            foundVolunteer = True
                            for cChat in charityChats:
                                if cChat[0] == chat[1]:
                                    in121 = True
                                    chat_id = cChat[0]
                                    break
        
            #Notify volunteer of enrollment
            cursor.execute('SELECT opportunity.poster_id, users.username, opportunity.title FROM opportunity INNER JOIN users ON opportunity.poster_id=users.user_id WHERE opportunity.opportunity_id = %s',(opportinity_id,))
            poster = cursor.fetchone()
            now = datetime.now()
            time = now.strftime("%Y/%m/%d %H:%M:%S")
            message = user[1]
            message += ' has been enrolled into: '
            message += poster[2]
            cursor.execute('INSERT INTO messages (sender_id, chat_id, content, message_time)VALUES (%s, %s, %s, %s)',(session.get('id', 'not set'), chat_id, message, time,))
            conn.commit()
            cursor.execute('UPDATE chats SET update_time = %s WHERE chat_id = %s', (time, chat_id))
            conn.commit()
            
            #Add to group chat
            cursor.execute('SELECT chat_id FROM opportunity2chat WHERE opportunity_id = %s', (opportinity_id,))
            chat_id = cursor.fetchall()
            chat_id = chat_id[0][0]
            cursor.execute('INSERT INTO participants (chat_id,user_id) VALUES (%s,%s)', (chat_id,user[0],))
            conn.commit()
            
            #Welcome to Group chat
            message = 'Welcome '
            message += user[1]
            cursor.execute('INSERT INTO messages (sender_id, chat_id, content, message_time)VALUES (%s, %s, %s, %s)',(session.get('id', 'not set'), chat_id, message, time,))
            conn.commit()
            cursor.execute('UPDATE chats SET update_time = %s WHERE chat_id = %s', (time, chat_id))
            conn.commit()
            
            return redirect(url_for('opportunity',opportinity_id=opportinity_id))
        return redirect(url_for('home'))

@app.route('/removeOpportunity', methods=['GET', 'POST'])
def removeOpportunity():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'opportinity_id' in request.form:
            cursor = mycursor
            opportinity_id = request.form['opportinity_id']
            cursor.execute('SELECT poster_id FROM opportunity WHERE opportunity_id = %s', (opportinity_id,))
            poster_id = cursor.fetchall()
            poster_id = poster_id[0]
            cursor.execute('SELECT enrolled.user_id, users.real_name FROM enrolled INNER JOIN users ON enrolled.user_id=users.user_id WHERE enrolled.opportunity_id = %s', (opportinity_id,))
            users = cursor.fetchall()
            cursor.execute('SELECT chat_id FROM opportunity2chat WHERE opportunity_id = %s', (opportinity_id,))
            chat_id = cursor.fetchall()
            chat_id = chat_id[0]
            if poster_id[0] == session.get('id', 'not set'):
                cursor.execute('DELETE FROM opportunity WHERE opportunity_id = %s', (opportinity_id,))
                conn.commit()
                cursor.execute('DELETE FROM participants WHERE chat_id = %s', (chat_id[0],))
                conn.commit()
                cursor.execute('DELETE FROM opportunity2chat WHERE opportunity_id = %s', (opportinity_id,))
                conn.commit()
                cursor.execute('DELETE FROM opportunity2interest WHERE opportunity_id = %s', (opportinity_id,))
                conn.commit()
                cursor.execute('DELETE FROM chats WHERE chat_id = %s', (chat_id[0],))
                conn.commit()
                cursor.execute('DELETE FROM messages WHERE chat_id = %s', (chat_id[0],))
                conn.commit()
                cursor.execute('DELETE FROM applied WHERE opportunity_id = %s', (opportinity_id,))
                conn.commit()
                msg = 'You have deleted this opportunity'
                return redirect(url_for('myOpportunities',msg=msg))
            else:
                for user in users:
                    if session.get('id', 'not set') in user:
                        cursor.execute('DELETE FROM participants WHERE chat_id = %s AND user_id = %s', (chat_id[0],session.get('id', 'not set'),))
                        conn.commit()
                        cursor.execute('DELETE FROM enrolled WHERE user_id = %s AND opportunity_id = %s', (session.get('id', 'not set'),opportinity_id,))
                        conn.commit()
                        
                        cursor.execute('SELECT users.real_name FROM opportunity INNER JOIN users ON opportunity.poster_id=users.user_id WHERE poster_id=%s',(poster_id[0],))
                        charUsername = cursor.fetchall()
                        charUsername = charUsername[0][0]
                        chatName = ''
                        chatName += charUsername + ' - ' + user[1]
                        
                        cursor.execute('SELECT chat_id FROM chats WHERE chat_name = %s', (chatName,))
                        chat_id = cursor.fetchall()
                        chat_id = chat_id[0][0]
                        
                        now = datetime.now()
                        time = now.strftime("%Y/%m/%d %H:%M:%S")
                        message = session.get('username', 'not set')
                        message += ' has withdrawn from this opportinity'
                        cursor.execute('INSERT INTO messages (sender_id, chat_id, content, message_time)VALUES (%s, %s, %s, %s)',(session.get('id', 'not set'), chat_id, message, time,))
                        conn.commit()
                        cursor.execute('UPDATE chats SET update_time = %s WHERE chat_id = %s', (time, chat_id))
                        conn.commit()
                        msg = 'You have withdrawn from this opportunity'
                        return redirect(url_for('myOpportunities',msg=msg))
        msg = 'No opportunity selected'
        return redirect(url_for('myOpportunities',msg=msg))   
                
@app.route('/reject', methods=['GET', 'POST'])
def reject():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'opportinity_id' in request.form and 'application_id' in request.form:
            if session.get('is_charity', 'not set') == 0:
                isCharity = 'no'
            else:
                isCharity = 'yes'
            cursor = mycursor
            opportinity_id = request.form['opportinity_id']
            application_id = request.form['application_id']
            cursor.execute('SELECT user_id FROM applied WHERE applied_id = %s', (application_id,))
            user = cursor.fetchall()
            user = user[0]
            cursor.execute('DELETE FROM applied WHERE applied_id=%s', (application_id,))
            conn.commit()

            #Find 1-2-1 chat
            cursor.execute('SELECT COUNT(user_id), chat_id FROM participants WHERE user_id = %s OR user_id = %s GROUP BY chat_id', (user[0],session.get('id', 'not set'),)) 
            chats2look = cursor.fetchall()
            cursor.execute('SELECT chat_id FROM participants WHERE user_id = %s', (user[0],))
            volenteerChats = cursor.fetchall()
            cursor.execute('SELECT chat_id FROM participants WHERE user_id = %s', (session.get('id', 'not set'),))
            charityChats = cursor.fetchall()
            in121 = False     
            for chat in chats2look:
                if in121 == True:
                    break
                if chat[0] == 2:
                    for vChat in volenteerChats:
                        if in121 == True:
                            break
                        if vChat[0] == chat[1]:
                            foundVolunteer = True
                            for cChat in charityChats:
                                if cChat[0] == chat[1]:
                                    in121 = True
                                    chat_id = cChat[0]
                                    break
        
            #Notify volunteer of enrollment
            cursor.execute('SELECT opportunity.poster_id, users.username, opportunity.title FROM opportunity INNER JOIN users ON opportunity.poster_id=users.user_id WHERE opportunity.opportunity_id = %s',(opportinity_id,))
            poster = cursor.fetchone()
            now = datetime.now()
            time = now.strftime("%Y/%m/%d %H:%M:%S")
            message = session.get('username', 'not set')
            message += ' has been rejected from: '
            message += poster[2]
            cursor.execute('INSERT INTO messages (sender_id, chat_id, content, message_time)VALUES (%s, %s, %s, %s)',(session.get('id', 'not set'), chat_id, message, time,))
            conn.commit()
            cursor.execute('UPDATE chats SET update_time = %s WHERE chat_id = %s', (time, chat_id))
            conn.commit()
            return redirect(url_for('opportunity',opportinity_id=opportinity_id))
        return redirect(url_for('home'))

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'opportinity_id' in request.form:
            msg = ''
            cursor = mycursor
            opportinity_id = request.form['opportinity_id']
            why = request.form['why']
            #if '"' in 
            cursor.execute('SELECT user_id FROM applied WHERE opportunity_id = %s AND user_id = %s',(opportinity_id,session.get('id', 'not set'),))
            check = cursor.fetchall()
            isEmpty = cursor.rowcount
            cursor.reset()
            if isEmpty != 0:
                if session.get('id', 'not set') in check[0]:
                    msg = 'you have already applied'
                    return redirect(url_for('opportunity',opportinity_id=opportinity_id,msg=msg))
            cursor.execute('INSERT INTO applied (opportunity_id,user_id,why) VALUES (%s, %s, %s)',(opportinity_id, session.get('id', 'not set'), why,))
            conn.commit()
            cursor.execute('SELECT opportunity.poster_id, users.username, opportunity.title, users.real_name FROM opportunity INNER JOIN users ON opportunity.poster_id=users.user_id WHERE opportunity.opportunity_id = %s',(opportinity_id,))
            poster = cursor.fetchone()
            cursor.reset()
            poster_id = poster[0]
            
            #check if users are already in 1-2-1 chat
            cursor.execute('SELECT COUNT(user_id), chat_id FROM participants WHERE user_id = %s OR user_id = %s GROUP BY chat_id', (poster_id,session.get('id', 'not set'),)) 
            chats2look = cursor.fetchall()
            cursor.execute('SELECT chat_id FROM participants WHERE user_id = %s', (poster_id,))
            charityChats = cursor.fetchall()
            cursor.execute('SELECT chat_id FROM participants WHERE user_id = %s', (session.get('id', 'not set'),))
            volenteerChats = cursor.fetchall()
            in121 = False     
            for chat in chats2look:
                if in121 == True:
                    break
                if chat[0] == 2:
                    for vChat in volenteerChats:
                        if in121 == True:
                            break
                        if vChat[0] == chat[1]:
                            foundVolunteer = True
                            for cChat in charityChats:
                                if cChat[0] == chat[1]:
                                    in121 = True
                                    chat_id = cChat[0]
                                    break
            now = datetime.now()
            time = now.strftime("%Y/%m/%d %H:%M:%S")
            
            cursor.execute('SELECT real_name FROM users WHERE user_id = %s', (session.get('id', 'not set'),))
            vol_id = cursor.fetchall()            
            
            #Not in 1-2-1
            if in121 == False:
                #Set up new chat
                chat_name = poster[3]
                chat_name += ' - '
                #return render_template('account.html',msg=msg)
                chat_name += vol_id[0][0]
                cursor.execute('INSERT INTO chats (chat_name, chat_admin_id, chat_creator_id, creation_time, update_time)VALUES (%s, %s, %s, %s, %s)',(chat_name, poster_id, poster_id, time, time,))
                conn.commit()
                cursor.execute('SELECT chat_id FROM chats WHERE creation_time = %s AND chat_creator_id = %s', (time, poster_id,))
                chat_id = cursor.fetchone()
                chat_id = chat_id[0]
                cursor.reset()
                cursor.execute('INSERT INTO participants (chat_id, user_id)VALUES (%s, %s)',(chat_id, poster_id,))
                conn.commit()
                cursor.execute('INSERT INTO participants (chat_id, user_id)VALUES (%s, %s)',(chat_id, session.get('id', 'not set'),))
                conn.commit()
                
            #Notify charity of application
            message = vol_id[0][0]
            message += ' has applied to opportinity: '
            message += poster[2]
            cursor.execute('INSERT INTO messages (sender_id, chat_id, content, message_time)VALUES (%s, %s, %s, %s)',(session.get('id', 'not set'), chat_id, message, time,))
            conn.commit()
            cursor.execute('UPDATE chats SET update_time = %s WHERE chat_id = %s', (time, chat_id))
            conn.commit()
                
            return redirect(url_for('home'))
        msg = check
        return redirect(url_for('home'))

@app.route('/applied', methods=['GET', 'POST'])
def applied():
    if "loggedin" not in session:
        return render_template('login.html')
    elif session.get('is_charity', 'not set'):
        return redirect(url_for('home'))    
    else:
        if session.get('is_charity', 'not set') == 0:
            isCharity = 'no'
        else:
            isCharity = 'yes'
        cursor = mycursor
        cursor.execute('SELECT applied.opportunity_id, opportunity.title, opportunity.discription, opportunity.day_needed, opportunity.start_time, opportunity.finish_time, opportunity.poster_id, users.real_name FROM opportunity LEFT JOIN applied ON applied.opportunity_id=opportunity.opportunity_id LEFT JOIN users ON users.user_id=opportunity.poster_id WHERE applied.user_id = %s', (session.get('id', 'not set'),))
        sqlresults = cursor.fetchall()
        check = cursor.rowcount
        results = []
        if check != 0:
            hasApplied = True
            for result in sqlresults:
                length = 160
                str2display = result[2]
                if len(result[2]) > length:
                    str2display = ''
                    for i in range(length):
                        str2display += result[2][i]
                    str2display += '...'
                hold = [result[0],result[1],str2display,result[3],result[4],result[5],result[6],result[7]]  
                results += [hold]
        else:
            hasApplied = False
        return render_template('applied.html',
                                results=results,
                                user_id=session.get('id', 'not set'),
                                isCharity = isCharity,
                                hasApplied=hasApplied)

@app.route('/removeApplied', methods=['GET', 'POST'])
def removeApplied():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'opportinity_id' in request.form:
            #Remove from applied
            opportinity_id = request.form['opportinity_id']
            cursor = mycursor
            cursor.execute('DELETE FROM applied WHERE user_id = %s AND opportunity_id = %s', (session.get('id', 'not set'), opportinity_id,)) 
            conn.commit()
            
            #Find 1-2-1 chat
            cursor.execute('SELECT poster_id FROM opportunity WHERE opportunity_id = %s', (opportinity_id,))
            poster = cursor.fetchone()
            poster_id = poster[0]
            cursor.execute('SELECT COUNT(user_id), chat_id FROM participants WHERE user_id = %s OR user_id = %s GROUP BY chat_id', (poster_id,session.get('id', 'not set'),)) 
            chats2look = cursor.fetchall()
            cursor.execute('SELECT chat_id FROM participants WHERE user_id = %s', (poster_id,))
            charityChats = cursor.fetchall()
            cursor.execute('SELECT chat_id FROM participants WHERE user_id = %s', (session.get('id', 'not set'),))
            volenteerChats = cursor.fetchall()
            in121 = False     
            for chat in chats2look:
                if in121 == True:
                    break
                if chat[0] == 2:
                    for vChat in volenteerChats:
                        if in121 == True:
                            break
                        if vChat[0] == chat[1]:
                            foundVolunteer = True
                            for cChat in charityChats:
                                if cChat[0] == chat[1]:
                                    in121 = True
                                    chat_id = cChat[0]
                                    break
        
            #Notify charity of application withdrawle
            cursor.execute('SELECT opportunity.poster_id, users.username, opportunity.title FROM opportunity INNER JOIN users ON opportunity.poster_id=users.user_id WHERE opportunity.opportunity_id = %s',(opportinity_id,))
            poster = cursor.fetchone()
            now = datetime.now()
            time = now.strftime("%Y/%m/%d %H:%M:%S")
            message = session.get('username', 'not set')
            message += ' has withdrawn from your opportinity: '
            message += poster[2]
            cursor.execute('INSERT INTO messages (sender_id, chat_id, content, message_time)VALUES (%s, %s, %s, %s)',(session.get('id', 'not set'), chat_id, message, time,))
            conn.commit()
            cursor.execute('UPDATE chats SET update_time = %s WHERE chat_id = %s', (time, chat_id))
            conn.commit()
            return redirect(url_for('applied'))
            
@app.route('/search', methods=['GET', 'POST'])
def search():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if session.get('is_charity', 'not set') == 0:
            isCharity = 'no'
        else:
            isCharity = 'yes'
        cursor = mycursor
        if request.method == 'POST':
            isFirst = True
            title = ''
            charity = ''
            maxDis = ''
            inputInterest = ''
            day = request.form['day']
            charity = request.form['charity']
            title = request.form['title']
            
            if '"' in charity or '"' in title:
                msg = "Please don't use quotation marks"
                return render_template('search.html',
                                        isCharity=isCharity,
                                        msg=msg)
                                        
            s_hour = request.form['s_hour']
            s_minute = request.form['s_minute']
            f_hour = request.form['f_hour']
            f_minute = request.form['f_minute']
            s_time = ''
            f_time = ''
            inputInterest = request.form['interest']
            maxDis = request.form['distance']
            querry = "SELECT opportunity.poster_id, opportunity.title, opportunity.discription, opportunity.has_dbs, opportunity.day_needed, opportunity.start_time, opportunity.finish_time, opportunity.address_id, users.real_name, opportunity.opportunity_id, addresses.longitude, addresses.latitude FROM opportunity LEFT JOIN users ON opportunity.poster_id=users.user_id LEFT JOIN addresses ON opportunity.address_id=addresses.address_id WHERE"
           
            querry += ' opportunity.title LIKE "%'
            querry += title
            querry += '%"'
            isFirst = False
            
            if charity != '':
                if isFirst == False:
                    querry += ' and'
                querry += ' users.real_name LIKE "%'
                querry += charity
                querry += '%"'
                isFirst = False
            
            if day != 'Any':
                if isFirst == False:
                    querry += ' and'
                querry += ' opportunity.day_needed = "'
                querry += day
                querry += '"'
                isFirst = False
                
            if s_hour != 'any':
                s_time = s_hour
                if s_minute != '0':
                    s_time += ':'
                    s_time += s_minute
                else:
                    s_time += ':00'
                s_time += ':00'
                if isFirst == False:
                    querry += ' and'
                querry += ' opportunity.start_time >= "'
                querry += s_time
                querry += '"'
                isFirst = False
            
            if f_hour != 'any':
                f_time = f_hour
                if f_minute != '0':
                    f_time += ':'
                    f_time += f_minute
                else:
                    f_time += ':45'
                f_time += ':00'
                if isFirst == False:
                    querry += ' and'
                querry += ' opportunity.finish_time <= "'
                querry += f_time
                querry += '"'
                isFirst = False
            querry += " ORDER BY title ASC"
            msg = ''
            cursor.execute(querry)
            fetchResults = cursor.fetchall()
            check = cursor.rowcount
            if check == 0:
                hasResult = False
            else:
                hasResult = True
            t1results = []
            t2results = []
            cursor.execute('SELECT addresses.longitude, addresses.latitude FROM addresses INNER JOIN users ON addresses.address_id=users.address_id WHERE users.user_id = %s', (session.get('id', 'not set'),))
            userAddress = cursor.fetchall()
            check = 0
            check = cursor.rowcount
            lastT1 = 0
            lastT2 = 0
            test = []
            if check == 0:
                maxDis = '26'
            else:
                userAddress = userAddress[0]
            for result in fetchResults:
                hold = result
                if result[10] != None or result[11] != None:
                    hold = result
                    if maxDis != '26':
                        lon1 = userAddress[0]
                        lon2 = result[10]
                        lat1 = userAddress[1]
                        lat2 = result[11]
                        
                        #Converts co-ords tp radians
                        lon1 = radians(lon1)
                        lon2 = radians(lon2)
                        lat1 = radians(lat1)
                        lat2 = radians(lat2)

                        #Apply Haversine formula
                        dlon = lon2 - lon1
                        dlat = lat2 - lat1
                        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

                        c = 2 * asin(sqrt(a))
                        r = 3956
                        distance = c * r
                        
                        if distance <= int(maxDis):
                            cursor.execute('SELECT interest_id FROM opportunity2interest WHERE opportunity_id = %s', (result[9],))
                            oppInterests = cursor.fetchall()
                            check = cursor.rowcount
                            if check != 0:
                                for i in oppInterests:
                                    if i[0] == int(inputInterest):
                                        if t1results == []:
                                            t1results += [hold]
                                        elif t1results[lastT1][9] != hold[9]:
                                            t1results += [hold]
                                            lastT1 += 1
                                    else: 
                                        if t2results == []:
                                            t2results += [hold]
                                        elif t2results[lastT2][9] != hold[9]:
                                            t2results += [hold]
                                            lastT2 += 1
                            else:
                                t2results += [hold]
                    else:
                        cursor.execute('SELECT interest_id FROM opportunity2interest WHERE opportunity_id = %s', (result[9],))
                        oppInterests = cursor.fetchall()
                        check = cursor.rowcount
                        if check != 0:
                            for i in oppInterests:
                                if i[0] == int(inputInterest):
                                    if t1results == []:
                                        t1results += [hold]
                                    elif t1results[lastT1][9] != hold[9]:
                                        t1results += [hold]
                                        lastT1 += 1
                                else: 
                                    if t2results == []:
                                        t2results += [hold]
                                    elif t2results[lastT2][9] != hold[9]:
                                        t2results += [hold]
                                        lastT2 += 1
                        else:
                            t2results += [hold]
                            
                                
            return render_template('searchResults.html', 
                                    t1results=t1results, 
                                    t2results=t2results, 
                                    msg=msg,
                                    user_id=session.get('id', 'not set'),
                                    isCharity = isCharity,
                                    hasResult=hasResult)
        cursor.execute('SELECT interest_id, interest FROM interests')
        interests = cursor.fetchall()
    if session.get('is_charity', 'not set') == 0:
        isCharity = 'no'
    else:
        isCharity = 'yes'
    return render_template('search.html',
                            interests=interests,
                            user_id=session.get('id', 'not set'),
                            isCharity = isCharity)

@app.route('/addAvadiblity', methods=['GET', 'POST'])
def addAvadiblity():
    if "loggedin" not in session:
        return render_template('login.html')
    else:
        if request.method == 'POST' and 'day' in request.form and 's_hour' in request.form and 's_minute' in request.form and 'f_hour' in request.form and 'f_minute' in request.form:
            cursor = mycursor
            day = request.form['day']
            s_hour = request.form['s_hour']
            s_minute = request.form['s_minute']
            f_hour = request.form['f_hour']
            f_minute = request.form['f_minute']
            s_time = '"' + s_hour + ':' + s_minute + ':00"'
            f_time = '"' + f_hour + ':' + f_minute + ':00"'
            startCol = ''
            finishCol = ''
            if day == 'Monday':
                startCol = 'mon_start'
                finishCol = 'mon_finish'
            elif day == 'Tuesday':
                startCol = 'tue_start'
                finishCol = 'tue__finish'            
            elif day == 'Wednesday':
                startCol = 'wed_start'
                finishCol = 'wed__finish'            
            elif day == 'Thursday':
                startCol = 'thur_start'
                finishCol = 'thur_finish'
            elif day == 'Friday':
                startCol = 'fri_start'
                finishCol = 'fri_finish'            
            elif day == 'Saturday':
                startCol = 'sat_start'
                finishCol = 'sat_finish'
            elif day == 'Sunday':
                startCol = 'sun_start'
                finishCol = 'sun_finish'
            cursor.execute('SELECT avadibility_id FROM avadibility WHERE user_id = %s', (session.get('id', 'not set'),))
            avadibility_id = cursor.fetchall()
            avadibility_id = avadibility_id[0]
            querry = 'UPDATE avadibility SET ' + startCol + ' = ' + s_time + ', ' + finishCol + ' = ' + f_time +' WHERE avadibility_id = ' + str(avadibility_id[0])
            cursor.execute(querry)
            conn.commit()
            return redirect(url_for('account'))
            

@app.route('/')
def index():
    if "loggedin" in session:
        return redirect(url_for('home'))
    return render_template('login.html')
    
@app.route('/home')
def home():
    if "loggedin" in session:
        if session.get('is_charity', 'not set') == 0:
            isCharity = 'no'
            empty = True
            cursor = mycursor
            cursor.execute('SELECT users.has_dbs, addresses.longitude, addresses.latitude, user2interest.interest_id, users.max_distance FROM users LEFT JOIN addresses ON users.address_id=addresses.address_id LEFT JOIN user2interest ON user2interest.user_id=users.user_id WHERE users.user_id = %s', (session.get('id', 'not set'),))
            fetchUserDetails = cursor.fetchall()
            hasAd = False
            if fetchUserDetails[0][1] != None and fetchUserDetails[0][2] != None:
                hasAd = True
            userDetails = [[fetchUserDetails[0][1]],[fetchUserDetails[0][2]]]
            userInterests = []
            maxDis = fetchUserDetails[0][4]
            for i in fetchUserDetails:
                userInterests += [i[3]]
            userDetails += [userInterests]
            userDetails += [maxDis]
            querry = 'SELECT opportunity.opportunity_id, opportunity.title, users.real_name, opportunity.discription, opportunity.day_needed, opportunity.start_time, opportunity.finish_time, addresses.longitude, addresses.latitude FROM opportunity LEFT JOIN addresses ON opportunity.address_id=addresses.address_id LEFT JOIN users ON opportunity.poster_id=users.user_id'
            if fetchUserDetails[0][0] == 0:
                querry += ' WHERE opportunity.has_dbs = 0'
            cursor.execute(querry)
            opportunityDetails = cursor.fetchall()
            odCheck = cursor.rowcount
            if odCheck == 0:
                msg = 'No recomended opportunities within your travel distance, avadibility, and DBS critiria'
                return render_template('home.html', 
                                        msg=msg,
                                        empty=empty,
                                        user_id=session.get('id', 'not set'),
                                        isCharity = isCharity)
            
            results = []
            scores = [[0,0]]
            cursor.execute('SELECT * FROM avadibility WHERE user_id = %s', (session.get('id', 'not set'),))
            fetchedUserAvadibility = cursor.fetchall()
            check = cursor.rowcount
            if check == 0:
                freshT = '00:00:00'
                cursor.execute('INSERT INTO avadibility VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (session.get('id', 'not set'), freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT, freshT,))
                conn.commit()
                cursor.execute('SELECT * FROM avadibility WHERE user_id = %s', (session.get('id', 'not set'),))
                fetchedUserAvadibility = cursor.fetchall()
            fetchedUserAvadibility = fetchedUserAvadibility[0]
            
            cursor.execute('SELECT opportunity_id FROM applied WHERE user_id = %s',(session.get('id', 'not set'),))
            applied = cursor.fetchall()
            apCheck = cursor.rowcount
            if apCheck == 0:
                applied = [[0]]
            cursor.execute('SELECT opportunity_id FROM enrolled WHERE user_id = %s',(session.get('id', 'not set'),))
            enrolled = cursor.fetchall()
            enCheck = cursor.rowcount
            if enCheck == 0:
                enrolled = [[0]]           
            
            for i in opportunityDetails:
                if i[4] == 'Monday':
                    userAvadibility = [fetchedUserAvadibility[2],fetchedUserAvadibility[3]]
                elif i[4] == 'Tuesday':
                    userAvadibility = [fetchedUserAvadibility[4],fetchedUserAvadibility[5]]
                elif i[4] == 'Wednesday':
                    userAvadibility = [fetchedUserAvadibility[6],fetchedUserAvadibility[7]]
                elif i[4] == 'Thursday':
                    userAvadibility = [fetchedUserAvadibility[8],fetchedUserAvadibility[9]]
                elif i[4] == 'Friday':
                    userAvadibility = [fetchedUserAvadibility[10],fetchedUserAvadibility[11]]
                elif i[4] == 'Saturday':
                    userAvadibility = [fetchedUserAvadibility[12],fetchedUserAvadibility[13]]
                elif i[4] == 'Sunday':
                    userAvadibility = [fetchedUserAvadibility[14],fetchedUserAvadibility[15]]
            
            #msg = hasAd
            #return render_template('account.html',msg=msg)
            
                if userDetails[0] != None and userDetails[1] != None and hasAd == True:
                #for i in opportunityDetails: 
                    if i[5] >= userAvadibility[0] and i[6] <= userAvadibility[1]:
                        for a in applied:
                            if a[0] == i[0]:
                                break
                            for e in enrolled:
                                if e[0] != i[0]:
                                    scores += [0,0]
                                    lon1 = userDetails[0][0]
                                    lon2 = i[7]
                                    lat1 = userDetails[1][0]
                                    lat2 = i[8]                  
                                    lon1 = radians(lon1)
                                    lon2 = radians(lon2)
                                    lat1 = radians(lat1)
                                    lat2 = radians(lat2)
                                    dlon = lon2 - lon1
                                    dlat = lat2 - lat1
                                    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                                    c = 2 * asin(sqrt(a))
                                    r = 3956
                                    distance = c * r                           
                                    if distance < userDetails[3]:
                                        cursor.execute('SELECT interest_id FROM opportunity2interest WHERE opportunity_id = %s', (i[0],))
                                        oppInterests = cursor.fetchall()
                                        check = cursor.rowcount
                                        score = 0.5
                                        if check != 0:
                                            for y in oppInterests:                                                 
                                                if y[0] in userDetails[2]:
                                                    score += 4
                                        if distance == 0:
                                            distance = 0.1
                                        
                                        distance = 1/distance
                                        score = score * distance 
                                         
                                        hold = []
                                        for x in i:
                                            hold += [x]
                                        hold += [score]
                                        if hold in results:
                                            msg = ''
                                        else:
                                            results += [hold]
                                        empty = False
                results = sorted(results, key=itemgetter(9), reverse=True)
            if request.args.get('msg') != None:
                msg = request.args.get('chat_id')
            elif hasAd == False:
                msg = 'Please add address'
            else:
                msg = ''
            return render_template('home.html',
                                    msg=msg,
                                    results=results,
                                    empty=empty,
                                    user_id=session.get('id', 'not set'),
                                    isCharity = isCharity)
        else:
            return redirect(url_for('myOpportunities'))
    return render_template('login.html')