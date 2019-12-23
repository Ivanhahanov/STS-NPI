from app.models import *
from app import db, app
from flask import redirect, url_for, abort, render_template, flash, request




# head = Head(firstname='i',
#             secondname='w',
#             lastname='v')
# db.session.add(head)
# info = Legalinfo(inn=12345)
# db.session.add(info)
# l = License(license_number=128931)
# db.session.add(l)
# db.session.commit()
#
#
# l = License.query.get(1)
# print(l)
# head = Head.query.get(1)
# info = Legalinfo.query.get(1)
# legal = LegalEntity(license=l, head=head, data=info)
# db.session.add(legal)
# db.session.commit()
# legal = LegalEntity.query.get(1)
# print(legal.license.license_number)
# print(legal.head.firstname)
# print(legal.data.inn)
# l = LegalEntity.query.get(2)
# print(l.license)
# lic = License.query.get(l.license)
# print(lic.license_number)
# cont = Contract(contract_number=1,
#                 organization='explabs')
# db.session.add(cont)
# db.session.commit()
# cont = Contract.query.get(1)
# print(cont)
# add = Addition(addition_number=1,
#                file='first',
#                document=cont)
# appe = Appendix(appendix_number=2,
#                 file='second',
#                 document=cont)
# db.session.add_all([add, appe])
# db.session.commit()
if __name__ == '__main__':
    app.run()
