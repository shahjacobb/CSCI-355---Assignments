import OutputUtils as ou

# [1] Define a function to read in the United States data from file "us-states.csv" into a two-dimensional list..
def read_file(filename):
    with open(filename) as file:
        lines = file.readlines()
        states = [line.strip().split(",") for line in lines]
        return states[0], states[1:]


def main():
    headers, states = read_file("States.csv")
    for i in range(len(states)):
        name = states[i][0]
        if name == "New York":
            wikiname = "New_York_(state)"
        else:
            wikiname = name
        href = "https://en.wikipedia.org/wiki/" + wikiname.replace(' ', '_')
        a_attributes = 'href="' + href + '" target="_blank"'
        td_cont = ou.create_element(ou.TAG_A, name, a_attributes)
        states[i][0] = td_cont
    title = "US States"
    alignments = ["l", "l", "l", "r"]
    types = ["S", "S", "S", "N"]
    output_file = "Assignment3.html"
    ou.write_html_file(output_file, title, headers, types, alignments, states, True)


if __name__ == "__main__":
    main()