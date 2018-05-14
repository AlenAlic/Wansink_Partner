from trello.variables import *
########################################################################################################################
# Contains all variables used for Simplicate
########################################################################################################################
# Simplicate codes
VAM = 'VAM'
VAK = 'VAK'
VAJ = 'VAJ'
OBM = 'OBM'
OBK = 'OBK'
OBJ = 'OBJ'
ICM = 'ICM'
ICK = 'ICK'
ICJ = 'ICJ'
PDM = 'PDM'
PDK = 'PDK'
SAM = 'SAM'
VJV = 'VJV'
VPB = 'VPB'
IB1 = 'IB1'
IB2 = 'IB2'
IB3 = 'IB3'
IBP = 'IB+'
IB = 'IB'

# Trello codes
TODO_ADM = 'TODO ADM'
TODO_OB = 'TODO OB'
TODO_ICP = 'TODO ICP'
TODO_PC = 'TODO PC'
TODO_SAM = 'TODO SAM'
TODO_VJV = 'TODO VJV'
TODO_VPB = 'TODO VPB'
TODO_IB = 'TODO IB'
TODO_opstart = 'TODO opstart project'
TODO_sluiten = 'TODO sluiten'

# Categories of codes
monthly_codes = [VAM, OBM, ICM, PDM]
quarterly_codes = [VAK, OBK, ICK, PDK]
yearly_codes = [VAJ, OBJ, ICJ]
jaarwerk_codes = [SAM, VJV, VPB, IB1, IB2, IB3, IBP]
supported_codes = monthly_codes + quarterly_codes + yearly_codes + jaarwerk_codes
filter_types = {'monthly': monthly_codes, 'quarterly': quarterly_codes,
                'monthly_and_quarterly': monthly_codes + quarterly_codes, 'yearly': yearly_codes,
                'jaarwerk': jaarwerk_codes}
periodic_dict = {maand: 'monthly', kwartaal: 'quarterly', jaar: 'yearly'}

# Order of checklists
order_jaarwerk = [TODO_opstart, TODO_SAM, TODO_VJV, TODO_VPB, TODO_IB, TODO_sluiten]
order_periodiek = [TODO_ADM, TODO_OB, TODO_ICP, TODO_PC]
order = order_jaarwerk + order_periodiek

# Linked codes
link_trello_simplicate = {VAK: TODO_ADM, VAM: TODO_ADM, VAJ: TODO_ADM,
                          OBM: TODO_OB, OBK: TODO_OB, OBJ: TODO_OB,
                          ICM: TODO_ICP, ICK: TODO_ICP, ICJ: TODO_ICP,
                          PDM: TODO_PC, PDK: TODO_PC, SAM: TODO_SAM, VJV: TODO_VJV, VPB: TODO_VPB,
                          IB1: TODO_IB, IB2: TODO_IB, IB3: TODO_IB, IBP: TODO_IB}

# Misc.
billing_method = {'employee_tariff': 'Medewerker uurtarief', 'itemtype_tariff': ' Urensoort uurtarief'}
BOEKJAAR = 'Boekjaar '
