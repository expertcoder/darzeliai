#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Author: sam@expertcoder.io
Since: April 2017

Python 2.7
"""

import pandas as pd
import sys
import numpy as np
import json

def dataframe_to_json(df):
    json_string = df.to_json(orient = 'records', force_ascii=False)
    json_object = json.loads(json_string)
    return json.dumps(json_object, indent=4, sort_keys=True, ensure_ascii=False)


df_schools = pd.read_csv('schools.csv', sep=";")

df_schools.rename(inplace=True, columns={'ID': 'municipality_internal_id',
                        'LABEL': 'name',
                        'LEFT(ADDRESS, 256)': 'address',
                        'SCHOOLNO': 'school_ident',
                        'WWW': 'website',
                        'SCHOOL_TYPE': 'school_type',
                        'BUILDDATE': 'build_date',
                        'REGION_TYPE': 'region_type',
                        'ELDERATE_ID': 'elderate_id',
                        'GIS_X': 'gis_x',
                        'GIS_Y': 'gis_y'
                        })

df_prefs = pd.read_csv('prefs.csv', sep=";", true_values=["Taip"], false_values=["Ne"])

prefs_columns = { 'Nr.': 'some_number',
           'Registracijos numeris': 'registration_number',
           'Prašymo pateikimo data': 'application_data',
           'Vaiko Identifikacinis Nr.': 'student_ident',
           'Vaiko gimimo data': 'dob',
           'Lankymo data': 'application_date',
           'Vaiko seniunija': 'district_where_registered',
           'Prioritetas (deklaruotas mieste)': 'priority_registered_in_city',
           'Prioritetas (šeimoje 3 ir daugiau vaikų)': 'priority_three_children',
           'Prioritetas (žemas darbingumo lygis)':'priority_low_working_capacity',
           'Prioritetas (augina tik vienas iš tėvų)':'priority_single_parent',
           }


# for i in range(1,6):
#     columns.update (  {'1 pasirinktas darželis':'preference_1_school_name',
#            '1 darželio Seniūnija':'preference_1_school_district',
#            '1 darželio grupės ugdomoji kalba':'preference_1_school_language',
#            '1 darželio grupės ugdymo metodika':'preference_1_some_other_info',
#            '1 darželio grupės tipas':'preference_1_age_group',
#            '1 darželio grupės amžiaus intervalas':'preference_1_age_interval',
#            'Atitinka 1 darželiui priskirta teritorija':'preference_1_same_territory',
#            '1 darželį lanko broliai/seserys':'preference_1_sibling_at_school',
#            'Tinkamų grupių 1 darželyje':'preference_1_if_fit_group'}
#  )
#
# print (columns)


df_prefs.rename(inplace=True, columns=prefs_columns)

df_prefs = df_prefs[ prefs_columns.values() ]   #TODO quick work around, might not be needed later

print ( dataframe_to_json(df_prefs) )

# df_merged = pd.merge(df_schools, df_prefs, left_on='name', right_on='preference_1_school_name')









