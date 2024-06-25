from fastapi import HTTPException, Request, status

auth_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')


def get_bearer_token(request: Request) -> str:
    if not (token_str := request.headers.get('Authorization')):
        raise auth_error
    try:
        prefix, token = token_str.split(' ')
    except ValueError:
        raise auth_error

    if not prefix == 'Bearer':
        raise auth_error

    return token
