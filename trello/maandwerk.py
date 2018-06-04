from trello.functions import *
from global_var import dev
import datetime


def main():
    ############################################################
    # DEBUG
    ############################################################
    debug = False

    ############################################################
    # TIME CHECK
    ############################################################
    today = datetime.date.today()
    day = today.day

    if day == 1 or debug is True:
        print('Running Maandwerk script...')

        organization_boards = get_organization_boards()

        ################################################################################################################
        # Script to COPY the Cards from the List "Maand" or "Kwartaal" in the Board "Planning Periodiek werk"
        # to the "Tod0 deze maand" List in the Board "Maandwerk".
        # Then move the cards from "Tod0 volgende maand" to the "Tod0 deze maand" List in the Board "Maandwerk"
        ################################################################################################################
        ############################################################
        # ESSENTIAL VARIABLES
        ############################################################
        # Board names
        board_name_source = planning_periodiek_werk
        board_name_target = maandwerk
        if debug is True:
            board_name_source = dev + board_name_source
            board_name_target = dev + board_name_target
        # List names
        now = datetime.datetime.now()
        if (now.month - 1) % 3 == 0:
            list_name_source = kwartaal
        else:
            list_name_source = maand
        list_name_target = todo_deze_maand

        ############################################################
        # WORKFLOW
        ############################################################
        # 01. Get id's of source and target Boards
        # 02. Get all Lists in source Board
        # 03. Get List id from source Board, given name
        # 04. Copy source List to target Board
        # 05. Get new source Board id
        # 06. Reset source List id
        # 07. Get all Lists in source Board
        # 08. Get source List id from source Board, given name
        # 09. Get target List id from target Board, given name
        # 10. Get all Cards in source List
        # 11. Rename all Cards in source List
        # 12. Move all cards from source List to target List
        # 13. Archive source List
        # 14. Reset source List id and name
        # 15. Get all Lists in source Board
        # 16. Get source List id from source Board, given name
        # 17. Get all Cards in source List
        # 18. Rename all Cards in source List
        # 19. Move all cards from source List to target List

        ############################################################
        # CODE
        ############################################################
        print(copy_list_in_board_to_board.format(list_name_source=list_name_source, board_name_source=board_name_source,
                                                 board_name_target=board_name_target))
        # 01. Get id's of source and target Boards
        board_id_source = get_id(organization_boards, board_name_source)
        board_id_target = get_id(organization_boards, board_name_target)
        if board_id_source is not None and board_id_target is not None:
            # 02. Get all Lists in source Board
            lists = requests.get(url=get_lists.format(id=board_id_source)).json()
            # 03. Get List id from source Board, given name
            list_id_source = get_id(lists, list_name_source)
            if list_id_source is not None:
                # 04. Copy source List to target Board
                requests.post(url=copy_list.format(name=list_name_source, board=board_id_target, list=list_id_source))
                print(successful_copy)
                # 05. Get new source Board id
                board_id_source = board_id_target
                board_name_source = board_name_target
                # 06. Reset source List id
                list_id_source = None
                # 07. Get all Lists in source Board
                lists = requests.get(url=get_lists.format(id=board_id_source)).json()
                # 08. Get source List id from source Board, given name
                list_id_source = get_id(lists, list_name_source)
                if list_id_source is not None:
                    print(move_list_to_list_in_board.format(name_source=list_name_source, name_target=list_name_target,
                                                            name_board=board_name_target))
                    # 09. Get target List id from target Board, given name
                    list_id_target = get_id(lists, list_name_target)
                    if list_id_target is not None:
                        # 10. Get all Cards in source List
                        cards = requests.get(get_cards.format(id=list_id_source)).json()
                        # 11. Rename all Cards in source List
                        for card in cards:
                            new_name = month_abbreviation_dict[now.month - 1] + " - " + card['name']
                            # TODO lelijke fix verwijderen
                            new_name.replace('&', '%26')
                            requests.put(rename_card.format(id=card['id'], name=new_name))
                        # 12. Move all cards from source List to target List
                        requests.post(url=move_all_cards.format(id=list_id_source, board=board_id_target,
                                                                list=list_id_target))
                        # 13. Archive source List
                        requests.put(url=archive_list.format(id=list_id_source))
                        print(successful_move)

                        # Move the Cards from the List "Tod0 volgende maand"
                        # to the List "Tod0 deze maand" in the Board "Maandwerk"
                        # 14. Reset source List id and name
                        list_id_source = None
                        list_name_source = todo_volgende_maand
                        print(move_list_to_list_in_board
                              .format(name_source=list_name_source, name_target=list_name_target,
                                      name_board=board_name_target))
                        # 15. Get all Lists in source Board
                        lists = requests.get(url=get_lists.format(id=board_id_source)).json()
                        # 16. Get source List id from source Board, given name
                        list_id_source = get_id(lists, list_name_source)
                        if list_id_source is not None:
                            # 17. Get all Cards in source List
                            cards = requests.get(get_cards.format(id=list_id_source)).json()
                            if len(cards) > 0:
                                # 18. Rename all Cards in source List
                                for card in cards:
                                    new_name = month_abbreviation_dict[now.month - 1] + " - " + card['name']
                                    requests.put(rename_card.format(id=card['id'], name=new_name))
                                # 19. Move all cards from source List to target List
                                requests.post(url=move_all_cards.
                                              format(id=list_id_source, board=board_id_target, list=list_id_target))
                                print(successful_move)
                            else:
                                print(list_in_board_empty.format(list_name=list_name_source, board=board_name_source))
                        else:
                            err_no_list_in_board(list_name_source, board_name_source)
                    else:
                        err_no_list_in_board(list_name_target, board_name_target)
                else:
                    err_no_list_in_board(list_name_source, board_name_source)
            else:
                err_no_list_in_board(list_name_source, board_name_source)
        else:
            if board_id_source is None:
                err_no_board(board_name_source)
            if board_id_target is None:
                err_no_board(board_name_target)

        print('Finished')
    else:
        print('It is not the first work day of the month, did not run monthly items.')
    print('\n')


if __name__ == "__main__":
    main()
