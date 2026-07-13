 # Parse user prompt into structured data
import re

CATEGORY_KEYWORDS = {

    "Food": [
        "bread","milk","rice","beans","sugar","meat",
        "tea","coffee","egg","eggs","ugali","flour",
        "maize","vegetables","fruit","banana","apple",
        "juice","water","soda","snacks","lunch","breakfast", "yoghurt"
    ],

    "Transport":[
        "fare","bus","matatu","uber","bolt",
        "fuel","taxi","parking","train","flight", "trip"
    ],

    "Entertainment":[
        "movie","cinema","netflix","game",
        "show","concert","spotify"
    ],

    "Internet":[
        "wifi","internet","airtime","bundle","bundles","data"
    ],

    "Utilities":[
        "water bill","electricity","tokens","electricity bill","gas", "rent"
    ],

    "Health":[
        "hospital","medicine","chemist","clinic","doctor"
    ],

    "Shopping":[
        "clothes","shoe","shoes","bag","shirt","dress"
    ],

    "Education":[
        "book","books","school","tuition","course"
    ],

    "Professional Development":[
        "udemy","coursera","certification","conference"
    ],

    "Savings":[
        "saving","savings","deposit","investment"
    ],
    "Toiletries":[
        "soap","shampoo","toothpaste","toothbrush","deodorant", "roll-on", "tissue", "tissues"
    ]   

}


# detect category by scoring instead of stopping at the first match, 
# to allow for more accurate categorization
def detect_category(description):

    description = description.lower()

    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():

        score = sum(
            1 for keyword in keywords
            if keyword in description
        )

        if score:
            scores[category] = score

    if not scores:
        return "Other"

    return max(scores, key=scores.get)


# parse single expense
def parse_single_expense(text):

    amount_match = re.findall(r"\d+(?:\.\d+)?", text)

    amount = float(amount_match[-1]) if amount_match else None

    description = re.sub(
        r"\d+(?:\.\d+)?",
        "",
        text
    ).strip(" ,-")

    category = detect_category(description)

    if category is None:
        raise ValueError(
            f"Could not determine category for '{description}'."
        )


    return {

        "description": description,

        "amount": amount,

        "category": category
    }


# parse multiple expenses from a single prompt
def parse_expense(prompt):

    prompt = prompt.replace("\n", ",")

    entries = [
        entry.strip()
        for entry in prompt.split(",")
        if entry.strip()
    ]

    expenses = []

    for entry in entries:

        expense = parse_single_expense(entry)

        if expense["amount"] is not None:
            expenses.append(expense)

    return expenses