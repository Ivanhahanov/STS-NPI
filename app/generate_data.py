from app.models import *
import random
import time
def gen_rand_int(num):
    return ''.join([str(random.randint(0, 9)) for _ in range(num)])

def gen_rand_file():
    return time.strftime(str(random.randint(0, 1000))+"%d%H%M%S%Y.pdf")

def docs():

    main_doc = TechnicalDocument(passport_code=gen_rand_int(10),
                                 manual=gen_rand_file(),
                                 specific=gen_rand_file()
                                 )
    doc = SupplementaryDocument(document_name=str(gen_rand_int(1)),
                                document=gen_rand_file(),
                                tech=main_doc)
    db.session.add(main_doc)
    db.session.commit()


docs()
