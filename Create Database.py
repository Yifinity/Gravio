import sqlite3

conn = sqlite3.connect('GravioScores_database')
cursor = conn.cursor()
cursor.execute("""DROP TABLE highScores""")
cursor.execute('''CREATE TABLE highScores([score] INTEGER)''')
cursor.execute('''INSERT INTO highScores (score) VALUES (80)''')
#
conn.commit()
# cursor.execute("""DELETE FROM testScores WHERE score = 51 LIMIT 1""")
# conn.commit()

cursor.execute('''SELECT * FROM highScores ORDER BY score''')
for score in cursor:
    print(score)


# cursor.execute("""DROP TABLE highScores""")

# cursor.execute("""DROP TABLE highScores""")

#
# # # cursor.execute('''CREATE TABLE IF NOT EXISTS scores ([score] INTEGER, [person] TEXT)''')
# cursor.execute('''INSERT INTO highScores (rank, score) VALUES (5, 50)''')
# cursor.execute('''INSERT INTO highScores (rank, score) VALUES (4, 51)''')
# cursor.execute('''INSERT INTO highScores (rank, score) VALUES (3, 52)''')
# cursor.execute('''INSERT INTO highScores (rank, score) VALUES (2, 77)''')
# cursor.execute('''INSERT INTO highScores (rank, score) VALUES (1, 80)''')
# #
# conn.commit()
#
# # cursor.execute('''SELECT score FROM highScores ORDER BY score''')
# for score in cursor:
#     print(score)


