from flask import Flask, flash, render_template, request, redirect, url_for, session
from auth import auth
from arrivals import get_arrivals
from reservation import get_reservation_by_id

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['PERMANENT_SESSION_LIFETIME'] = 900

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    Auth = auth(username, password)

    if Auth != False:
        
        session['logged_in'] = True
        rid = "H5519"
        session['rid'] = rid

        session['data'] = {
            "rid":rid,
            'token': Auth['token']
        }

        return redirect(url_for('arrivals'))
    else:
        flash('Incorreto ou não permitido.', 'danger')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('rid', None)
    return redirect(url_for('login'))

@app.route('/arrivals', methods=['GET', 'POST'])
def arrivals():
    data = session['data']

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        data['arrivals'] = get_arrivals(data['rid'], data['token'])

        if data['arrivals'] != False:
        #    print(data['arrivals'])
           return render_template('arrivals.html', data=data) 

    return render_template('arrivals.html')

@app.route('/<rid>/reservas/<resvId>', methods=['GET', 'POST'])
def reserva(rid, resvId):
    
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if rid == session['data']['rid']:

        main_resv = get_reservation_by_id(session['data']['rid'], resvId, session['data']['token'])

        session['data']['reservations'] = []
        session['data']['reservations'].append(main_resv)

        for share in main_resv.get('reservations',{}).get('reservation', {})[0].get('sharedGuests', []):
            shareId = share['profileId']['id']
            session['data']['reservations'].append(get_reservation_by_id(session['data']['rid'], shareId, session['data']['token']))

        shares = main_resv.get('reservations',{}).get('reservation', {})[0].get('sharedGuests', [])

        res = session['data']['reservations']
        t_adults = sum([int(x['reservations']['reservation'][0]['roomStay']['guestCounts']['adults']) for x in session['data']['reservations'] if x['reservations']['reservation'][0]['computedReservationStatus'] != "Cancelled" ])
        if t_adults > len(shares):
            session['data']['reservations_to_add'] = [x for x in range(t_adults - len(session['data']['reservations']))]
        else:
            session['data']['reservations_to_add'] = []

        data = session['data']
        # return data['reservations'][0]
        return render_template('reserva.html', data=data)
    
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
