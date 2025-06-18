# using blueprint
from flask import Blueprint, render_template, request, jsonify, session
import datetime
from app.models import db

patient_bp = Blueprint('patient', __name__, template_folder='templates', static_folder='static')


@patient_bp.route('/patient', methods=['GET'])
def patient():
    return render_template('patient/patient.html')


# Show appointments page
@patient_bp.route('/patient/appointments', methods=['GET'])
def appointments():
    return render_template('patient/appointments.html')


# API: Get all appointments for the logged-in patient
@patient_bp.route('/patient/api/appointments', methods=['GET'])
def get_appointments():
    # For demo, get patient_id from query or session (replace with real auth in production)
    patient_id = 1
    conn, cursor = db()
    cursor.execute("SELECT * FROM appointment WHERE patient_id=%s ORDER BY date DESC, time DESC", (patient_id,))
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(appointments)


# API: Get open clinic days (for calendar)
@patient_bp.route('/patient/api/open-days', methods=['GET'])
def get_open_days():
    conn, cursor = db()
    cursor.execute("SELECT day FROM clinic_days WHERE status='open'")
    days = [row['day'] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(days)


# API: Get available times (for time slots) for a specific date
@patient_bp.route('/patient/api/available-times', methods=['GET'])
def get_available_times():
    date = request.args.get('date')
    conn, cursor = db()
    # Get all times
    cursor.execute("SELECT time FROM doctor_times WHERE status='available' ORDER BY time")
    all_times = [row['time'] for row in cursor.fetchall()]
    # Get booked times for this date
    booked = set()
    if date:
        cursor.execute("SELECT time FROM appointment WHERE date=%s", (date,))
        booked = set(row['time'] for row in cursor.fetchall())
    # For today, filter out times that have already passed
    import datetime
    now = datetime.datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    available_times = []
    for t in all_times:
        if t in booked:
            continue
        if date == today_str:
            # Only show times in the future
            t_hour, t_min = map(int, t[:5].split(':'))
            if (t_hour, t_min) <= (now.hour, now.minute):
                continue
        available_times.append(t)
    cursor.close()
    conn.close()
    return jsonify(available_times)


# API: Add a new appointment (only on open days)
@patient_bp.route('/patient/api/appointments', methods=['POST'])
def add_appointment():
    data = request.json
    date = data.get('date')
    time = data.get('time')
    doctor_name = data.get('doctor_name')
    patient_id = data.get('patient_id') or session.get('patient_id', 1)
    day_name = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%A')
    conn, cursor = db()
    cursor.execute("SELECT * FROM clinic_days WHERE day=%s AND status='open'", (day_name,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': f"Clinic is closed on {day_name}."}), 400
    # Check if time is available (not already booked for this doctor/date/time)
    cursor.execute("SELECT * FROM appointment WHERE doctor_name=%s AND date=%s AND time=%s", (doctor_name, date, time))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': "This time slot is already booked."}), 400
    # Insert appointment
    cursor.execute("INSERT INTO appointment (date, time, doctor_name, patient_id, status) VALUES (%s, %s, %s, %s, 'pending')", (date, time, doctor_name, patient_id))

    # Check if all times for this date are booked, then mark day as closed
    cursor.execute("SELECT time FROM doctor_times")
    all_times = set(row['time'] for row in cursor.fetchall())
    cursor.execute("SELECT time FROM appointment WHERE date=%s", (date,))
    booked_times = set(row['time'] for row in cursor.fetchall())
    if all_times == booked_times:
        # Mark this day as closed in clinic_days
        cursor.execute("UPDATE clinic_days SET status='closed' WHERE day=%s", (day_name,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True, 'message': "Appointment booked!"})

