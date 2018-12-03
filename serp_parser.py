# Copyright 2018 Duck Duck Go, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# serp_parser.py
# To be used by other analysis scripts.
# Read the CSV files containing Google search results and related data.
# Parse to create dictionaries for later analysis and a participant list.

import csv
import operator
import re

# Global objects
queries = {
    'g': {
        'abbr': 'gc',
        'full': 'gun control'
    },
    'i': {
        'abbr': 'im',
        'full': 'immigration'
    },
    'v': {
        'abbr': 'va',
        'full': 'vaccinations'
    }
}
modes = {
    'i': {
        'abbr': 'in',
        'full': 'private browsing ("incognito") mode'
    },
    'n': {
        'abbr': 'no',
        'full': 'normal mode'
    }
}


# Create a dictionary of participants with "id" as the key.
# Attributes for each participant are "format", "blocker", "browser".
def get_participants():
    participants_filename = 'participants.csv'
    participants = {}
    try:
        reader = csv.DictReader(open('data/' + participants_filename, 'r'))
        for line in reader:
            participants[line['id']] = line
    except IOError as e:
        print(e)
        print 'Problem reading ' + participants_file + ' file.'
    return participants


# Get list of domains classified as local from external CSV file
def get_local_domains():
    local_filename = 'local-domains.csv'
    local_domains = []
    try:
        with open('data/' + local_filename, 'r') as local_file:
            for line in local_file.readlines():
                local_domains.append(line.strip())
    except IOError as e:
        print(e)
        print 'Problem reading ' + local_filename + ' file.'
    return local_domains


# Ask the user which search query they want to analyse.
# Returns a tuple with two-letter query abbreviation and full name
def get_query():
    for key, value in queries.iteritems():
        print "[%s] %s" % (key, value['full'])
    
    user_query = raw_input('\nChoose query to analyse: ')
    if user_query in queries:
        return user_query
    else:
        print 'Sorry, please choose again.'
        return get_query()


# Ask the user which search query they want to analyse.
# Returns a tuple with two-letter query abbreviation and full name
def get_mode():
    for key, value in modes.iteritems():
        print "[%s] %s" % (key, value['full'])
    
    user_mode = raw_input('\nChoose browsing mode: ')
    if user_mode in modes:
        return user_mode
    else:
        print 'Sorry, please choose again.'
        return get_mode()


# Parse the search results, creating a dictionary in the format:
# results: {'101': [result, result, result, ...], '102': [result, result, result, ...]}
def get_results(query, mode='i'):
    print 'Analysing data for "' + queries[query]['full'] + '" search query in ' + modes[mode]['full'] + '...\n'
    
    try:
        results_filename = modes[mode]['abbr'] + '_' + queries[query]['abbr'] + '.csv'
        file_content = open('data/' + results_filename, 'r').read()
        file_lines = file_content.splitlines()
    except IOError as e:
        print(e)
        print 'Problem reading ' + results_filename + ' file.'
        return {}

    results = {}
    result = []
    local_domains = get_local_domains()
    for line in file_lines:
        # Parse the set of results for each participant.
        if re.match('\d', line) is not None:
            participant_id = re.findall('\d+', line)[0]
        elif ':' in line: # Infobox data
            # Replace any city or state-specific infobox sources with Local Source
            for local_domain in local_domains:
                line = line.replace(local_domain, 'Local Source')
            result.append(line)
        elif '.' in line: # Domain names
            # Replace any city or state-specific domains with localdomain.com
            domain = line.strip(',')
            domain = 'localdomain.com' if domain in local_domains else domain
            result.append(domain)
        elif not line.strip(','):
            # At the end of a set of results, add it to the results dictionary
            if participant_id:
                results[participant_id] = result
            result = []

    return results


# Loop through the search results and return the unique domains as a dictionary
def get_unique_domains(results_full):
    unique_domains = {}
    for results in results_full.values():
        for result in results:
            if '.' in result and ':' not in result: # Domain names
                if result in unique_domains:
                    unique_domains[result] += 1
                else:
                    unique_domains[result] = 1
    return unique_domains


# Sort a dictionary by value, returning an ordered list of tuples
def sort_dict(dict_unsorted):
    return sorted(dict_unsorted.items(), key=operator.itemgetter(1), reverse=True)
