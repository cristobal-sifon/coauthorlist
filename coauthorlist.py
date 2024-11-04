from argparse import ArgumentParser
import pandas as pd
import numpy as np

### Modify these ###

# comment this line if there are no acknowledgements other than the authors' ones
general_acknowledgements = "We thank Jakob Dietl for sharing the eROSITA contours for the Abell 3651/3667 system."


def rename_columns(tbl):
    """Rename columns for easier use. Note that modifying the new names
    will require also modifying the main code accordingly"""
    tbl = tbl.rename(
        columns={
            "Latex-formatted name": "name",
            'Affiliation(s). Please separate multiple affiliations with semi-colons ";"': "affiliation",
            "Acknowledgements": "acknowledgements",
        }
    )
    return tbl


def last_name_index(name):
    """Special rules for identifying last names for alphabetical ordering.

    Here ``idx`` is the index of the last name in the entry (counting from zero)"""
    # the last name is not always the last word
    if "Jr" in name or "Hugo" in name or "Mendes" in name:
        idx = 1
    elif "Castelli" in name:
        idx = 2
    # but most of the time it is
    else:
        idx = -1
    return idx


def format_affiliation(affiliation, journal):
    """Format affiliations following journal requirements. Only A&A implemented so far"""
    # for generality let's assume there's more than one affiliation
    affiliation = affiliation.split(";")
    for i, aff in enumerate(affiliation):
        if journal == "aap":
            if "\\affiliation" in aff:
                affiliation[i] = aff[: aff.rfind("}")]
            affiliation[i] = aff.replace("\\affiliation{", "")
    # we now merge it into one string
    return ";".join(affiliation)


### These generally do not need to be modified ###


def parse_args():
    parser = ArgumentParser(
        description="Construct Latex-formatted author list, ordered affiliations, and \
            acknowledgements from a table. See README.rst for more information."
    )
    parser.add_argument(
        "filename",
        help="Input file with author data. Easiest to use are Excel and CSV files",
    )
    parser.add_argument(
        "--alphabetical",
        "-a",
        nargs="*",
        default=[-1],
        type=int,
        help="""Which tiers to sort alphabetically,counting from 1.
Negative numbers indicate which tiers *not* to sort alphabetically.
Default  (-1) means to sort all tiers except the first.""",
    )
    parser.add_argument(
        "--journal",
        "-j",
        default="aap",
        help="Journal style (using AASTeX abbreviation). Only A&A (aap) implemented so far.",
        choices=["aap"],
    )
    parser.add_argument(
        "--orcidlink",
        "-l",
        action="store_true",
        help="Use \\orcidlink macro instead of custom \\orcid macro",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="authors.tex",
        help="filename to write author and affiliation lists (tex A&A format; default authors.tex)",
    )
    parser.add_argument(
        "--output-ack",
        "-k",
        default="acknowledgements.tex",
        help="filename to write acknowledgement list (default acknowledgements.tex)",
    )
    args = parser.parse_args()
    print(args.alphabetical)
    assert np.all(np.array(args.alphabetical) < 0) or np.all(
        np.array(args.alphabetical) > 0
    ), "Alphabetical tiers must be defined only through those which are alphabetical (positive) \
        or only through those that are not alphabetical (negative)"
    return args


###############
## Main code ##
###############

args = parse_args()
if args.orcidlink:
    print(
        """
**Note**: using \\orcidlink macro. Make sure to \\usepackage{orcidlink} in your tex file"""
    )
else:
    print(
        """
**Note**: using custom \\orcid macro. Please add the following to your tex file:
    \\newcommand{\\orcid}[2]{\href{https://orcid.org/#1}{#2}}
"""
    )
# read the data with some flexibility
if args.filename.split(".")[-1][:3] == "xls":
    read = pd.read_excel
elif args.filename.split(".")[-1] == "csv":
    read = pd.read_csv
else:
    read = pd.read_table
