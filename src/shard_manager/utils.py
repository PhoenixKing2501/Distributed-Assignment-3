from common import *
import common


def err_payload(err: Exception):
    """
    Generate an error payload.
    """

    if DEBUG:
        print(f'{Fore.RED}ERROR | '
              f'{err.__class__.__name__}: {err}\n'
              f'{Style.RESET_ALL}',
              file=sys.stderr)

    return {
        'message': f'<Error> {err.__class__.__name__}: {err}',
        'status': 'failure'
    }
# END err_payload


def get_container_config(
    serv_id: int,
    hostname: str
):
    """
    Get the container config for the server replica.
    """

    return {
        'image': 'server:v3',
        'detach': True,
        'env': [
            f'SERVER_ID={serv_id:06}',
            f'DEBUG={str(DEBUG).lower()}',
            'POSTGRES_HOST=localhost',
            'POSTGRES_PORT=5432',
            'POSTGRES_USER=postgres',
            'POSTGRES_PASSWORD=postgres',
            'POSTGRES_DB_NAME=postgres',
        ],
        'hostname': hostname,
        'tty': True,
    }


def get_request_id():
    """
    Get a new request id.
    """

    return random.randint(100000, 999999)
# END get_request_id


async def get_primary_server(shard: str):
    """
    Get the primary server for the shard.
    """

    # TODO: Implement this function

    return "primary_server"
