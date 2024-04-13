from quart import Blueprint, jsonify, request

from utils import *
from endpoints.add_helper import *

blueprint = Blueprint('add', __name__)


@blueprint.route('/add', methods=['POST'])
async def add():
    """
    `Request payload:`
        `servers: dict of servers to add`
            `id: server id`
            `shards: list of shard names to copy`

    `Response payload:`
        `message: Servers added successfully`
        `status: Success`

    `Error payload:`
        `message: error message`
        `status: status of the request`
    """

    # Allow other tasks to run
    await asyncio.sleep(0)

    try:
        # Convert the reponse to json object
        response_json = await request.get_json()

        if response_json is None:
            raise Exception('Payload is empty')

        # Convert the json response to dictionary
        payload = dict(response_json)
        ic(payload)

        # Get the list of server replica hostnames to add
        servers: Dict[str, Dict[str, Any]] = dict(payload.get('servers', {}))

        # Spawn new containers
        semaphore = asyncio.Semaphore(DOCKER_TASK_BATCH_SIZE)

        async with Docker() as docker:
            tasks = [asyncio.create_task(
                spawn_container(
                    docker,
                    serv_config['id'],
                    server,
                    semaphore,
                )
            ) for server, serv_config in servers.items()]

            # Wait for all tasks to complete
            await asyncio.gather(*tasks, return_exceptions=True)
        # END async with Docker() as docker

        await asyncio.sleep(0)

        # Copy shards to the new containers
        semaphore = asyncio.Semaphore(REQUEST_BATCH_SIZE)

        tasks = [asyncio.create_task(
            copy_shards_to_container(
                 server,
                 serv_config['shards'],
                 semaphore,
                 )
        ) for server, serv_config in servers.items()]

        # Wait for all tasks to complete
        await asyncio.gather(*tasks, return_exceptions=True)

        return jsonify(ic({
            'message': 'Servers added successfully',
            'status': 'success'
        })), 200

    except Exception as e:
        return jsonify(ic(err_payload(e))), 400

# END add
