import json
import os
from jsonschema import RefResolver, Draft7Validator, validate
from setup import ROOT_DIR
from src.model.src.honeycomb.honeycomb import Bee, HoneyComb
from flask import current_app

"""
Open the honeycomb and the bee schema, and map them
"""
resources_path = os.path.join(ROOT_DIR, 'resources', 'blueprints', 'json_schemas')
with open(os.path.join(resources_path, 'honeycomb_schema.json'), 'r') as file:
    honeycomb_schema = json.load(file)

with open(os.path.join(resources_path, 'bee_schema.json'), 'r') as file:
    bee_schema = json.load(file)

schema_store = {
    bee_schema['$id']: bee_schema,
    honeycomb_schema['$id']: honeycomb_schema,
}

bee_validator = Draft7Validator(bee_schema)
resolver = RefResolver.from_schema(bee_schema, store=schema_store)
honeycomb_validator = Draft7Validator(honeycomb_schema, resolver=resolver)


def get_bee(json_data):
    """
    Get a bee from the json data
    :param json_data:
    :return:
    """
    bee_validator.validate(json_data)
    return Bee(json_data['x'], json_data['y'], json_data['orientation'], json_data['moves'])


def get_honeycomb(json_data):
    """
    Get the honeycomb given a JSON
    :param json_data:
    :return:
    """
    honeycomb_validator.validate(json_data)
    honeycomb = HoneyComb([], json_data['size'])
    if 'bees' in json_data:
        for bee_data in json_data['bees']:
            bee = get_bee(bee_data)
            honeycomb.add_bee(bee)
    return honeycomb


def get_bee_full_data(bee: Bee):
    """
    Get the full data of a bee, in a JSON format
    :param bee:
    :return:
    """
    return {
        **get_bee_position_data(bee),
        **{
            'moves': bee.get_moves()
        }
    }


def get_bee_position_data(bee: Bee):
    """
    Get the bee id, location and orientation of the bee
    :param bee:
    :return:
    """
    [x, y], orientation = bee.get_position()
    return {
        'bee_id': bee.get_id(),
        'x': x,
        'y': y,
        'orientation': orientation
    }


def get_bee_position_on_honeycomb_data(honeycomb: HoneyComb, bee: Bee):
    """
    Get the position of a bee in the honeycomb as a JSON
    :param honeycomb:
    :param bee:
    :return:
    """
    current_app.logger.info(bee)
    return get_bee_position_data(bee) if honeycomb.get_bee_position(bee.get_id()) is not None else \
        {
            'bee_id': bee.get_id(),
            'x': -1,
            'y': -1,
            'orientation': ''
        }


def get_honeycomb_full_data(honeycomb: HoneyComb):
    """
    Get all the honeycomb_id, the size and the information of the position of the bees as a JSON
    :param honeycomb:
    :return:
    """
    return {
        'honeycomb_id': honeycomb.get_id(),
        'size': honeycomb.get_size(),
        'bees': [get_bee_position_on_honeycomb_data(honeycomb, bee) for bee in honeycomb.get_bees().values()]
    }


def get_all_moves_data(bees_moves):
    """
    Transform a list of moves into a JSON format
    :param bees_moves:
    :return:
    """
    all_moves = []
    for move in bees_moves:
        all_moves.append(get_next_move_data(move))
    return all_moves


def get_next_move_data(bees_move):
    """
    Transform the bee's move to a JSON format. If the bee is out of range, it will return [-1, -1] as it's position
    :param bees_move:
    :return:
    """
    one_move = []
    for bee_id, bee_move in bees_move.items():
        one_move.append(
            {
                'bee_id': bee_id,
                'x': -1,
                'y': -1,
                'orientation': ''
            } if bee_move is None else {
                'bee_id': bee_id,
                'x': bee_move[0][0],
                'y': bee_move[0][1],
                'orientation': bee_move[1]
            })
    return one_move
