import _sqlite3 as sql
from datetime import datetime
from haray.models import User, Product, Payment
from haray import db
from haray import *
##### UNRELATED!!

# page = request.args.get('page', 1, type=int)
conn = sql.connect('haraydbFinal.db')
c = conn.cursor()

datenow = datetime.utcnow()

examplesql = c.execute('''SELECT * FROM Product as p, Payment as pa, User as u
                    WHERE
                    pa.prod_id = p.prod_id AND 
                    u.user_id = p.user_id AND 
                    pa.user_id = 1''')
                    # WHERE pa.user_id = 1''')

for x in examplesql:
    print(x)



products = db.session.query(
    Payment, Product,
).filter(
    Product.prod_id == Payment.prod_id,
).filter(
    Payment.user_id == 1,
).order_by(Payment.transaction_date.desc()).all()



# print(examplesql)

for tes in examplesql:
    print(tes[1])


# print(products[0])
# print(products)






# c.execute('ALTER TABLE Payment ADD COLUMN transaction_date DATETIME NOT NULL DEFAULT(?)', (datetime.utcnow(),))
# conn.commit()

# c.execute('SELECT * FROM User')
# print(c.fetchall())
