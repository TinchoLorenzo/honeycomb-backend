import json
import os
from jsonschema import RefResolver, Draft7Validator, validate
from setup import ROOT_DIR
from src.model.src.honeycomb.honeycomb import Bee, HoneyComb
from flask import current_app

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
    bee_validator.validate(json_data)
    return Bee(json_data['x'], json_data['y'], json_data['orientation'], json_data['moves'])


def get_honeycomb(json_data):
    honeycomb_validator.validate(json_data)
    honeycomb = HoneyComb([], json_data['size'])
    if 'bees' in json_data:
        for bee_data in json_data['bees']:
            bee = get_bee(bee_data)
            honeycomb.add_bee(bee)
    return honeycomb


def get_bee_full_data(bee: Bee):
    return {
        **get_bee_position_data(bee),
        **{
            'moves': bee.get_moves()
        }
    }


def get_bee_position_data(bee: Bee):
    [x, y], orientation = bee.get_position()
    return {
        'bee_id': bee.get_id(),
        'x': x,
        'y': y,
        'orientation': orientation
    }


def get_bee_position_on_honeycomb_data(honeycomb: HoneyComb, bee: Bee):
    current_app.logger.info(bee)
    return get_bee_position_data(bee) if honeycomb.get_bee_position(bee.get_id()) is not None else \
        {
            'bee_id': bee.get_id(),
            'x': -1,
            'y': -1,
            'orientation': ''
        }


def get_honeycomb_full_data(honeycomb: HoneyComb):
    return {
        'honeycomb_id': honeycomb.get_id(),
        'size': honeycomb.get_size(),
        'bees': [get_bee_position_on_honeycomb_data(honeycomb, bee) for bee in honeycomb.get_bees().values()]
    }


def get_all_moves_data(bees_moves):
    all_moves = []
    for move in bees_moves:
        all_moves.append(get_next_move_data(move))
    return all_moves


def get_next_move_data(bees_move):
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
