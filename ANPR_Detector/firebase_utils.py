# firebase_utils.py
# firebase operations: user registration check, entry/exit

from datetime import datetime
from firebase_admin import db

def is_registered_user(plate_number):
    """
    check if the given plate number is listed under any registered user in firebase

    """
    try:
        users_ref = db.reference('users')
        users_snapshot = users_ref.get()
        if not users_snapshot:
            
            return False

        for user_data in users_snapshot.values():
            license_plates = user_data.get('license_plates', [])
            if plate_number in license_plates:
                return True
        return False
    except Exception as e:
        print(f"Firebase check error: {str(e)}")
        
        return False

def register_entry(plate_number, confidence, image_name):
    """
    if no active unpaid session exists, register a new entry in firebase.

    """
    normalized_plate = plate_number.replace(" ", "").upper()

    if not is_registered_user(normalized_plate):
        print(f"Unregistered plate detected: {plate_number}")
        unreg_ref = db.reference(f"unregistered-entries/{normalized_plate}")
        unreg_ref.push({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "confidence": float(confidence)
        })
        return False

    sessions_ref = db.reference(f"parking-records/{normalized_plate}")
    sessions = sessions_ref.get()

    if sessions:
        for session in sessions.values():
            if session.get('paid') is False:
                print(f"Active session exists for plate {plate_number}")

                return False

    now = datetime.now()
    new_ref = sessions_ref.push()
    new_ref.set({
        "entryTime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "paid": False,
        "entryMethod": "camera",
        "confidence": float(confidence),
        "image": image_name
    })

    print(f"Registered entry for {plate_number}")

    return True

def register_exit(plate_number, confidence, image_name):
    """
    find active session and mark exit time, duration, and payment.

    """
    try:
        normalized_plate = plate_number.replace(" ", "").upper()
        records_ref = db.reference(f"parking-records/{normalized_plate}")
        records = records_ref.get()

        if not records:
            print(f"No sessions found for {plate_number}")

            return False

        for session_id, session in records.items():
            if session.get('paid') is False and session.get('exitTime') is None:
                now = datetime.now()
                entry_time = datetime.strptime(session.get('entryTime'), "%Y-%m-%d %H:%M:%S")
                duration_min = (now - entry_time).total_seconds() / 60.0

                # pricing logic
                if duration_min <= 10:
                    fee = 0.0
                else:
                    hours = int(duration_min / 60) + (1 if duration_min % 60 > 0 else 0)
                    fee = min(hours * 2.0, 10.0)

                session_ref = records_ref.child(session_id)
                session_ref.update({
                    "exitTime": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "durationMinutes": round(duration_min, 1),
                    "amountDue": round(fee, 2),
                    "exitConfidence": float(confidence),
                    "exitImage": image_name,
                    "paid": True
                })

                print(f"{plate_number} exited, charged £{fee:.2f}")
                return True

        print(f"No active unpaid session for {plate_number}")

        return False

    except Exception as e:
        print(f"Firebase exit error: {str(e)}")

        return False
