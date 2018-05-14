from trello.queries import *
from trello.errors import *
from trello.variables import *
import requests

########################################################################################################################
# All functions used by the scripts
########################################################################################################################


def get_organization_boards():
    """"Gets a JSON list of all the boards in the organization."""
    return requests.get(url=get_boards_organization).json()


def get_member_list():
    """"Gets a JSON list of al the members in the organization"""
    return requests.get(url=get_members).json()


def get_id(resource, name):
    """"Gets id of a Board, List or Card from a resource, given the name. Returns None if no match is found."""
    all_ids = [d['id'] for d in resource if d['name'] == name]
    if len(all_ids) > 0:
        return all_ids[-1]
    return None


def move_cards_in_same_board(name_board, name_source, name_target):
    """"Script to move the Cards from the List 'name_source' to the List 'name_target' in the Board 'name_board'"""

    print(move_list_to_list_in_board.format(name_source=name_source, name_target=name_target, name_board=name_board))
    organization_boards = get_organization_boards()

    # WORKFLOW
    # 01. Get id of Board
    # 02. Get all Lists in Board
    # 03. Get id's of source and target Lists
    # 04. Move all cards from source List to target List

    # 01. Get id of Board
    id_board = get_id(organization_boards, name_board)
    if id_board is not None:
        # 02. Get all Lists in Board
        lists = requests.get(url=get_lists.format(id=id_board)).json()
        # 03. Get id's of source and target Lists
        id_source = get_id(lists, name_source)
        id_target = get_id(lists, name_target)
        if id_source is not None and id_target is not None:
            # 04. Move all cards from source List to target List if there are cards to move
            if len(requests.get(url=get_cards.format(id=id_source)).json()) > 0:
                requests.post(url=move_all_cards.format(id=id_source, board=id_board, list=id_target))
                print(successful_move)
            else:
                print(list_in_board_empty.format(list_name=name_source, board=name_board))
        else:
            if id_source is None:
                err_no_list(name_source)
            if id_target is None:
                err_no_list(name_target)
    else:
        err_no_board(name_board)


def move_card_to_specific_list(card_id, name_target, name_board):
    """"Script to move a Card to a specific List"""
    print(move_card_to_list_string.format(list=name_target, board=name_board))
    organization_boards = get_organization_boards()

    # WORKFLOW
    # 01. Get id of Board
    # 02. Get all Lists in Board
    # 03. Get id of target List
    # 04. Move Card to target List

    # 01. Get id of Board
    id_board = get_id(organization_boards, name_board)
    if id_board is not None:
        # 02. Get all Lists in Board
        lists = requests.get(url=get_lists.format(id=id_board)).json()
        # 03. Get id of target List
        id_target = get_id(lists, name_target)
        if id_target is not None:
            # 04. Move Card to target List
            if len(requests.get(url=get_card.format(id=card_id)).json()) > 0:
                requests.put(url=move_card_to_list.format(id=card_id, list=id_target, board=id_board))
                print(successful_move)
            else:
                print(card_not_found)
                print(move_aborted)
        else:
            err_no_list(name_target)
    else:
        err_no_board(name_board)
