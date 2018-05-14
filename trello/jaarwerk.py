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
        print('Running Jaarwerk script...')

        organization_boards = get_organization_boards()

        ################################################################################################################
        # Script to move the Cards from the List of a new month (ex. 'Oktober 2017') in the Board "Planning Jaarwerk"
        # to the "Nog te starten" List in the Board "Jaarwerk SAM / VJV"
        ################################################################################################################
        ############################################################
        # ESSENTIAL VARIABLES
        ############################################################
        # Board names
        board_name_source = planning_jaarwerk
        board_name_target = jaarwerk_sam_vjv
        if debug is True:
            board_name_source = dev + board_name_source
            board_name_target = dev + board_name_target
        # List names
        list_name_target = nog_te_starten

        ############################################################
        # WORKFLOW
        ############################################################
        # 01. Get id's of source and target Boards
        # 02. Get source list name from date
        # 03. Get all Lists in source Board
        # 04. Get List id from source Board, given name
        # 05. Get all Lists in target Board
        # 06. Get List id from target Board, given name
        # 07. Move all Cards from source List to target List
        # 08. Archive copied List from target Board

        ############################################################
        # CODE
        ############################################################
        # 01. Get id's of source and target Boards
        board_id_source = get_id(organization_boards, board_name_source)
        board_id_target = get_id(organization_boards, board_name_target)
        # 02. Get source List name from current date
        now = datetime.datetime.now()
        list_name_source = month_dict[now.month] + " " + str(now.year)
        print(move_list_in_board_to_list_in_board
              .format(list_name_source=list_name_source, board_name_source=board_name_source,
                      list_name_target=list_name_target, board_name_target=board_name_target))
        if board_id_source is not None and board_id_target is not None:
            # 03. Get all Lists in source Board
            lists = requests.get(url=get_lists.format(id=board_id_source)).json()
            # 04. Get List id from source Board, given name
            list_id_source = get_id(lists, list_name_source)
            if list_id_source is not None:
                if len(requests.get(url=get_cards.format(id=list_id_source)).json()) > 0:
                    # 05. Get all Lists in target Board
                    lists = requests.get(url=get_lists.format(id=board_id_target)).json()
                    # 06. Get List id from target Board, given name
                    list_id_target = get_id(lists, list_name_target)
                    if list_id_target is not None:
                        # 07. Move all Cards from source List to target List
                        requests.post(url=move_all_cards.format(id=list_id_source,
                                                                board=board_id_target, list=list_id_target))
                        # 08. Archive copied List from target Board
                        requests.put(url=archive_list.format(id=list_id_source))
                        print(successful_move)
                    else:
                        err_no_list_in_board(list_name_target, board_name_target)
                else:
                    print(list_in_board_empty.format(list_name=list_name_source, board=board_name_source))
            else:
                err_no_list_in_board(list_name_source, board_name_source)
        else:
            if board_id_source is None:
                err_no_board(board_name_source)
            if board_id_target is None:
                err_no_board(board_name_target)

        print('Finished.')
    else:
        print('It is not the first work day of the month, did not run monthly items.')
    print('\n')


if __name__ == "__main__":
    main()
