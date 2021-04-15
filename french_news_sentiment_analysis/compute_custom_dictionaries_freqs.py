from shared.db_helpers import init_db, fetch_script_from_db
from shared.folders import death_dict_freqs, virus_dict_freqs, vaccine_dict_freqs
from shared.file_read_write import write_to_file
from collections import Counter
import json


def from_counter_from_frequency_dict(counter):
    assert isinstance(counter, Counter)
    total = float(sum(counter.values()))
    counts_dict = dict(counter)
    freqs_dict = {key: (float(count) / total) for key,
                  count in counts_dict.items()}
    del counts_dict
    return dict(sorted(freqs_dict.items(), key=lambda item: item[1], reverse=True))


def compute_custom_dicts_freqs():
    # Load Data
    init_db()
    data = fetch_script_from_db("select_all_from_counts.sql")

    # Group Counters
    death_counter = Counter()
    vaccine_counter = Counter()
    virus_counter = Counter()
    for death, virus, vaccines in data:
        virus_counter += Counter(json.loads(virus))
        death_counter += Counter(json.loads(death))
        vaccine_counter += Counter(json.loads(vaccines))

    # Compute precentage from counts
    virus_freqs = from_counter_from_frequency_dict(virus_counter)
    del virus_counter
    death_freqs = from_counter_from_frequency_dict(death_counter)
    del death_counter
    vaccine_freqs = from_counter_from_frequency_dict(vaccine_counter)
    del vaccine_counter

    # Dump data to json
    write_to_file(virus_freqs, virus_dict_freqs)
    write_to_file(death_freqs, vaccine_dict_freqs)
    write_to_file(vaccine_freqs, death_dict_freqs)


compute_custom_dicts_freqs()
