"""
Queens College
CSCI 355 - Internet and Web Technologies
Winter 2024
Assignment3.py
Shah Bhuiyan
Worked with the class
"""

import OutputUtils as ou

# [1] Define a function to read in the United States data from file "us-states.csv" into a two-dimensional list.
def read_line(fileName):
    with open(fileName) as file:
        lines = file.readlines()
        states = [line.strip().split(",") for line in lines]
        return states[0], states[1:]


def main():
    header, states = read_line("States.csv")
    for i in range(len(states)):
        name = states[i][0]
        if name == "New York":
            wikiname = "New_York_(state)"
        else:
            wikiname = name
        href = "https://en.wikipedia.org/wiki/" + wikiname.replace(' ', '_')
        a_attributes = 'href="' + href + '" target="_blank"'
        td_cont = ou.create_element(ou.TAG_A, name, a_attributes)
    title = "US States"
    alignments = ["l", "l", "l", "r"]
    types = ["S", "S", "S", "N"]
    outputFile = "Assignment3.html"
    ou.write_html_file(outputFile, title, header, types,alignments,states,open_file=True)

if __name__ == "__main__":
    main()