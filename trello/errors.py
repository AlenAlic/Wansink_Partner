# General Strings
move_aborted = 'Move aborted.\n'
successful_copy = 'Successfully completed copy.'
successful_move = 'Successfully completed move.\n'
card_not_found = 'Card not found.'

# Error Strings
string_err_no_list_in_board = 'Could not find List "{list_name}" in Board "{board}".'
string_no_card_in_list_in_board = 'Could not find Card "{card}" in List "{list_name}" in Board "{board}".'
string_err_no_board = 'Could not find Board "{board}".'
string_err_no_list = 'Could not find List "{list_name}".'


# Error functions
def err_no_list_in_board(list_name, board):
    print(string_err_no_list_in_board.format(list_name=list_name, board=board))
    print(move_aborted)


def err_no_card_in_list_in_board(card, list_name, board):
    print(string_no_card_in_list_in_board.format(card=card, list_name=list_name, board=board))
    print('\n')


def err_no_board(board):
    print(string_err_no_board.format(board=board))
    print(move_aborted)


def err_no_list(list_name):
    print(string_err_no_list.format(list_name=list_name))
    print(move_aborted)
