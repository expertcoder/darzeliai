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

def isNaN(num):
    return num != num

def dataframe_to_json_print(df):
    json_string = df.to_json(orient = 'records', force_ascii=False)
    json_object = json.loads(json_string)
    return json.dumps(json_object, indent=4, sort_keys=True, ensure_ascii=False)

def dataframe_to_json_file(df):
    df.to_json('data-v7.json', orient = 'records', force_ascii=False)


def format_dict(dict, arg):
    ndict = {}
    for k, v in dict.items():
        ndict[ k.format(arg) ] = v.format(arg)
    return ndict

def tidy_row(row):

    row['preferences'] = [{} for i in range(PREFERENCE_AMOUNT)]

    for key, value in row.iteritems():

        chunks = key.split('|')
        if len(chunks) == 3:
            ignore, preference_attribute, preference_number = chunks
            preference_number = int(preference_number)
            row['preferences'][ preference_number  - 1][preference_attribute] = value
            row['preferences'][ preference_number  - 1]['preference_number'] = preference_number


    for i, values in enumerate(row['preferences'] ):
        #Some students will haev less than 5 preferences, in this case remove the useless list element
        if isNaN(values['school_name']):
            row['preferences'] = row['preferences'][:i]

    return row

# ---------- begin script ---------

PREFERENCE_AMOUNT = 5


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

df_prefs = pd.read_csv('prefs-short.csv', sep=";", true_values=["Taip"], false_values=["Ne"])

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


preference_columns_template = {'{} pasirinktas darželis': 'preference|school_name|{}',
           '{} darželio vieta eilėje':'preference|translation_needed_darzelio_vieta_eileje|{}',
           '{} darželio Seniūnija':'preference|school_district|{}',
           '{} darželio grupės ugdomoji kalba':'preference|school_language|{}',
           '{} darželio grupės ugdymo metodika':'preference|some_other_info|{}',
           '{} darželio grupės tipas':'preference|age_group|{}',
           '{} darželio grupės amžiaus intervalas':'preference|age_interval|{}',
           'Atitinka {} darželiui priskirta teritorija':'preference|same_territory|{}',
           '{} darželį lanko broliai/seserys':'preference|sibling_at_school|{}',
           'Tinkamų grupių {} darželyje':'preference|if_fit_group|{}'}

preference_columns = {}

for i in range(1,PREFERENCE_AMOUNT + 1):
    preference_columns_formatted = format_dict(preference_columns_template, i)
    preference_columns.update(preference_columns_formatted)
    columns.update(preference_columns_formatted)


df_prefs.rename(inplace=True, columns=columns)

df_prefs = df_prefs.apply(tidy_row, axis=1)


df_prefs.drop(preference_columns.values(), inplace=True, axis=1 )  #Remove the original preference columns which are no longer needed

dataframe_to_json_file(df_prefs )










