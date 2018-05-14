from authentication.simplicate import *
# from simplicate.authentication import *
from simplicate.variables import *
from simplicate.queries import *
from global_var import dev
from trello.functions import *

req_data = {'Authentication-Key': AUTHkey, 'Authentication-Secret': AUTHsecret}


########################################################################################################################
# General request functions used by the scripts for Simplicate
########################################################################################################################
def simplicate_request(method, api, simplicate_filter='', headers=None):
    if method not in ['GET']:
        raise Exception('"{method}" is not a valid HTTP method.'.format(method=method))
    url = 'https://{your_domain}.simplicate.nl/api/v2{api}{simplicate_filter}'\
        .format(your_domain=organization_domain, api=api, simplicate_filter=simplicate_filter)
    r = requests.request(method=method, url=url, headers=req_data if headers is None else req_data.update(headers))\
        .json()
    if r['errors'] is None:
        return r['data']
    else:
        raise Exception('Errors with API call: {}'.format(r['errors']))


########################################################################################################################
# Global data pulled only once from the servers
########################################################################################################################
organization_boards = get_organization_boards()
trello_member_list = get_member_list()
default_services = {ds['id']: ds['name'] for ds in simplicate_request('GET', services_defaultservice)}


########################################################################################################################
# All functions used by the scripts
########################################################################################################################
def get_service_codes(list_of_services):
    return [service['name'][:3] for service in list_of_services]


def is_monthly(list_of_services):
    return not set(get_service_codes(list_of_services)).isdisjoint(monthly_codes)


def is_quarterly(list_of_services):
    return not set(get_service_codes(list_of_services)).isdisjoint(quarterly_codes)


def is_yearly(list_of_services):
    return not set(get_service_codes(list_of_services)).isdisjoint(yearly_codes)


def is_jaarwerk(list_of_services):
    return not set(get_service_codes(list_of_services)).isdisjoint(jaarwerk_codes)


def is_exception(list_of_services):
    return set(get_service_codes(list_of_services)).isdisjoint(supported_codes)


def get_checklist_ids(list_of_checklists, list_of_services):
    list_of_checklists = sorted(list_of_checklists, key=lambda o: (order.index(o['name'])))
    checklist_ids = [checklist['id'] for checklist in list_of_checklists
                     if checklist['name'] in get_trello_checklist(list_of_services)]
    return checklist_ids


def get_trello_checklist(list_of_services):
    checklist_names = [link_trello_simplicate[simp_code] for simp_code in get_service_codes(list_of_services)]
    if is_jaarwerk(list_of_services):
        if all(service['name'].startswith(IB) for service in list_of_services):
            return checklist_names
        else:
            return [TODO_opstart] + checklist_names + [TODO_sluiten]
    else:
        return checklist_names


def filter_services(list_of_services, project_type):
    types = [key for key in filter_types]
    if project_type not in types:
        raise ValueError("Invalid sim type. Expected one of: %s" % types)
    services = []
    for service in list_of_services:
        if get_service_codes([service])[0] in filter_types[project_type]:
            services.append(service)
    return services


def get_trello_member_id(trello_members_list, simplicate_employee):
    try:
        return [member['id'] for member in trello_members_list if member['fullName'] == simplicate_employee][0]
    except IndexError:
        return ''


def create_description(project):
    desc = 'SIM\n\n'
    desc += 'Link naar project:\n' + project['simplicate_url']
    if project['billable']:
        desc += '\n\n' + 'Factuurmethode:\n' + billing_method[project['hours_rate_type']]
    if 'note' in project:
        desc += '\n\n' + 'Notities:\n' + project['note']
    return desc


