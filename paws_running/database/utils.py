# database/utils.py
def get_user_by_username(username):
    from database.models import User
    return User.query.filter_by(username=username).first()

def add_transaction(user, amount):
    from database import db
    from database.models import Transaction
    transaction = Transaction(user_id=user.id, amount=amount)
    db.session.add(transaction)
    db.session.commit()
