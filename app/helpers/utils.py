import secrets
import bcrypt
import flask


def generate_password_hash(password, rounds=14, prefix=b'2b'):
    """
    Generate password hash with bcrypt having default prefix being 2b if not parsed. Also default
    log rounds is 14.
    :param password:
    :param rounds:
    :param prefix:
    :return:
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=rounds, prefix=prefix)).decode('utf-8')


def check_password_hash(hashed, password):
    """
    To check for password against hash
    :param password:
    :param hashed:
    :return:
    """
    if bcrypt.checkpw(password.encode(), hashed.encode()):
        return True
    return False


def generate_token_urlsafe(nbytes=None):
    """
    Generate a random URL-safe text string
    :param nbytes:
    :return:
    """
    return secrets.token_urlsafe(nbytes)


def response_dict(obj, results, path, id=None):
    domain = flask.request.url_root
    if obj.has_next:
        data = {
            "count": obj.total,
            "results": results,
            "next": "{0}{1}?id={2}&page={3}".format(domain, path, id, obj.next_num)
            if id else "{0}{1}?page={2}".format(domain, path, obj.next_num),
            "previous": ""
        }
    elif obj.has_prev:
        data = {
            "count": obj.total,
            "results": results,
            "next": "",
            "previous": "{0}{1}?id={2}&page={3}".format(domain, path, id, obj.prev_num)
            if id else "{0}{1}?page={2}".format(domain, path, obj.prev_num),
        }
    else:
        data = {
            "count": obj.total,
            "results": results,
            "next": "",
            "previous": ""
        }

    return data
