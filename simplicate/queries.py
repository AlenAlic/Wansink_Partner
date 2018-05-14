import datetime


########################################################################################################################
# Contains all queries used for in the scripts
########################################################################################################################


# API queries
projects_project = '/projects/project'
projects_service = '/projects/service'
hrm_employee = '/hrm/employee'
services_defaultservice = '/services/defaultservice'


# Filters
created_yesterday = '?q[created][ge]={yesterday}'\
    .format(yesterday=(datetime.date.today() - datetime.timedelta(days=1)).isoformat())
service_of_project = '?q[project_id]={project_id}'
