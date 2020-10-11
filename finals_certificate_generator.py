import csv

filename = 'individuals_finals_placings.csv'
name_col = 'Name'
country_col = 'Verein'
class_col = 'Klasse'
tournament_col = 'Turnier'
score_col = 'Ringe'
rank_col = 'Rang'

start_code = \
'\\documentclass[17pt,a4paper]{article} \n \
\\usepackage[a4paper, left=11cm, top = 15cm, bottom = 5mm, right = 5mm]{geometry} \n \
\\usepackage[utf8]{inputenc} \n \
\\usepackage[T1]{fontenc} \n \
\\usepackage[ngerman]{babel} \n \
\\usepackage{lmodern} \n \
\n \
\\usepackage[no-math]{fontspec} \n \
\\setmainfont{Comic Sans MS} \n \
\n \
\\author{Thomas Frank} \n \
\\title{PSV Urkunde} \n \
\\begin{document} \n \
	\\pagestyle{empty} \n \
'

page_code = \
'	\\begin{{center}} \n \
		\\fontsize{{26}}{{31}}\selectfont \\textbf{{{name}}}\\\\  \n \
		\\fontsize{{18}}{{24}}\selectfont {club}\\\\ \n \
		\\fontsize{{18}}{{24}}\selectfont belegte beim\\\\ \n \
		\\fontsize{{26}}{{31}}\selectfont \\textbf{{{tournament}}}\\\\ \n \
		\\fontsize{{18}}{{24}}\selectfont in der Klasse\\\\ \n \
		\\fontsize{{26}}{{31}}\selectfont \\textbf{{{clas}}}\\\\ \n \
		\\fontsize{{18}}{{24}}\selectfont den\\\\ \n \
		\\fontsize{{42}}{{50}}\selectfont \\textbf{{{rank}. Rang}}\\\\ \n \
	\\end{{center}} \n \
	\\pagebreak \n \
'

end_code = \
'\end{document}'

def main():
    try:
        csvfile = open(filename, newline='')
    except FileNotFoundError:
        print(f'{filename} was not found')
        return
    reader = csv.DictReader(csvfile)

    print(start_code)
    for row in reader:
        print(page_code.format(
            name = row[name_col],
            club = row[country_col],
            tournament = row[tournament_col],
            clas = row[class_col],
            rank = row[rank_col]
            ))

    print(end_code)

if __name__ == "__main__":
    main()

