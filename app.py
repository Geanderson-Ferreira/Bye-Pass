from flask import Flask, flash, render_template, request, redirect, url_for, session
from src.auth import auth
from src.arrivals import get_arrivals
from src.reservation import get_reservation_by_id
from src.registration_card import get_fnrh
from src.profiles import get_profile_by_id
from flask import Flask, send_file, make_response
import base64
import io

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
        rid = "HB8P5"
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
            # return data['arrivals']
            return render_template('arrivals.html', data=data) 

    return render_template('arrivals.html')

@app.route('/<rid>/reservas/<resvId>', methods=['GET', 'POST'])
def reserva(rid, resvId):
    #Dados previstos de retorno session['data']

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if rid == session['data']['rid']:

        main_resv = get_reservation_by_id(session['data']['rid'], resvId, session['data']['token'])
        main_resv['profile'] = get_profile_by_id(main_resv['reservations']['reservation'][0]['reservationGuests'][0]['profileInfo']['profileIdList'][0]['id'], session['data']['token'], session['data']['rid'])

        session['data']['reservations'] = []
        session['data']['reservations'].append(main_resv)

        for share in main_resv.get('reservations',{}).get('reservation', {})[0].get('sharedGuests', []):
            shareId = share['profileId']['id']
            resvShare = get_reservation_by_id(session['data']['rid'], shareId, session['data']['token'])
            resvShare['profile'] = get_profile_by_id(resvShare['reservations']['reservation'][0]['reservationGuests'][0]['profileInfo']['profileIdList'][0]['id'], session['data']['token'], session['data']['rid'])
            session['data']['reservations'].append(resvShare)

        shares = main_resv.get('reservations',{}).get('reservation', {})[0].get('sharedGuests', [])

        #Soma do total de Adultos
        t_adults = sum([int(x['reservations']['reservation'][0]['roomStay']['guestCounts']['adults']) for x in session['data']['reservations'] if x['reservations']['reservation'][0]['computedReservationStatus'] != "Cancelled" ])
        
        #Logica de reservations to add
        if t_adults > len(shares):
            session['data']['reservations_to_add'] = [x for x in range(t_adults - len(session['data']['reservations']))]
        else:
            session['data']['reservations_to_add'] = []

        # return session['data']['reservations'][0]['profile']
        # return main_resv['reservations']['reservation'][0]['reservationGuests'][0]['profileInfo']['profileIdList'][0]['id']
        return render_template('reserva.html', data=session['data'])

    else:
        return redirect(url_for('login'))
    
@app.route('/<resvId>/registration_card')
def show_registration_card(resvId):

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    fnrh = get_fnrh(session['data']['rid'], resvId, session['data']['token'])['registrationCard']['registrationCard']

    decoded_pdf = base64.b64decode(fnrh)

    flask_response = make_response(decoded_pdf)
    flask_response.headers['Content-Type'] = 'application/pdf'
    flask_response.headers['Content-Disposition'] = 'inline; filename=registration_card.pdf'

    return flask_response

if __name__ == '__main__':
    app.run(debug=True)