import sys

sys.path.append('../weatherapp')
sys.path.append('../')

import weatherapp.orm_runner as orm


def test_add_tg_user():
    tg_user_id = 123456789
    orm.add_user(tg_user_id)
    session = orm.Session()
    test_user_query = session.query(orm.User).filter_by(tg_id=tg_user_id).first()
    assert test_user_query.tg_id == tg_user_id
    print('Test passed')