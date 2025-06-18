from flask import Blueprint, render_template, request, jsonify
from app.models import db

doctor_bp = Blueprint('doctor', __name__, template_folder='templates', static_folder='static')

@doctor_bp.route('/doctor', methods=['GET'])
def doctor():
    return render_template('doctor/doctor.html')


# for time route
@doctor_bp.route('/doctor/time', methods=['GET'])
def doctor_time():
    return render_template('doctor/time.html')


# API: Get all doctor times
@doctor_bp.route('/doctor/api/times', methods=['GET'])
def get_doctor_times():
    conn, cursor = db()
    cursor.execute("SELECT * FROM doctor_times ORDER BY id DESC")
    times = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(times)


# API: Add a new doctor time
@doctor_bp.route('/doctor/api/times', methods=['POST'])
def add_doctor_time():
    data = request.json
    time = data.get('time')
    status = data.get('status', 'available')
    conn, cursor = db()
    cursor.execute("INSERT INTO doctor_times (time, status) VALUES (%s, %s)", (time, status))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})


# API: Update a doctor time
@doctor_bp.route('/doctor/api/times/<int:time_id>', methods=['PUT'])
def update_doctor_time(time_id):
    data = request.json
    time = data.get('time')
    status = data.get('status')
    conn, cursor = db()
    cursor.execute("UPDATE doctor_times SET time=%s, status=%s WHERE id=%s", (time, status, time_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})


# API: Delete a doctor time
@doctor_bp.route('/doctor/api/times/<int:time_id>', methods=['DELETE'])
def delete_doctor_time(time_id):
    conn, cursor = db()
    cursor.execute("DELETE FROM doctor_times WHERE id=%s", (time_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})




# for clinic days route
@doctor_bp.route('/doctor/clinic-days', methods=['GET'])
def clinic_days():
    return render_template('doctor/clinic_days.html')


# API: Get all clinic days
@doctor_bp.route('/doctor/api/clinic-days', methods=['GET'])
def get_clinic_days():
    conn, cursor = db()
    cursor.execute("SELECT * FROM clinic_days ORDER BY id DESC")
    days = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(days)


# API: Add a new clinic day (update status if day exists, else insert new)
@doctor_bp.route('/doctor/api/clinic-days', methods=['POST'])
def add_clinic_day():
    data = request.json
    day = data.get('day')
    status = data.get('status', 'closed')
    conn, cursor = db()
    cursor.execute("SELECT * FROM clinic_days WHERE day=%s", (day,))
    exists = cursor.fetchone()
    if exists:
        # If status is the same, return duplicate message
        if exists['status'] == status:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': f"{day} already set as {status}."}), 400
        # If status is different, update status
        cursor.execute("UPDATE clinic_days SET status=%s WHERE id=%s", (status, exists['id']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': f"{day} status updated to {status}."})
    # If not exists, insert new
    cursor.execute("INSERT INTO clinic_days (day, status) VALUES (%s, %s)", (day, status))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True, 'message': f"{day} added as {status}."})


# API: Update a clinic day
@doctor_bp.route('/doctor/api/clinic-days/<int:day_id>', methods=['PUT'])
def update_clinic_day(day_id):
    data = request.json
    day = data.get('day')
    status = data.get('status')
    conn, cursor = db()
    cursor.execute("SELECT * FROM clinic_days WHERE day=%s AND status=%s AND id!=%s", (day, status, day_id))
    exists = cursor.fetchone()
    if exists:
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': f"{day} already set as {status}."}), 400
    cursor.execute("UPDATE clinic_days SET day=%s, status=%s WHERE id=%s", (day, status, day_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})


# API: Delete a clinic day
@doctor_bp.route('/doctor/api/clinic-days/<int:day_id>', methods=['DELETE'])
def delete_clinic_day(day_id):
    conn, cursor = db()
    cursor.execute("DELETE FROM clinic_days WHERE id=%s", (day_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})




# Show appointments page for doctor
@doctor_bp.route('/doctor/appointments', methods=['GET'])
def doctor_appointments():
    return render_template('doctor/appointments.html')

