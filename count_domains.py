# Copyright 2018 Duck Duck Go, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# count_domains.py
# Count how many domains were shown to each participant and how many times each domain appeared.

import serp_parser


def main():
    query = serp_parser.get_query()
    mode = serp_parser.get_mode()
    results_full = serp_parser.get_results(query, mode)

    unique_domains = serp_parser.get_unique_domains(results_full)
    unique_domains = serp_parser.sort_dict(unique_domains)

    # Print the results
    print 'Unique domains shown (organic links only): ' + str(len(unique_domains))
    print '\nDomain occurrences (organic links only): '
    for domain, count in unique_domains:
        occurrence_pct = int(round(float(count) / len(results_full) * 100))
        print '-- ' + domain + ': ' + str(count) + ' (' + str(occurrence_pct) + '%)'


if __name__ == "__main__":
    main()