tbl = read(args.filename, na_filter=False)
tbl = rename_columns(tbl)
# is there more than one tier?
if "Tier" in tbl.columns:
    tiers = np.unique(tbl["Tier"])
    nt = tiers.size
    print(f"Found {nt} tiers")
else:
    nt = 1
    print("No Tier column found. Assuming only one tier")
print()
# create one list per tier
names = [[] for i in range(nt)]
last_names = [[] for i in range(nt)]
affils = [[] for i in range(nt)]
acks = [[] for i in range(nt)]

# let's go through each author
for i, author in tbl.iterrows():
    tier = author["Tier"] - 1
    if tier == -1:
        continue
    # replace spaces in author names with ~ to ensure there are no line breaks
    n = author["name"].replace("\\ ", " ").replace(" ", "~")
    # orcid linking
    if author["ORCID"]:
        o = author["ORCID"].split("/")[-1]
        if args.orcidlink:
            names[tier].append(f"{n}\\orcidlink{{{o}}}")
        else:
            names[tier].append(f"\orcid{{{o}}}{{{n}}}")
    else:
        names[tier].append(n)
    # find last name according to specified rules
    idx = last_name_index(n)
    last_names[tier].append(n.split("~")[idx])
    affil = format_affiliation(author["affiliation"], args.journal)
    # account for a few weird characters and split multiple affiliations
    affils[tier].append(
        affil.strip().replace("  ", " ").replace(" &", " \&").split(";")
    )
    ack = author["acknowledgements"]
    if len(ack) == 0:
        acks[tier].append("%")
    else:
        if ack[-1] != ".":
            ack = f"{ack}."
        acks[tier].append(ack)

# sort alphatically by last name (except Tier 1)
a = args.alphabetical
for i in range(nt):
    print(f" - Tier {i+1}, unsorted - ")
    print(", ".join(last_names[i]))
    if ((a[0] > 0) and (i + 1 in a)) or ((a[0] < 0) and (-(i + 1) not in a)):
        jsort = np.argsort(last_names[i])
        names[i] = [names[i][j] for j in jsort]
        last_names[i] = [last_names[i][j] for j in jsort]
        affils[i] = [affils[i][j] for j in jsort]
        acks[i] = [acks[i][j] for j in jsort]
        print(f" - Tier {i+1}, sorted - ")
        print(", ".join(last_names[i]))
    print()
names = [name for tier_names in names for name in tier_names]
last_names = [name for tier_names in last_names for name in tier_names]
affils = [aff for tier_affils in affils for aff in tier_affils]
acks = [ack for tier_acks in acks for ack in tier_acks if ack != "%"]

# write author and affiliation lists
affiliation_list = []
# add general acknowledgement if it exists
ack_list = []

with open(args.output, "w") as afile:
    for i in range(len(names)):
        iaff = []
        for aff in affils[i]:
            aff = aff.replace("\\\\", "").strip().replace("  ", " ")
            # curate affiliations
            if aff in affiliation_list:
                iaff.append(affiliation_list.index(aff) + 1)
            elif "Casilla 4059" in aff:
                iaff.append(1)
            elif "Atacama" in aff:
                iaff.append(3)
            elif "Federico" in aff:
                iaff.append(4)
            else:
                iaff.append(len(affiliation_list) + 1)
            if iaff[-1] > len(affiliation_list):
                affiliation_list.append(aff)
        iaff = ",".join([str(i) for i in iaff])
        names[i] = f"{names[i]}\inst{{{iaff}}}"
    if args.journal == "aap":
        print("\\author{", file=afile)
        print("\n\\and ".join(names), file=afile)
        print("}\n", file=afile)
        # this is also A&A specifi
        print("\institute{", file=afile)
        print("\n\\and ".join(affiliation_list), file=afile)
        print("}", file=afile)
    for name in names:
        print(name[28 : name.index("\\inst") - 1].replace("~", " "), end=", ")
print()

# write acknowledgements
with open("acknowledgements.tex", "w") as ackfile:
    if general_acknowledgements:
        print(general_acknowledgements, file=ackfile)
    print("\n".join(acks), file=ackfile)