# API: Get all appointments (doctor view)
@doctor_bp.route('/doctor/api/appointments', methods=['GET'])
def get_all_appointments():
    conn, cursor = db()
    cursor.execute("SELECT * FROM appointment ORDER BY date DESC, time DESC")
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(appointments)

# API: Delete an appointment
@doctor_bp.route('/doctor/api/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    conn, cursor = db()
    cursor.execute("DELETE FROM appointment WHERE id=%s", (appointment_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})


# API: Get available times for a specific date (doctor view, same as patient)
@doctor_bp.route('/doctor/api/available-times', methods=['GET'])
def doctor_available_times():
    date = request.args.get('date')
    exclude_id = request.args.get('exclude_id')  # Optional appointment ID to exclude from booked times
    conn, cursor = db()
    cursor.execute("SELECT time FROM doctor_times WHERE status='available' ORDER BY time")
    all_times = [row['time'] for row in cursor.fetchall()]
    booked = set()
    if date:
        if exclude_id:
            cursor.execute("SELECT time FROM appointment WHERE date=%s AND id!=%s", (date, exclude_id))
        else:
            cursor.execute("SELECT time FROM appointment WHERE date=%s", (date,))
        booked = set(row['time'] for row in cursor.fetchall())
    import datetime
    now = datetime.datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    available_times = []
    for t in all_times:
        if t in booked:
            continue
        if date == today_str:
            t_hour, t_min = map(int, t[:5].split(':'))
            if (t_hour, t_min) <= (now.hour, now.minute):
                continue
        available_times.append(t)
    cursor.close()
    conn.close()
    return jsonify(available_times)

# API: Edit/update an appointment (date, time, status) with restrictions (no double-booking, no past)
@doctor_bp.route('/doctor/api/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    data = request.json
    date = data.get('date')
    time = data.get('time')
    status = data.get('status')
    conn, cursor = db()
    
    # Get current appointment
    cursor.execute("SELECT * FROM appointment WHERE id=%s", (appointment_id,))
    current = cursor.fetchone()
    if not current:
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': 'Appointment not found.'}), 404
    
    # Check if the day is open
    day_name = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%A')
    cursor.execute("SELECT * FROM clinic_days WHERE day=%s AND status='open'", (day_name,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': f'Clinic is closed on {day_name}.'}), 400
    
    # Restriction: no double-booking (except for this appointment)
    cursor.execute("SELECT * FROM appointment WHERE date=%s AND time=%s AND id!=%s", (date, time, appointment_id))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': 'This time slot is already booked.'}), 400
    
    # Restriction: no past times
    import datetime
    now = datetime.datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    if date < today_str or (date == today_str and time.startswith(now.strftime('%H:%M'))):
        t_hour, t_min = map(int, time[:5].split(':'))
        if date < today_str or (date == today_str and (t_hour, t_min) <= (now.hour, now.minute)):
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'Cannot schedule in the past.'}), 400
    
    # Make sure time slot is valid (available in doctor_times)
    cursor.execute("SELECT * FROM doctor_times WHERE time=%s AND status='available'", (time,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': 'This time slot is not available.'}), 400
    
    # Update the appointment
    cursor.execute("UPDATE appointment SET date=%s, time=%s, status=%s WHERE id=%s", 
                  (date, time, status, appointment_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Appointment updated successfully!'})

# API: Quick status update for an appointment
@doctor_bp.route('/doctor/api/appointments/<int:appointment_id>/status', methods=['PUT'])
def update_appointment_status(appointment_id):
    data = request.json
    status = data.get('status')
    
    conn, cursor = db()
    cursor.execute("UPDATE appointment SET status=%s WHERE id=%s", (status, appointment_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Status updated successfully!'})


# API: Get open clinic days (for calendar)
@doctor_bp.route('/doctor/api/open-days', methods=['GET'])
def doctor_get_open_days():
    conn, cursor = db()
    cursor.execute("SELECT day FROM clinic_days WHERE status='open'")
    days = [row['day'] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(days)
