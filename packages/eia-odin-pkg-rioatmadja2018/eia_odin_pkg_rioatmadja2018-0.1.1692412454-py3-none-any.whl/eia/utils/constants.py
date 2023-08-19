#!/usr/bin/env python3
from typing import List, Dict

API_KEY: str = "Z58UNXyRhL0iDpZUtj6aZPhN9y2nHH7OHPBRXT5i"
STATE: List[str] = ["California", "Colorado", "Florida", "Massachusetts", "Minnesota", "New York", "Ohio", "Texas", "Washington"]
REGION: Dict = {'New York': 'East Coast',
                 'Massachusetts': 'East Coast',
                 'Ohio': 'Midwest',
                 'Minnesota': 'Midwest',
                 'Texas': 'Gulf Coast',
                 'Florida': 'Gulf Coast',
                 'Colorado': 'Rocky Mountain',
                 'California': 'West Coast',
                 'Washington': 'West Coast'}

REGION_REVERSE: Dict = {'East Coast': 'Massachusetts',
                        'MidWest': 'Minnesota',
                        'Gulf Coast': 'Florida',
                        'Rocky Mountain': 'Colorado',
                        'West Coast': 'Washington'}

MOVEMENT_FACETS: Dict = {'Gulf Coast': 'MTTNRP31',
                         'West Coast': 'MTTNRP51',
                         'East Coast': 'MTTNRP11',
                         'Rocky Mountain': 'MTTNRP41',
                         'Midwest' : 'MTTNRP21'}

PRICING_FACETS: Dict = {'Florida': 'EMM_EPMR_PTE_R30_DPG',
                        'Texas': 'EMM_EPMR_PTE_R30_DPG',
                        'Colorado': 'EMM_EPM0U_PTE_SCO_DPG',
                        'Minnesota': 'EMM_EPM0U_PTE_SMN_DPG',
                        'Ohio': 'EMD_EPD2DXL0_PTE_R20_DPG',
                        'California': 'EMM_EPMRU_PTE_R50_DPG',
                        'Washington': 'EMM_EPMRU_PTE_R50_DPG',
                        'Massachusetts': 'EMM_EPMPU_PTE_R10_DPG',
                        'New York': 'EMM_EPMPU_PTE_R10_DPG'}

PRODUCTION_FACETS: Dict = {'California': 'MCRFPCA2',
                           'Colorado': 'MCRFPP42',
                           'Florida': 'MCRFPP31',
                           'Texas': 'MCRFPP31',
                           'Massachusetts': 'MCRFPP12',
                           'New York': 'MCRFPNY2',
                           'Washington': 'MCRFPP51',
                           'Minnesota': 'MCRFPP22',
                           'Ohio': 'MCRFPP22'}

REFINING_PROCESSING_FACETS: Dict = {'California': 'W_EPOOXE_YOP_R50_MBBLD',
                                    'Washington': 'W_EPOOXE_YOP_R50_MBBLD',
                                    'Minnesota': 'W_EPOOXE_YOP_R20_MBBLD',
                                    'Ohio': 'W_EPOOXE_YOP_R20_MBBLD',
                                    'Massachusetts': 'W_EPOOXE_YOP_R10_MBBLD',
                                    'New York': 'W_EPOOXE_YOP_R10_MBBLD',
                                    'Colorado': 'W_EPOOXE_YOP_R40_MBBLD',
                                    'Florida': 'W_EPOOXE_YOP_R30_MBBLD',
                                    'Texas': 'W_EPOOXE_YOP_R30_MBBLD'}

IMPORT_EXPORT_FACETS: Dict = {'California': 'WDIIM_R50-Z00_2',
                              'Colorado': 'W_EPPO6_IM0_R40-Z00_MBBLD',
                              'Washington': 'WDIIM_R50-Z00_2',
                              'Massachusetts': 'WG6IM_R10-Z00_2',
                              'New York': 'WG6IM_R10-Z00_2',
                              'Minnesota': 'WCEIMP22',
                              'Ohio': 'WCEIMP22',
                              'Florida': 'WG4IM_R30-Z00_2',
                              'Texas': 'WG4IM_R30-Z00_2'}

