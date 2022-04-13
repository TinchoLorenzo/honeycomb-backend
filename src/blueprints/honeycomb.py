from flask import Blueprint, jsonify, request, current_app

from .honeycomb_orm import get_bee,get_honeycomb_full_data, get_honeycomb, get_bee_position_on_honeycomb_data, get_all_moves_data, get_next_move_data
import logging
honeycomb_blueprint = Blueprint(name="honeycomb", import_name=__name__)
honeycombs = {}

@honeycomb_blueprint.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@honeycomb_blueprint.route('/', methods=['POST'])
def create_honeycomb():
    try:
        data = request.get_json()
        honeycomb = get_honeycomb(data)
        honeycombs[honeycomb.get_id()] = honeycomb
        response = {
            'honeycomb_id': honeycomb.get_id(),
            'bees_ids': [bee for bee in honeycomb.get_bees().keys()]
        }
        return jsonify(response)
    except Exception as e:
        logging.warning(e)
        return e, 404


@honeycomb_blueprint.route('/<string:honeycomb_id>/bee/', methods=['POST'])
def add_bee_to_honeycomb(honeycomb_id):
    try:
        data = request.get_json()
        bee = get_bee(data)
        honeycombs[honeycomb_id].add_bee(bee)
        response = {
            'bee_id': bee.get_id()
        }
        return jsonify(response)
    except Exception as e:
        logging.warning(e)
        return e, 404


@honeycomb_blueprint.route('/<string:honeycomb_id>/bee/<string:bee_id>', methods=['DELETE'])
def delete_bee_to_honeycomb(honeycomb_id, bee_id):
    try:
        honeycombs[honeycomb_id].delete_bee(bee_id)
        response = {
            'bee_id': bee_id
        }
        return jsonify(response)
    except Exception as e:
        logging.warning(e)
        return e, 404


@honeycomb_blueprint.route('/<string:honeycomb_id>', methods=['PATCH'])
def reset_honeycomb(honeycomb_id):
    try:
        honeycombs[honeycomb_id].reset()
        return jsonify(get_honeycomb_full_data(honeycombs[honeycomb_id]))
    except Exception as e:
        logging.warning(e)
        return e, 404


@honeycomb_blueprint.route('/<string:honeycomb_id>/bee/<string:bee_id>', methods=['GET'])
def get_bee_position(honeycomb_id, bee_id):
    try:
        # The bee couldn't be there
        honeycomb = honeycombs[honeycomb_id]
        bee = honeycomb.get_bees()[bee_id]
        return jsonify(get_bee_position_on_honeycomb_data(honeycomb, bee))
    except Exception as e:
        logging.error(e)
        return e, 404


@honeycomb_blueprint.route('/<string:honeycomb_id>/moves/all/', methods=['GET'])
def get_all_moves(honeycomb_id):
    try:
        response = get_all_moves_data(honeycombs[honeycomb_id].simulate_all())
        return jsonify(response)
    except Exception as e:
        logging.error(e)
        return e, 404


@honeycomb_blueprint.route('/<string:honeycomb_id>/moves/next/', methods=['GET'])
def get_next_move(honeycomb_id):
    try:
        response = get_next_move_data(next(honeycombs[honeycomb_id].simulate_next()))
        return jsonify(response)
    except Exception as e:
        logging.error(e)
        return e, 404
