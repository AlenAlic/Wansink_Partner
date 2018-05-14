from simplicate.functions import *


def main():
    ############################################################
    # DEBUG
    ############################################################
    debug = False

    ####################################################################################################################
    # Description here
    ####################################################################################################################
    print('Creating new Trello Cards from Simplicate Projects ...')

    ############################################################
    # ESSENTIAL VARIABLES
    ############################################################
    # Source projects, get TEST projects if debug is True
    if debug:
        projects = simplicate_request('GET', projects_project, '?q[created][ge]=2018-04-19&q[name]=*TEST -*')
        # projects = get_req(projects_project, '?q[created][ge]=2018-04-19')
    else:
        projects = simplicate_request('GET', projects_project, created_yesterday)

    # Check in which category each project belongs and create the necessary Cards
    for project in projects:
        print('Creating cards for project: {}'.format(project['name']))

        # All services that belong to a specific project
        services = simplicate_request('GET', projects_service, service_of_project.format(project_id=project['id']))
        for service in services:
            if service['default_service_id'] in default_services:
                service['name'] = default_services[service['default_service_id']]

        if is_monthly(services) and is_quarterly(services):
            # Create card in "Maand" List in Board "Planning Periodiek werk"
            card_id = create_card_from_simplicate(project=project, services=filter_services(services, 'monthly'),
                                                  board_name=planning_periodiek_werk, list_name_source=sjabloon,
                                                  list_name_target=maand, card_name_source=sjabloon, debug=debug)
            # Create card in "Kwartaal" List in Board "Planning Periodiek werk"
            card_id = create_card_from_simplicate(project=project,
                                                  services=filter_services(services, 'monthly_and_quarterly'),
                                                  board_name=planning_periodiek_werk, list_name_source=sjabloon,
                                                  list_name_target=kwartaal, card_name_source=sjabloon, debug=debug)
        elif is_monthly(services):
            # Create card in "Maand" List in Board "Planning Periodiek werk"
            card_id = create_card_from_simplicate(project=project, services=filter_services(services, 'monthly'),
                                                  board_name=planning_periodiek_werk, list_name_source=sjabloon,
                                                  list_name_target=maand, card_name_source=sjabloon, debug=debug)
            # Create card in "Kwartaal" List in Board "Planning Periodiek werk"
            card_id = create_card_from_simplicate(project=project, services=filter_services(services, 'monthly'),
                                                  board_name=planning_periodiek_werk, list_name_source=sjabloon,
                                                  list_name_target=kwartaal, card_name_source=sjabloon, debug=debug)
        elif is_quarterly(services):
            # Create card in "Maand" List in Board "Planning Periodiek werk"
            card_id = create_card_from_simplicate(project=project, services=filter_services(services, 'quarterly'),
                                                  board_name=planning_periodiek_werk, list_name_source=sjabloon,
                                                  list_name_target=kwartaal, card_name_source=sjabloon, debug=debug)

        if is_yearly(services):
            # Create card in "Jaar" List in Board "Planning Periodiek werk"
            card_id = create_card_from_simplicate(project=project, services=filter_services(services, 'yearly'),
                                                  board_name=planning_periodiek_werk, list_name_source=sjabloon,
                                                  list_name_target=jaar, card_name_source=sjabloon, debug=debug)
        if is_jaarwerk(services):
            # Create card in "Afspraken planning volgend jaar" List in Board "Planning Jaarwerk"
            card_id = create_card_from_simplicate(project=project, services=filter_services(services, 'jaarwerk'),
                                                  board_name=planning_jaarwerk, list_name_source=how_to_use,
                                                  list_name_target=planning_volgend_jaar, card_name_source=sjablonen,
                                                  debug=debug)
            # Move card to List "Simplicate Automatisering - uitzonderingen" List in Board "Nog te plannen" if it
            # only has IB* services
            if all(service['name'].startswith(IB) for service in services):
                move_card_to_specific_list(card_id=card_id, name_target=simplicate_uitzonderingen,
                                           name_board=dev + nog_te_plannen if debug else nog_te_plannen)
        if is_exception(services):
            # Create card in "Simplicate Automatisering - uitzonderingen" List in Board "Nog te plannen"
            card_id = create_card_from_simplicate(project=project, board_name=nog_te_plannen, exception=True,
                                                  list_name_target=simplicate_uitzonderingen, debug=debug)

    print('Done')


if __name__ == "__main__":
    main()
