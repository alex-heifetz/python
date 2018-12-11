import os
from sql import Db

db_dir = os.path.dirname(os.path.abspath(__file__)) + "/choosecanteen.db"


def change(message, place_id):
    if message:
        db = Db(db_dir)
        place = db.get_place(place_id)
        today = db.get_today_crusade()
        if today:
            db.update_crusade(place[0])
        else:
            db.add_crusade(place[0])
        return str(place[1])


def delete(message, place_id):
    if message:
        db = Db(db_dir)
        place = db.get_place(place_id)
        db.set_delete(place_id, int(not bool(place[3])))
        return str(place[1])