ODIN_DB: str = "44.192.127.255"

DB_DASHBOARD_COLUMNS: List[str] = ['area_name',
                                     'month',
                                     'period',
                                     'process_name',
                                     'product_name',
                                     'quarter',
                                     'units',
                                     'value',
                                     'year']

INVERSE_STATES: Dict = {'AL': 'Alabama',
 'AK': 'Alaska',
 'AZ': 'Arizona',
 'AR': 'Arkansas',
 'CA': 'California',
 'CO': 'Colorado',
 'CT': 'Connecticut',
 'DE': 'Delaware',
 'FL': 'Florida',
 'GA': 'Georgia',
 'HI': 'Hawaii',
 'ID': 'Idaho',
 'IL': 'Illinois',
 'IN': 'Indiana',
 'IA': 'Iowa',
 'KS': 'Kansas',
 'KY': 'Kentucky',
 'LA': 'Louisiana',
 'ME': 'Maine',
 'MD': 'Maryland',
 'MA': 'Massachusetts',
 'MI': 'Michigan',
 'MN': 'Minnesota',
 'MS': 'Mississippi',
 'MO': 'Missouri',
 'MT': 'Montana',
 'NE': 'Nebraska',
 'NV': 'Nevada',
 'NH': 'New Hampshire',
 'NJ': 'New Jersey',
 'NM': 'New Mexico',
 'NY': 'New York',
 'NC': 'North Carolina',
 'ND': 'North Dakota',
 'OH': 'Ohio',
 'OK': 'Oklahoma',
 'OR': 'Oregon',
 'PA': 'Pennsylvania',
 'PR': 'Puerto Rico',
 'RI': 'Rhode Island',
 'SC': 'South Carolina',
 'SD': 'South Dakota',
 'TN': 'Tennessee',
 'TX': 'Texas',
 'UT': 'Utah',
 'VT': 'Vermont',
 'VA': 'Virginia',
 'WA': 'Washington',
 'WV': 'West Virginia',
 'WI': 'Wisconsin',
 'WY': 'Wyoming'}

STATES_LOOKUP: Dict = {'Alabama': 'AL',
 'Alaska': 'AK',
 'Arizona': 'AZ',
 'Arkansas': 'AR',
 'California': 'CA',
 'Colorado': 'CO',
 'Connecticut': 'CT',
 'Delaware': 'DE',
 'Florida': 'FL',
 'Georgia': 'GA',
 'Hawaii': 'HI',
 'Idaho': 'ID',
 'Illinois': 'IL',
 'Indiana': 'IN',
 'Iowa': 'IA',
 'Kansas': 'KS',
 'Kentucky': 'KY',
 'Louisiana': 'LA',
 'Maine': 'ME',
 'Maryland': 'MD',
 'Massachusetts': 'MA',
 'Michigan': 'MI',
 'Minnesota': 'MN',
 'Mississippi': 'MS',
 'Missouri': 'MO',
 'Montana': 'MT',
 'Nebraska': 'NE',
 'Nevada': 'NV',
 'New Hampshire': 'NH',
 'New Jersey': 'NJ',
 'New Mexico': 'NM',
 'New York': 'NY',
 'North Carolina': 'NC',
 'North Dakota': 'ND',
 'Ohio': 'OH',
 'Oklahoma': 'OK',
 'Oregon': 'OR',
 'Pennsylvania': 'PA',
 'Puerto Rico': 'PR',
 'Rhode Island': 'RI',
 'South Carolina': 'SC',
 'South Dakota': 'SD',
 'Tennessee': 'TN',
 'Texas': 'TX',
 'Utah': 'UT',
 'Vermont': 'VT',
 'Virginia': 'VA',
 'Washington': 'WA',
 'West Virginia': 'WV',
 'Wisconsin': 'WI',
 'Wyoming': 'WY'}










