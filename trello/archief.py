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
        print('Running Archief script...')

        ################################################################################################################
        # Script to move the Cards from "Klaar" to "Archief" in the Boards "Jaarwerk SAM / VJV" and "Maandwerk"
        ################################################################################################################

        board_name_source1 = jaarwerk_sam_vjv
        board_name_source2 = maandwerk
        if debug is True:
            board_name_source1 = dev + board_name_source1
            board_name_source2 = dev + board_name_source2

        move_cards_in_same_board(name_board=board_name_source1, name_source=klaar, name_target=archief)
        move_cards_in_same_board(name_board=board_name_source2, name_source=klaar, name_target=archief)

        print('Finished')
    else:
        print('It is not the first work day of the month, did not run monthly items.')
    print('\n')


if __name__ == "__main__":
    main()
