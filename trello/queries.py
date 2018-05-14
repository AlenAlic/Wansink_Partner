from authentication.trello import *
# from trello.authentication import *

########################################################################################################################
# Contains all queries used for in the scripts
########################################################################################################################

# GET - Get Boards from organization
get_boards_organization = "https://api.trello.com/1/organizations/{org}/boards?filter=all&fields=name%2Cid" \
                          "&key={key}&token={token}".format(org=organization_id, key=APIkey, token=token)
# GET - Get Lists from Board
get_lists = "https://api.trello.com/1/boards/{id}/lists?fields=name%2Cid&key={key}&token={token}"\
    .format(id='{id}', key=APIkey, token=token)
# GET - Get Cards from List
get_cards = "https://api.trello.com/1/lists/{id}/cards?fields=name%2Cid&key={key}&token={token}"\
    .format(id='{id}', key=APIkey, token=token)
# GET - Get Checklist id from Card
get_checklists = "https://api.trello.com/1/cards/{id}/checklists?checkItems=all&checkItem_fields=all&filter=all&" \
                 "fields=all&key={key}&token={token}".format(id='{id}', key=APIkey, token=token)
# GET - Get members in a Organization
get_members = "https://api.trello.com/1/organizations/{org}/members?filter=all&key={key}&token={token}"\
    .format(org=organization_id, key=APIkey, token=token)
# GET - Get specific card
get_card = "https://api.trello.com/1/cards/{id}?key={key}&token={token}".format(id='{id}', key=APIkey, token=token)


# POST - Move all Cards to a List
move_all_cards = "https://api.trello.com/1/lists/{id}/moveAllCards?idBoard={board}&idList={list}" \
                 "&key={key}&token={token}".format(id='{id}', board='{board}', list='{list}', key=APIkey, token=token)
# POST - Copy List to a Board
copy_list = "https://api.trello.com/1/lists?name={name}&idBoard={board}&idListSource={list}&key={key}&token={token}"\
    .format(name='{name}', board='{board}', list='{list}', key=APIkey, token=token)
# POST - Copy Card to List
copy_card = "https://api.trello.com/1/cards?idList={list}&idCardSource={card}&key={key}&token={token}"\
    .format(list='{list}', card='{card}', key=APIkey, token=token)
# POST - Create Card in a List
create_card = "https://api.trello.com/1/cards?name={name}&desc={desc}&idList={list}&idMembers={member}" \
              "&key={key}&token={token}".format(name='{name}', desc='{desc}', list='{list}', member='{member}',
                                                key=APIkey, token=token)
# POST - Create Checklist in a Card
create_checklist = "https://api.trello.com/1/cards/{card_id}/checklists?idChecklistSource={checklist_id}&pos=bottom" \
                   "&key={key}&token={token}".format(card_id='{card_id}', checklist_id='{checklist_id}',
                                                     key=APIkey, token=token)


# PUT - Archive List
archive_list = "https://api.trello.com/1/lists/{id}?closed=true&key={key}&token={token}"\
    .format(id='{id}', key=APIkey, token=token)
# PUT - Rename Card
rename_card = "https://api.trello.com/1/cards/{id}?name={name}&key={key}&token={token}"\
    .format(id='{id}', name='{name}', key=APIkey, token=token)
# PUT - Move Card to List
move_card_to_list = "https://api.trello.com/1/cards/{id}?idList={list}&idBoard={board}&key={key}&token={token}" \
    .format(id='{id}', list='{list}', board='{board}', key=APIkey, token=token)
