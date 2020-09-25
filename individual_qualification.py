import csv
import name_lookup

### CONFIG
tournament_name = 'PSV Cup 2020'
filename = 'tournament.csv'
output_filename = 'individual_qualifications_placings.csv'

### OUTPUT CONFIG
out_name_col = 'Name'
out_country_col = 'Verein'
out_class_col = 'Klasse'
out_tournament_col = 'Turnier'
out_score_col = 'Ringe'
out_rank_col = 'Rang'
max_num_per_event = 5

### IANSEO CONFIG
fam_name_col = 'FamilyName'
giv_name_col = 'GivenName'
country_col = 'Country'
division_col = 'Division'
class_col = 'Class'
score_cols = 'D{} Score'
xs_score_cols = 'D{} X'
xs_and_tens_score_cols = 'D{} 10+X'


def main():
    try:
        csvfile = open(filename, newline='')
    except FileNotFoundError:
        print(f'{filename} was not found')
        return
    reader = csv.DictReader(csvfile, delimiter=';')

    results = {}
    for row in reader:
        name = f'{row[giv_name_col]} {row[fam_name_col]}'.strip()
        country = row[country_col].strip()
        division = name_lookup.division_name_lookup[row[division_col]]
        clas = name_lookup.class_name_lookup[row[class_col]]
        counter = 0
        score = 0
        xs = 0
        xs_and_tens = 0
        while True:
            counter += 1
            if score_cols.format(counter) in row.keys():
                score += int(row[score_cols.format(counter)])
                xs += int(row[xs_score_cols.format(counter)])
                xs_and_tens += int(row[xs_and_tens_score_cols.format(counter)])
            else:
                break
        if (row[division_col], row[class_col]) not in results.keys():
            results[(row[division_col], row[class_col])] = []
        results[(row[division_col], row[class_col])]\
            .append(Shooter(name, country, division, clas, score, xs, xs_and_tens))

    # sort
    for key, participants_list in results.items():
        results[key] = sorted(participants_list, key=lambda participant: (participant.score, participant.xs, participant.xs_and_tens), reverse=True)

    # write out table for form letters
    outfile = open(output_filename, 'w', newline='')
    fieldnames = [out_name_col, out_country_col, out_class_col, out_tournament_col, out_score_col, out_rank_col]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for _, participants_list in results.items():
        for rank, participant in enumerate(participants_list[:max_num_per_event], 1):
            writer.writerow({
                out_name_col: participant.name,
                out_country_col: participant.country,
                out_class_col:f'{participant.division} {participant.clas}'.strip(),
                out_tournament_col: tournament_name,
                out_score_col: participant.score,
                out_rank_col: rank
            })


class Shooter:
    def __init__(self, name: str, country: str, division: str, clas: str, score: int, xs: int, xs_and_tens: int):
        self.name = name
        self.country = country
        self.division = division
        self.clas = clas
        self.score = score
        self.xs = xs
        self.xs_and_tens = xs_and_tens


if __name__ == '__main__':
    main()