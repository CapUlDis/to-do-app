import logging, string, random
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import exists
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import current_app
from models import User


logger = logging.getLogger(__file__)


def check_user_with_password_exists(name, password):
    session = current_app.Session()
    query = session.query(User).filter(User.name == name)
    try:
        query.one()
    except OperationalError as err:
        session.close()
        logger.error(f'OperationalError: database does not exist or connection does not work. Make sure that postgresql server run and run dbsetup.sh: {err}.')
        raise ConnectionError(f'Database are not connected to app or does not exist: {err}.')
    except ProgrammingError as err:
        session.close()
        logger.error(f'ProgrammingError: table users does not exist in database. Create table with dbsetup.sh: {err}.')
        raise NameError(f'Table users does not exist in database: {err}.')
    except NoResultFound as err:
        session.close()
        logger.info(f'NoResultFound: no such username in database: {err}.')
        return False
    except MultipleResultsFound as err:
        session.close()
        logger.error(f'MultipleResultsFound: database has more than one users with such name: {err}.')
        raise LookupError(f'MultipleResultsFound: database has more than one users with such name: {err}.')
    else:
        session.close()
        return check_password_hash(query.one().passwordhash, password)

def generate_password():
    password = ''
    for n in range(16):
        x = random.randint(0,61)
        password += string.printable[x]
    return password

def check_useremail_exist(useremail):
    session = current_app.Session()
    try:
        check_result = session.query(exists().where(User.useremail == useremail)).scalar()
    except OperationalError as err:
        session.close()
        logger.error(f'OperationalError: database does not exist or connection does not work. Make sure that postgresql server run and run dbsetup.sh: {err}.')
        raise ConnectionError(f'Database are not connected to app or does not exist: {err}.')
    except ProgrammingError as err:
        session.close()
        logger.error(f'ProgrammingError: table users does not exist in database. Create table with dbsetup.sh: {err}.')
        raise NameError(f'Table users does not exist in database: {err}.')
    else:
        session.close()
        return check_result

def add_new_user_to_db(name, password, useremail):
    session = current_app.Session()
    passwordhash = generate_password_hash(password)
    session.add(User(name=name, passwordhash=passwordhash, useremail=useremail))
    try:
        session.commit()
        session.close()
    except OperationalError as err:
        session.close()
        logger.error(f'OperationalError: database does not exist or connection does not work. Make sure that postgresql server run and run dbsetup.sh: {err}.')
        raise ConnectionError(f'Database are not connected to app or does not exist: {err}.')
    except ProgrammingError as err:
        session.close()
        logger.error(f'ProgrammingError: table users does not exist in database. Create table with dbsetup.sh: {err}.')
        raise NameError(f'Table users does not exist in database: {err}.')

    