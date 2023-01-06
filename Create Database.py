import sqlite3

conn = sqlite3.connect('GravioScores_database')
cursor = conn.cursor()

# # cursor.execute('''CREATE TABLE IF NOT EXISTS scores ([score] INTEGER, [person] TEXT)''')
# cursor.execute('''INSERT INTO scores VALUES (?,?)''', (50, 'Yifan'))
# cursor.execute('''INSERT INTO scores VALUES (?,?)''', (80, 'Dennis'))
#
# conn.commit()

cursor.execute('''SELECT score, person FROM scores ORDER BY score''')
for score in cursor:
    print(score)


