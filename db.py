import sqlite3 as sql
import datetime


db = sql.connect('DataBaseSecond.db')
with db:
    cur = db.cursor()
    cur.execute("""CREATE TABLE if not exists question (
        question TEXT, 
        ansver TEXT
    )""")
    db.commit()

class database:

    def __init__(self) -> None:
        pass

    def insert_new_question(self, question, ansv):
        cur.execute(""" INSERT INTO question (question, ansver) VALUES (?,?) """, (question, ansv))
        db.commit()

        return {"status" : True, "data" : {"question" : question, "ansv" : ansv}}
    
    def select_ansv_from_question(self, question):
        cur.execute(""" SELECT ansver FROM question WHERE question = ? """, (question,))
        result = cur.fetchall()

        if len(result) >= 1: return {"status" : True, "ansv" : result[0][0]}
        else: return {"status" : False}

    def select_all_question(self):
        cur.execute(""" SELECT question FROM question""")
        result = cur.fetchall()

        if len(result) >= 1: return {"status" : True, "question" : result}
        else: return {"status" : False}

    def edit_question_hedder(self, question, new_question):
        cur.execute(" UPDATE question SET question = ? WHERE question = ?", (new_question, question))
        db.commit()
        return {"status" : True}
    
    def edit_question_ansv(self, question, new_tex):
        cur.execute(" UPDATE question SET ansver = ? WHERE question = ?", (new_tex, question))
        db.commit()
        return {"status" : True}

    def delate_question(self, question):
        cur.execute(""" DELETE FROM question WHERE question = ? """, (question,))
        db.commit()
        return {"status" : True}