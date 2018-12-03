# Copyright 2018 Duck Duck Go, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# count_domains.py
# Count how many domains were shown to each participant and how many times each domain appeared.

import serp_parser


def get_variations(participants, results_full):

    # Prepare a dictionary to store the sources for infoboxes.
    sources = {
        'news': [],
        'videos': []
    }

    # Prepare a dictionary to store variations for our chosen types of result.
    variations = {
        'full': {},
        'news': {},
        'videos': {}
    }

    participant_count = {
        'full': 0, # To count all participants.
        'unique': 0, # To count appearances of unique search results.
        'news': 0, # To count the appearances of News infoboxes.
        'videos': 0 # To count the appearances of Videos infoboxes.
    }

    def analyse_infoboxes(type, result):
        infobox_list = result.split(',')
        # Remove empty items from infobox list
        infoboxes = [x for x in infobox_list if x]
        sources[type] += infoboxes

        if infoboxes:
            participant_count[type] += 1
            if result not in variations[type]:
                variations[type][result] = 1
            else:
                variations[type][result] += 1

    # Loop through the search results to count the number of variations (excluding mobile).
    for participant_id, results in results_full.iteritems():
        if participants[participant_id]['format'] == 'desktop':
            participant_count['full'] += 1
            news_combined = ''
            videos_combined = ''

            for result in results:
                # Get the variation stats for News or Videos infoboxes.
                if 'TS:' in result:
                    news_combined += result + ','
                elif 'V:' in result:
                    videos_combined += result + ','

            # Analyse complete search result variations.
            # Concatenate the list of results into a string so it can be a dictionary key.
            result_combined = ''.join(results)
            if result_combined not in variations['full']:
                variations['full'][result_combined] = 1
            else:
                variations['full'][result_combined] += 1

            analyse_infoboxes('news', news_combined)
            analyse_infoboxes('videos', videos_combined)

    # Iterate through the final dictionary to get the full set of unique results.
    participant_count['unique'] = len([count for (variation, count) in variations['full'].items() if count == 1])

    return sources, variations, participant_count


# Calculate and print more detailed data for infoboxes.
def print_infobox_data(sources, variations, participant_count, type):
    print '\n' + type.title() + ' infobox variations: ' + str(len(variations[type]))

    # Remove duplicates from list of sources and show count.
    source_names = list(set(sources[type]))
    print 'Number of sources for ' + type.title() + ' infoboxes: ' + str(len(source_names))

    # Get percentage of people who saw this type of infobox.
    variation_pct = int(round(float(participant_count[type]) / participant_count['full'] * 100))
    print 'Participants seeing ' + type.title() + ' infoboxes: ' + str(participant_count[type]) + '/' + str(
        participant_count['full']) + ' (' + str(variation_pct) + '%)'

    # Sort the infobox dictionary to get most common occurrence
    variation_max = serp_parser.sort_dict(variations[type])[0][1] if len(variations[type]) > 0 else 0
    print 'Participants seeing most common ' + type.title() + ' variation: ' + str(variation_max)


def main():
    query = serp_parser.get_query()
    mode = serp_parser.get_mode()
    results_full = serp_parser.get_results(query, mode)
    participants = serp_parser.get_participants()

    (sources, variations, participant_count) = get_variations(participants, results_full)

    # Print the results
    print 'Search result variations: ' + str(len(variations['full']))
    unique_pct = int(round(float(participant_count['unique']) / participant_count['full'] * 100))
    print 'Participants seeing unique results: ' + str(participant_count['unique']) + '/' + str(participant_count['full']) + ' (' + str(unique_pct) + '%)'

    print_infobox_data(sources, variations, participant_count, 'news')
    print_infobox_data(sources, variations, participant_count, 'videos')


if __name__ == "__main__":
    main()
