import csv
import name_lookup

### CONFIG
tournament_name = 'PSV Cup 2020'
filename = 'tournament_Matches.csv'
output_filename = 'individuals_finals_placings.csv'

### OUTPUT CONFIG
name_col = 'Name'
country_col = 'Verein'
class_col = 'Klasse'
tournament_col = 'Turnier'
rank_col = 'Rang'
max_num_per_event = 3  # between 1 and 4

### IANSEO CONFIG
event_col = 'Event'
phase_col = 'Phase'
ath1_famname_col = 'Ath1 GivenName'
ath1_givname_col = 'Ath1 FamilyName'
ath1_country_col = 'Ath1 Country'
ath1_winner_col = 'Ath1 Winner'
ath2_famname_col = 'Ath2 GivenName'
ath2_givname_col = 'Ath2 FamilyName'
ath2_country_col = 'Ath2 Country'
ath2_winner_col = 'Ath2 Winner'


def main():
    try:
        csvfile = open(filename, newline='')
    except FileNotFoundError:
        print(f'{filename} was not found')
        return
    reader = csv.DictReader(csvfile, delimiter=';')

    results = {}
    for row in reader:
        if row[event_col] not in results.keys():
            results[row[event_col]] = []

        # gold medal match
        if int(row[phase_col]) == 0:
            results[row[event_col]].append({
                ath1_famname_col: row[ath1_famname_col],
                ath1_givname_col: row[ath1_givname_col],
                ath1_country_col: row[ath1_country_col],
                'Place': 1 if row[ath1_winner_col] == '1' else 2
            })
            results[row[event_col]].append({
                ath1_famname_col: row[ath2_famname_col],
                ath1_givname_col: row[ath2_givname_col],
                ath1_country_col: row[ath2_country_col],
                'Place': 1 if row[ath2_winner_col] == '1' else 2
            })

        # bronze medal match
        if int(row[phase_col]) == 1:
            results[row[event_col]].append({
                ath1_famname_col: row[ath1_famname_col],
                ath1_givname_col: row[ath1_givname_col],
                ath1_country_col: row[ath1_country_col],
                'Place': 3 if row[ath1_winner_col] == '1' else 4
            })
            results[row[event_col]].append({
                ath1_famname_col: row[ath2_famname_col],
                ath1_givname_col: row[ath2_givname_col],
                ath1_country_col: row[ath2_country_col],
                'Place': 3 if row[ath2_winner_col] == '1' else 4
            })

    # sort
    for event, result_list in results.items():
        results[event] = list(sorted(result_list, key=lambda res: res['Place'])[:max_num_per_event])


    # write out table for form letters
    outfile = open(output_filename, 'w', newline='')
    fieldnames = [name_col, country_col, class_col, tournament_col, rank_col]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for event, result_list in results.items():
        for result in result_list:
            name = f'{result[ath1_givname_col]} {result[ath1_famname_col]}'.strip()
            country = f'{result[ath1_country_col]}'.strip()
            class_name = f'{name_lookup.division_name_lookup[event[0]]} {name_lookup.class_name_lookup[event[1:]]}'.strip()
            tournament = tournament_name
            rank = result['Place']

            writer.writerow({
                name_col: name,
                country_col: country,
                class_col: class_name,
                tournament_col: tournament,
                rank_col: rank,
            })




if __name__ == '__main__':
    main()