def create_card_from_simplicate(project, board_name, list_name_target, debug, exception=False, services=None,
                                list_name_source=None, card_name_source=None):
    if debug is True:
        board_name = dev + board_name
    # Name Trello Card, depending on if the Simplicate Project is for a organization or a person
    if 'organization' in project:
        card_name_target = project['organization']['name']
    else:
        card_name_target = project['name']
    # Add "- Boekjaar xxxx" to Card name if it goes to the Board "Planning Jaarwerk"
    if board_name == planning_jaarwerk or board_name == (dev + planning_jaarwerk):
        if project['name'].lower().startswith(BOEKJAAR.lower()):
            card_name_target += ' - ' + BOEKJAAR + project['name'].replace(BOEKJAAR, '')[:4]

    # WORKFLOW
    # 01. Get id of Board
    # 02. Get all Lists in Board
    # 03. Get target List id from Board, given name
    # NORMAL CARD
    # 04. Get source List id from Board, given name
    # 05. Get source Card id from source List, given name
    # 06. Get checklist id's that need to be copied over
    # 07. Create target Card
    # 08. Get target Card id from target List, given name
    # 09. Add checklists to target Card
    # EXCEPTION CARD
    # 04. Create target Card
    # 05. Get target Card id from target List, given name

    # 01. Get id of Board
    board_id_target = get_id(organization_boards, board_name)
    if board_id_target is not None:
        # 02. Get all Lists in Board
        lists = requests.get(url=get_lists.format(id=board_id_target)).json()
        # 03. Get target List id from Board, given name
        list_id_target = get_id(lists, list_name_target)
        if list_id_target is not None:
            if not exception:
                # 04. Get source List id from Board, given name
                list_id_source = get_id(lists, list_name_source)
                if list_id_source is not None:
                    # 05. Get source Card id from source List, given name
                    cards = requests.get(get_cards.format(id=list_id_source)).json()
                    card_id_source = get_id(cards, card_name_source)
                    if card_id_source is not None:
                        # 06. Get checklist id's that need to be copied over
                        checklists = requests.get(get_checklists.format(id=card_id_source)).json()
                        checklist_ids = get_checklist_ids(checklists, services)
                        # 07. Create target Card
                        requests.post(url=create_card
                                      .format(name=card_name_target, list=list_id_target,
                                              member=get_trello_member_id(trello_member_list,
                                                                          project['project_manager']['name']),
                                              desc=create_description(project)))
                        # 08. Get target Card id from target List, given name
                        cards = requests.get(get_cards.format(id=list_id_target)).json()
                        card_id_target = get_id(cards, card_name_target)
                        if card_id_target is not None:
                            # 09. Add checklists to target Card
                            for checklist_id in checklist_ids:
                                requests.post(url=create_checklist.format(card_id=card_id_target,
                                                                          checklist_id=checklist_id))
                            if list_name_target in periodic_dict:
                                print('Created {period} card for {name} in List {list} on Board {board}'
                                      .format(name=card_name_target, list=list_name_target, board=board_name,
                                              period=periodic_dict[list_name_target]))
                            else:
                                print(created_card_in_list_on_board
                                      .format(name=card_name_target, list=list_name_target, board=board_name))
                            return card_id_target
                        else:
                            err_no_card_in_list_in_board(card_id_target, list_name_target, board_name)
                    else:
                        err_no_card_in_list_in_board(card_name_source, list_name_source, board_name)
                else:
                    err_no_list_in_board(list_name_source, board_name)
            else:
                # 04. Create target Card
                requests.post(url=create_card
                              .format(name=card_name_target, list=list_id_target,
                                      member=get_trello_member_id(trello_member_list,
                                                                  project['project_manager']['name']),
                                      desc=create_description(project)))
                # 05. Get target Card id from target List, given name
                cards = requests.get(get_cards.format(id=list_id_target)).json()
                card_id_target = get_id(cards, card_name_target)
                if card_id_target is not None:
                    print('Created card for {name} in List {list} on Board {board}'
                          .format(name=card_name_target, list=list_name_target, board=board_name))
                    return card_id_target
                else:
                    err_no_card_in_list_in_board(card_id_target, list_name_target, board_name)
        else:
            err_no_list_in_board(list_name_target, board_name)
    else:
        err_no_board(board_name)
