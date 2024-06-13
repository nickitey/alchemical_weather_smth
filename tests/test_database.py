import sys

import pytest
sys.path.append('../weatherapp')
sys.path.append('../')

import weatherapp.orm_runner as orm

test_counter = 0


@pytest.fixture()
def get_user_id():
    return 123456789


@pytest.fixture()
def get_user_city():
    return 'Moscow'


def test_add_tg_user(get_user_id):
    orm.add_user(get_user_id)
    session = orm.Session()
    test_user_query = session.query(orm.User).filter_by(tg_id=get_user_id).first()
    assert test_user_query.tg_id == get_user_id
    global test_counter
    test_counter += 1
    print(f'Test # {test_counter} passed. New user is added.')


def test_add_user_city(get_user_id, get_user_city):
    orm.add_city(get_user_id, get_user_city)
    session = orm.Session()
    test_user_query = session.query(orm.User).filter(orm.User.tg_id == get_user_id).first()
    assert test_user_query.city == get_user_city
    global test_counter
    test_counter += 1
    print(f'Test # {test_counter} passed. User\'s city is updated.')
