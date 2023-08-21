from gocept.webtoken import create_authorization_header
from gocept.webtoken import create_web_token
from gocept.webtoken import decode_web_token
from gocept.webtoken import extract_token
import pytest


def test_endtoend_1():
    """Testing create and decode of token via request header."""
    token_dict = create_web_token(
        'jwt-access-private', 'issuer', 'app', 300, data={'foo': 'bar'})
    key, value = create_authorization_header(token_dict)
    encoded_token = extract_token(value)
    decoded_token = decode_web_token(encoded_token, 'jwt-access-public', 'app')
    assert {'foo': 'bar'} == decoded_token['data']


def test_endtoend_2():
    """`decode_web_token()` raises a ValueError if the token is expired."""
    token_dict = create_web_token(
        'jwt-access-private', 'issuer', 'app', -1, data={'foo': 'bar'})
    header = create_authorization_header(token_dict)
    encoded_token = extract_token(dict([header]))
    with pytest.raises(ValueError) as err:
        decode_web_token(encoded_token, 'jwt-access-public', 'app')
    assert 'Signature has expired' == str(err.value)
