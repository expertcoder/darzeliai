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

def dataframe_to_json_print(df):
    json_string = df.to_json(orient = 'records', force_ascii=False)
    json_object = json.loads(json_string)
    return json.dumps(json_object, indent=4, sort_keys=True, ensure_ascii=False)

def dataframe_to_json_file(df):
    df.to_json('data-v3.json', orient = 'records', force_ascii=False)


def format_dict(dict, arg):
    ndict = {}
    for k, v in dict.items():
        ndict[ k.format(arg) ] = v.format(arg)
    return ndict

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

#Fix error in CSV file.
df_prefs.rename(inplace=True, columns={'Tinkamų grupių 13darželyje': 'Tinkamų grupių 3 darželyje'})

columns = { 'Nr.': 'some_number',
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


dynamic_columns_template = {'{} pasirinktas darželis': 'preference_{}_school_name',
           '{} darželio Seniūnija':'preference_{}_school_district',
           '{} darželio grupės ugdomoji kalba':'preference_{}_school_language',
           '{} darželio grupės ugdymo metodika':'preference_{}_some_other_info',
           '{} darželio grupės tipas':'preference_{}_age_group',
           '{} darželio grupės amžiaus intervalas':'preference_{}_age_interval',
           'Atitinka {} darželiui priskirta teritorija':'preference_{}_same_territory',
           '{} darželį lanko broliai/seserys':'preference_{}_sibling_at_school',
           'Tinkamų grupių {} darželyje':'preference_{}_if_fit_group'}

for i in range(1,6):
    columns.update (format_dict(dynamic_columns_template, i))



def myfunc(row):
    row['preferences'] = []

    # print row
    # sys.exit()

    for i in range(1, 6):
        d = format_dict(dynamic_columns_template, i)
        preferences_dict = {}
        for jk, jv in d.items():

            # print jv
            # print jv
            # sys.exit()

            preferences_dict[jv[13:] ] = row[jv]
        row['preferences'].append(preferences_dict)

    return row



df_prefs.rename(inplace=True, columns=columns)

df_prefs = df_prefs[ columns.values() ]   #TODO quick work around, might not be needed later

df_prefs = df_prefs.apply(myfunc, axis=1)

#Quick hack to remove columns which are no longer needed
for i in range(1,6):
    d = format_dict(dynamic_columns_template, i)
    for jk, jv in d.items():
        del df_prefs[jv ]

dataframe_to_json_file(df_prefs.head() )

# print ( dataframe_to_json(df_prefs.head()) )

# df_merged = pd.merge(df_schools, df_prefs, left_on='name', right_on='preference_1_school_name')









