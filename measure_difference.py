# Copyright 2018 Duck Duck Go, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# measure_difference.py
# Calculate the difference between sets of search results (organic links only).


from pyxdameraulevenshtein import damerau_levenshtein_distance
import csv
import random
import string
import serp_parser


# Reduce the results to a string of letters for each participant, representing their domain names.
def get_result_strings(unique_domains, results_full):
    strings = {}
    for participant_id, results in results_full.iteritems():
        result_string = ''
        for result in results:
            if result in unique_domains:
                result_string += unique_domains[result]
        strings[participant_id] = result_string
    return strings


# Get a random participant from the results that is different to the specified participant
def get_random_participant(participant_results, participant_id):
    secure_random = random.SystemRandom()
    while True:
        id = secure_random.choice(participant_results.keys())
        if id != participant_id:
            break
    return id


def main():
    query = serp_parser.get_query()
    results_in = serp_parser.get_results(query, 'i')
    results_no = serp_parser.get_results(query, 'n')

    # Prepare dictionary for assignment of domains represented by letters for participants in both modes.
    result_strings = {
        'i': {},
        'n': {}
    }

    # Get a combined list of unique domains for both modes.
    unique_domains_in = serp_parser.get_unique_domains(results_in)
    unique_domains_no = serp_parser.get_unique_domains(results_no)
    unique_domains = unique_domains_in
    unique_domains.update(unique_domains_no)

    # Give each unique domain name a letter of the alphabet, e.g. wikipedia.org = 'A'.
    for i, domain in enumerate(unique_domains):
        unique_domains[domain] = string.uppercase[i]

    result_strings['i'] = get_result_strings(unique_domains, results_in)
    result_strings['n'] = get_result_strings(unique_domains, results_no)

    # Get a dictionary of closest participants
    closest = {}
    closest_filename = 'closest.csv'
    try:
        with open('data/' + closest_filename, 'r') as closest_file:
            closest_data = csv.reader(closest_file, delimiter=',')
            for row in closest_data:
                # Using eval here because we can vouch for where the data is coming from
                closest[row[0]] = eval(row[1])
    except IOError as e:
        print(e)
        print 'Problem reading ' + closest_filename + ' file.'
        exit()

    diff_same_participant = 0.0
    diff_random = 0.0
    diff_closest = 0.0
    for participant_id, result_string in result_strings['i'].iteritems():
        # Get the average difference of each participant's normal and private mode results.
        diff_tmp = damerau_levenshtein_distance(result_string, result_strings['n'][participant_id])
        diff_same_participant += diff_tmp

        # Get the average result difference of each participant and a random participant in private browsing mode.
        random_id = get_random_participant(result_strings['i'], participant_id)
        diff_tmp = damerau_levenshtein_distance(result_string, result_strings['i'][random_id])
        diff_random += diff_tmp
    
        # Get the average result difference of each participant and their five closet participants in private browsing mode.
        diff_tmp = 0.0
        for closest_id in closest[participant_id]:
            diff_tmp += damerau_levenshtein_distance(result_string, result_strings['i'][closest_id])
        diff_closest += (diff_tmp / 5) # Divide by 5 to give us the average of the five closest participants.


    # Print the results
    avg_diff_same_participant = round(diff_same_participant / len(result_strings['i']), 2)
    print 'Average difference of normal and private browsing mode (same user): ' + str(avg_diff_same_participant)

    avg_diff_random = round(diff_random / len(result_strings['i']), 2)
    print 'Average difference of random users (private browsing mode): ' + str(avg_diff_random)

    avg_diff_closest = round(diff_closest / len(result_strings['i']), 2)
    print 'Average difference of geographically closest users (private browsing mode): ' + str(avg_diff_closest)


if __name__ == "__main__":
    main()
