# from haray import manager
from haray import create_app

app = create_app()

if __name__ == '__main__':
    # manager.run()
    app.run(debug=True)





# sql lite
#
# nums = [1,2,3,4,5,6,7,8,9]
# numGen = random.choice(nums)
# dateNow = str(datetime.now())
#
# newUser = User('Kamis', 'Kamees', '29/07/1996')
#
# conn = sql.connect(':memory:', check_same_thread=False)
# c = conn.cursor()
#
# c.execute('''CREATE TABLE User (
#           uID INTEGER PRIMARY KEY NOT NULL,
#           username TEXT NOT NULL,
#           password TEXT NOT NULL,
#           lastname TEXT NOT NULL,
#           firstname TEXT NOT NULL,
#           dob NUMBERIC NOT NULL,
#           joindate NUMERIC NOT NULL
#         )''')
#
#
# c.execute('INSERT INTO User VALUES (NULL, :user, :pass, :firstN, :lastN, :dob, :joindate)',
#         {
#         'user': newUser.firstName + str(numGen),
#         'pass': '123',
#         'firstN': newUser.firstName,
#         'lastN': newUser.lastName,
#         'dob': newUser.dob,
#         'joindate': dateNow[0:10]
#         })
#
#
#
# c.execute('SELECT * FROM User WHERE uID = 1') #, (newUser.firstName, ))
# getUser = c.fetchall()
# # print('--')
# # print(c.fetchall())
# # print('--')

