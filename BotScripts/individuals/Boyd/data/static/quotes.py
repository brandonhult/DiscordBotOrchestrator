"""
Boyd / Milkman quote dataset for Boyd / Ultron.

POSITIONAL RATING SYSTEM
------------------------
1 = cannot be the last quote in the sentence
2 = cannot be the first quote in the sentence
3 = cannot be the first OR last quote in the sentence
4 = can fit anywhere

ADDITIONAL METADATA
-------------------
roles:
    - starter       : strong opener
    - bridge        : connective middle segment
    - fragment      : incomplete thought / dangling phrase
    - closer        : strong ending / punchline / accusation
    - interjection  : short interruption
    - reaction      : emotional outburst / standalone reaction
    - standalone    : works well by itself

topics:
    - milk
    - conspiracy
    - surveillance
    - neighborhood
    - government
    - industry
    - animals
    - clinic
    - media
    - paranoia
    - identity
    - violence
    - food
    - death
    - truth

flow:
    - entity        : introduces a suspicious person/group/object/system
    - connector     : links a subject to another subject or action
    - accusation    : explicit wrongdoing / hidden action / crime
    - reaction      : panic, confrontation, alarm, emotional outburst
    - interruption  : short derail, pause, aside, wobble
    - collapse      : unraveling, self-doubt, mental break, identity confusion
    - reveal        : dramatic truth-drop / proclamation
    - observation   : strange noticed detail / concrete sensory oddity

weight:
    Relative selection weight for future weighted random generation.
    Higher = appears more often.

NOTES
-----
- This file is designed to replace the old quotes.py.
- `rating` is preserved for backward compatibility.
- The 3 extra lines added here are from public transcript sources.
"""

quotes = {
    1: {
        "quote": "I'm the guard, I've been fully trained.",
        "rating": 4,
        "roles": ["starter", "standalone"],
        "topics": ["identity", "paranoia"],
        "flow": ["reaction", "reveal"],
        "weight": 3,
    },
    2: {
        "quote": "I'll bet he's sleeping on the job, his milk is delicious, everyone wants it.",
        "rating": 4,
        "roles": ["starter", "standalone"],
        "topics": ["milk", "paranoia"],
        "flow": ["observation", "accusation"],
        "weight": 3,
    },
    3: {
        "quote": "He'll be here soon, and the lies will end.",
        "rating": 4,
        "roles": ["closer", "standalone"],
        "topics": ["truth", "conspiracy"],
        "flow": ["reveal"],
        "weight": 2,
    },
    4: {
        "quote": "Gah! Not another tracking device!",
        "rating": 4,
        "roles": ["reaction", "starter", "standalone"],
        "topics": ["surveillance", "paranoia"],
        "flow": ["reaction", "observation"],
        "weight": 3,
    },
    5: {
        "quote": "You! You're one of them! Stay away!",
        "rating": 4,
        "roles": ["reaction", "starter", "standalone"],
        "topics": ["paranoia", "identity"],
        "flow": ["reaction", "accusation"],
        "weight": 3,
    },
    6: {
        "quote": "Had everyone fooled!",
        "rating": 3,
        "roles": ["bridge", "closer"],
        "topics": ["conspiracy", "truth"],
        "flow": ["accusation", "reveal"],
        "weight": 2,
    },
    7: {
        "quote": "Are telling my location to...",
        "rating": 3,
        "roles": ["bridge", "fragment"],
        "topics": ["surveillance", "paranoia"],
        "flow": ["connector"],
        "weight": 2,
    },
    8: {
        "quote": "Sorry, the Milkman has the key, I am not the Milkman, I'm the guard!",
        "rating": 4,
        "roles": ["starter", "standalone"],
        "topics": ["milk", "identity"],
        "flow": ["collapse", "reveal"],
        "weight": 3,
    },
    9: {
        "quote": "Huh?! Who are you working for?!",
        "rating": 2,
        "roles": ["closer", "reaction"],
        "topics": ["conspiracy", "paranoia", "identity"],
        "flow": ["reaction", "accusation"],
        "weight": 3,
    },
    10: {
        "quote": "The who? That doesn't fit in! That doesn't fit in at all! Maybe I've got this all wrong!",
        "rating": 2,
        "roles": ["closer", "reaction", "standalone"],
        "topics": ["identity", "paranoia"],
        "flow": ["collapse"],
        "weight": 2,
    },
    11: {
        "quote": "The kid with the goggles...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["surveillance", "identity"],
        "flow": ["entity"],
        "weight": 2,
    },
    12: {
        "quote": "The little fat kid with the bunny...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["identity", "paranoia"],
        "flow": ["entity"],
        "weight": 1,
    },
    13: {
        "quote": "Burned up in a department store fire, didn't you hear? At least, that's what the media would have you believe. Is he dead or not?",
        "rating": 2,
        "roles": ["closer", "standalone"],
        "topics": ["media", "death", "conspiracy"],
        "flow": ["accusation", "collapse"],
        "weight": 2,
    },
    14: {
        "quote": "Go out to the Graveyard! Dig him up! Oh, you'll find something there, but it's neither man nor milk.",
        "rating": 4,
        "roles": ["starter", "standalone"],
        "topics": ["death", "milk", "conspiracy"],
        "flow": ["reveal", "observation"],
        "weight": 2,
    },
    15: {
        "quote": "Be careful, they're watching, all the time!",
        "rating": 4,
        "roles": ["starter", "closer", "standalone"],
        "topics": ["surveillance", "paranoia"],
        "flow": ["reaction", "reveal"],
        "weight": 3,
    },
    16: {
        "quote": "It's perfect, isn't it?",
        "rating": 4,
        "roles": ["bridge", "closer"],
        "topics": ["paranoia", "truth"],
        "flow": ["observation", "collapse"],
        "weight": 1,
    },
    17: {
        "quote": "Almost complete, just a few missing pieces.",
        "rating": 4,
        "roles": ["bridge", "standalone"],
        "topics": ["conspiracy", "truth"],
        "flow": ["observation", "reveal"],
        "weight": 1,
    },
    18: {
        "quote": "But it's ALL about the Milkman!",
        "rating": 4,
        "roles": ["reaction", "closer", "standalone"],
        "topics": ["milk", "conspiracy"],
        "flow": ["reaction", "reveal"],
        "weight": 3,
    },
    19: {
        "quote": "Aah! I'm telling you! I don't know where the Milkman is!",
        "rating": 4,
        "roles": ["reaction", "standalone"],
        "topics": ["milk", "identity", "paranoia"],
        "flow": ["reaction", "collapse"],
        "weight": 2,
    },
    20: {
        "quote": "Aah! They've come for me! They're taking me away!",
        "rating": 4,
        "roles": ["reaction", "standalone"],
        "topics": ["paranoia", "surveillance"],
        "flow": ["reaction", "collapse"],
        "weight": 2,
    },
    21: {
        "quote": "Give a loaded gun to a ten year old? Do I look crazy to you?",
        "rating": 4,
        "roles": ["standalone", "reaction"],
        "topics": ["violence", "identity"],
        "flow": ["reaction", "collapse"],
        "weight": 2,
    },
    22: {
        "quote": "On the front...like most refrigerators.",
        "rating": 2,
        "roles": ["closer", "bridge"],
        "topics": ["food", "paranoia"],
        "flow": ["observation"],
        "weight": 1,
    },
    23: {
        "quote": "Made a deal, back in 68' with...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["government", "conspiracy"],
        "flow": ["connector"],
        "weight": 2,
    },
    24: {
        "quote": "I scream, you scream, we all scream, we all scream...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["food", "paranoia"],
        "flow": ["observation", "interruption"],
        "weight": 1,
    },
    25: {
        "quote": "You can pass it over the counter, but that don't make it over the counter!",
        "rating": 4,
        "roles": ["standalone", "reaction"],
        "topics": ["food", "conspiracy"],
        "flow": ["accusation", "observation"],
        "weight": 1,
    },
    26: {
        "quote": "You know my house is clean, right? Right, boss?!",
        "rating": 4,
        "roles": ["standalone", "reaction"],
        "topics": ["neighborhood", "paranoia"],
        "flow": ["reaction", "collapse"],
        "weight": 1,
    },
    27: {
        "quote": "They should paint their garage door the same color as everybody else's!",
        "rating": 2,
        "roles": ["closer", "standalone"],
        "topics": ["neighborhood", "paranoia"],
        "flow": ["accusation", "observation"],
        "weight": 1,
    },
    28: {
        "quote": "The housing committee is not going to like this!",
        "rating": 4,
        "roles": ["reaction", "closer", "standalone"],
        "topics": ["neighborhood", "paranoia"],
        "flow": ["reaction", "accusation"],
        "weight": 3,
    },
    29: {
        "quote": "All them haters!",
        "rating": 4,
        "roles": ["reaction", "interjection"],
        "topics": ["paranoia", "identity"],
        "flow": ["reaction", "interruption"],
        "weight": 2,
    },
    30: {
        "quote": "The doctors back at the clinic...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["clinic", "conspiracy"],
        "flow": ["entity"],
        "weight": 2,
    },
    31: {
        "quote": "Are telling my location to...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["surveillance", "paranoia"],
        "flow": ["connector"],
        "weight": 1,
    },
    32: {
        "quote": "Am I? Or is he? Am I he?! What is he doing in my house?!",
        "rating": 2,
        "roles": ["closer", "reaction", "standalone"],
        "topics": ["identity", "paranoia"],
        "flow": ["collapse"],
        "weight": 3,
    },
    33: {
        "quote": "Huh? Are you sure these are your children?",
        "rating": 4,
        "roles": ["standalone", "reaction"],
        "topics": ["identity", "paranoia"],
        "flow": ["reaction", "observation"],
        "weight": 1,
    },
    34: {
        "quote": "Ha Ha! L-Like I don't know that they...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["conspiracy", "paranoia"],
        "flow": ["connector", "reaction"],
        "weight": 1,
    },
    35: {
        "quote": "Why does that hydrant keep looking at me?!",
        "rating": 4,
        "roles": ["reaction", "standalone"],
        "topics": ["surveillance", "neighborhood", "paranoia"],
        "flow": ["observation", "reaction"],
        "weight": 2,
    },
    36: {
        "quote": "G-man! Who you working for?! Who is G?",
        "rating": 4,
        "roles": ["reaction", "starter", "standalone"],
        "topics": ["government", "identity", "paranoia"],
        "flow": ["reaction", "accusation"],
        "weight": 2,
    },
    37: {
        "quote": "And the little girl stuck her finger in the dike and saved all the windmills. But who does the little girl work for?",
        "rating": 2,
        "roles": ["closer", "standalone"],
        "topics": ["conspiracy", "government", "paranoia"],
        "flow": ["observation", "accusation"],
        "weight": 1,
    },
    38: {
        "quote": "Foreign toy makers...",
        "rating": 3,
        "roles": ["bridge", "fragment"],
        "topics": ["industry", "conspiracy"],
        "flow": ["entity"],
        "weight": 2,
    },
    39: {
        "quote": "The Cows!",
        "rating": 4,
        "roles": ["reaction", "interjection", "standalone"],
        "topics": ["animals", "milk", "paranoia"],
        "flow": ["reaction", "interruption"],
        "weight": 4,
    },
    40: {
        "quote": "In order to monopolize...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["industry", "conspiracy"],
        "flow": ["connector"],
        "weight": 1,
    },
    41: {
        "quote": "The band manager...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["conspiracy", "identity"],
        "flow": ["entity"],
        "weight": 3,
    },
    42: {
        "quote": "The Squirrels have EYES!",
        "rating": 4,
        "roles": ["reaction", "standalone"],
        "topics": ["animals", "surveillance", "paranoia"],
        "flow": ["reaction", "observation"],
        "weight": 3,
    },
    43: {
        "quote": "The intelligence community...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["government", "surveillance", "conspiracy"],
        "flow": ["entity"],
        "weight": 2,
    },
    44: {
        "quote": "The rodeo clown cartel...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["conspiracy", "industry"],
        "flow": ["entity"],
        "weight": 2,
    },
    45: {
        "quote": "The pelicans...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["animals", "conspiracy"],
        "flow": ["entity"],
        "weight": 1,
    },
    46: {
        "quote": "Oh, you think that's regular yarn, do you?!",
        "rating": 4,
        "roles": ["reaction", "standalone"],
        "topics": ["paranoia", "conspiracy"],
        "flow": ["reaction", "observation"],
        "weight": 1,
    },
    47: {
        "quote": "Y-You think you can get this past me?! I'm the guard!",
        "rating": 4,
        "roles": ["reaction", "standalone"],
        "topics": ["identity", "paranoia"],
        "flow": ["reaction", "reveal"],
        "weight": 2,
    },
    48: {
        "quote": "This is ugly, it's like a cyclops, with a million eyes!",
        "rating": 4,
        "roles": ["standalone", "reaction"],
        "topics": ["surveillance", "paranoia"],
        "flow": ["observation", "reaction"],
        "weight": 1,
    },
    49: {
        "quote": "Someone has to get this information to the people!",
        "rating": 4,
        "roles": ["closer", "standalone"],
        "topics": ["truth", "conspiracy"],
        "flow": ["reveal"],
        "weight": 3,
    },
    50: {
        "quote": "Those eggheads in their ivory tower...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["government", "conspiracy"],
        "flow": ["entity"],
        "weight": 2,
    },
    51: {
        "quote": "I thought you worked for me!",
        "rating": 4,
        "roles": ["reaction", "standalone"],
        "topics": ["identity", "paranoia"],
        "flow": ["reaction", "collapse"],
        "weight": 1,
    },
    52: {
        "quote": "Hey, don't worry about me. I'm centered. I'm the whole center in fact.",
        "rating": 4,
        "roles": ["standalone"],
        "topics": ["identity", "paranoia"],
        "flow": ["collapse", "reveal"],
        "weight": 1,
    },
    53: {
        "quote": "Who are merely the pawns of...",
        "rating": 3,
        "roles": ["bridge", "fragment"],
        "topics": ["conspiracy", "government"],
        "flow": ["connector"],
        "weight": 2,
    },
    54: {
        "quote": "The truth is sleeping in a glass box.",
        "rating": 4,
        "roles": ["standalone", "closer"],
        "topics": ["truth", "conspiracy"],
        "flow": ["reveal"],
        "weight": 2,
    },
    55: {
        "quote": "Did I just think that? Or did someone make me think it?",
        "rating": 2,
        "roles": ["closer", "standalone"],
        "topics": ["identity", "surveillance", "paranoia"],
        "flow": ["collapse"],
        "weight": 2,
    },
    56: {
        "quote": "And if they find out if I know this stuff, I'm dead!",
        "rating": 2,
        "roles": ["closer", "standalone"],
        "topics": ["death", "conspiracy", "paranoia"],
        "flow": ["accusation", "reveal"],
        "weight": 2,
    },
    57: {
        "quote": "They think the windows are tinted, but they aren't tinted NEARLY enough!",
        "rating": 4,
        "roles": ["standalone", "reaction"],
        "topics": ["surveillance", "paranoia"],
        "flow": ["observation", "accusation"],
        "weight": 2,
    },
    58: {
        "quote": "The tuna canneries have been living off the teat of the dairy industry.",
        "rating": 4,
        "roles": ["standalone", "closer"],
        "topics": ["industry", "milk", "conspiracy"],
        "flow": ["accusation", "reveal"],
        "weight": 2,
    },
    59: {
        "quote": "Wait.",
        "rating": 4,
        "roles": ["interjection"],
        "topics": ["paranoia"],
        "flow": ["interruption"],
        "weight": 4,
    },
    60: {
        "quote": "Who are the puppet masters of...",
        "rating": 3,
        "roles": ["bridge", "fragment"],
        "topics": ["conspiracy", "government"],
        "flow": ["connector"],
        "weight": 2,
    },
    61: {
        "quote": "The fire will start in men's wear!",
        "rating": 4,
        "roles": ["standalone", "closer"],
        "topics": ["death", "conspiracy", "paranoia"],
        "flow": ["reveal", "accusation"],
        "weight": 1,
    },
    62: {
        "quote": "Ate a whole jar of olives, with uh...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["food", "paranoia"],
        "flow": ["observation", "connector"],
        "weight": 1,
    },
    63: {
        "quote": "And sure as the nose on my face, I am sure they...",
        "rating": 3,
        "roles": ["bridge", "fragment"],
        "topics": ["conspiracy", "paranoia"],
        "flow": ["connector"],
        "weight": 1,
    },
    64: {
        "quote": "How long do they think they can hide that?!",
        "rating": 2,
        "roles": ["closer", "reaction"],
        "topics": ["truth", "conspiracy", "paranoia"],
        "flow": ["accusation", "reaction"],
        "weight": 4,
    },
    65: {
        "quote": "The Psycho...whats-its...?",
        "rating": 4,
        "roles": ["reaction", "standalone"],
        "topics": ["identity", "paranoia"],
        "flow": ["interruption", "collapse"],
        "weight": 1,
    },
    66: {
        "quote": "Hey! Lady! Where you going with that sweater?",
        "rating": 4,
        "roles": ["reaction", "standalone"],
        "topics": ["neighborhood", "paranoia"],
        "flow": ["reaction", "observation"],
        "weight": 1,
    },
    67: {
        "quote": "These are not my dot-to-dots. These are not my babies.",
        "rating": 2,
        "roles": ["closer", "standalone"],
        "topics": ["identity", "paranoia"],
        "flow": ["collapse"],
        "weight": 1,
    },
    68: {
        "quote": "Keep sparring with me.",
        "rating": 4,
        "roles": ["interjection", "standalone"],
        "topics": ["paranoia"],
        "flow": ["interruption"],
        "weight": 1,
    },
    69: {
        "quote": "Something's got to give!",
        "rating": 4,
        "roles": ["closer", "reaction", "standalone"],
        "topics": ["paranoia", "truth"],
        "flow": ["reaction", "collapse"],
        "weight": 2,
    },
    70: {
        "quote": "Oh man, this stuff is hot.",
        "rating": 4,
        "roles": ["standalone"],
        "topics": ["food"],
        "flow": ["observation"],
        "weight": 1,
    },
    71: {
        "quote": "All in a big fight over...",
        "rating": 3,
        "roles": ["bridge", "fragment"],
        "topics": ["conspiracy", "industry"],
        "flow": ["connector"],
        "weight": 1,
    },
    72: {
        "quote": "Some sort of power, you know...",
        "rating": 3,
        "roles": ["bridge", "fragment"],
        "topics": ["government", "conspiracy"],
        "flow": ["connector"],
        "weight": 1,
    },
    73: {
        "quote": "Last specimen of the super virus!",
        "rating": 2,
        "roles": ["closer", "standalone"],
        "topics": ["clinic", "government", "conspiracy"],
        "flow": ["reveal", "accusation"],
        "weight": 1,
    },
    74: {
        "quote": "Someone moved into my neighborhood, uninvited!",
        "rating": 4,
        "roles": ["reaction", "standalone"],
        "topics": ["neighborhood", "paranoia"],
        "flow": ["reaction", "accusation"],
        "weight": 2,
    },
    75: {
        "quote": "Have been fixing oil prices!",
        "rating": 2,
        "roles": ["closer"],
        "topics": ["industry", "government", "conspiracy"],
        "flow": ["accusation"],
        "weight": 2,
    },
    76: {
        "quote": "Of course! The milk's got spiderwebs in it! Taste it!",
        "rating": 4,
        "roles": ["reaction", "standalone"],
        "topics": ["milk", "paranoia"],
        "flow": ["observation", "reaction"],
        "weight": 2,
    },
    77: {
        "quote": "The ice cream's in the web, the web is in the cream.",
        "rating": 4,
        "roles": ["standalone"],
        "topics": ["food", "milk", "paranoia"],
        "flow": ["observation", "reveal"],
        "weight": 1,
    },
    78: {
        "quote": "And he waits, and he waits...",
        "rating": 3,
        "roles": ["bridge", "fragment"],
        "topics": ["conspiracy", "paranoia"],
        "flow": ["connector", "observation"],
        "weight": 1,
    },
    79: {
        "quote": "Are you buying, or are you spying?",
        "rating": 4,
        "roles": ["standalone", "reaction"],
        "topics": ["surveillance", "paranoia"],
        "flow": ["reaction", "accusation"],
        "weight": 1,
    },
    80: {
        "quote": "Have been spitting on me all day!",
        "rating": 2,
        "roles": ["closer", "reaction"],
        "topics": ["paranoia", "identity"],
        "flow": ["accusation", "reaction"],
        "weight": 1,
    },
    81: {
        "quote": "I mean, who do they think they're fooling?!",
        "rating": 4,
        "roles": ["reaction", "closer", "standalone"],
        "topics": ["truth", "conspiracy", "paranoia"],
        "flow": ["reaction", "accusation"],
        "weight": 3,
    },
    82: {
        "quote": "Signed a secret treaty with...",
        "rating": 3,
        "roles": ["bridge", "fragment"],
        "topics": ["government", "conspiracy"],
        "flow": ["connector"],
        "weight": 2,
    },
    83: {
        "quote": "I see myself more as a turtle, with a rocket strapped to its back!",
        "rating": 4,
        "roles": ["standalone"],
        "topics": ["identity", "paranoia"],
        "flow": ["collapse", "reveal"],
        "weight": 1,
    },
    84: {
        "quote": "The freaky hunchback girl who loves brains so much...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["clinic", "identity", "paranoia"],
        "flow": ["entity"],
        "weight": 1,
    },
    85: {
        "quote": "Can I really be the only person who sees this?!",
        "rating": 4,
        "roles": ["reaction", "closer", "standalone"],
        "topics": ["truth", "paranoia"],
        "flow": ["reaction", "collapse"],
        "weight": 3,
    },
    86: {
        "quote": "The military industrial complex...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["government", "industry", "conspiracy"],
        "flow": ["entity"],
        "weight": 2,
    },
    87: {
        "quote": "The national park system!",
        "rating": 1,
        "roles": ["starter", "reaction", "fragment"],
        "topics": ["government", "conspiracy"],
        "flow": ["entity", "reaction"],
        "weight": 1,
    },
    88: {
        "quote": "All those stupid Crows!",
        "rating": 4,
        "roles": ["reaction", "standalone"],
        "topics": ["animals", "paranoia"],
        "flow": ["reaction"],
        "weight": 2,
    },
    89: {
        "quote": "But they can't hide that they...",
        "rating": 3,
        "roles": ["bridge", "fragment"],
        "topics": ["truth", "conspiracy"],
        "flow": ["connector"],
        "weight": 2,
    },
    90: {
        "quote": "If I know anything, I know that they...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["truth", "conspiracy"],
        "flow": ["connector", "reveal"],
        "weight": 2,
    },
    91: {
        "quote": "The five richest families in the country...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["government", "conspiracy", "industry"],
        "flow": ["entity"],
        "weight": 2,
    },
    92: {
        "quote": "Got in bed with...",
        "rating": 3,
        "roles": ["bridge", "fragment"],
        "topics": ["conspiracy", "industry"],
        "flow": ["connector"],
        "weight": 2,
    },
    93: {
        "quote": "Hey, where's the boss?",
        "rating": 4,
        "roles": ["interjection", "standalone"],
        "topics": ["identity", "paranoia"],
        "flow": ["interruption"],
        "weight": 1,
    },
    94: {
        "quote": "Stole my theories and reprinted them incorrectly, to discredit them.",
        "rating": 2,
        "roles": ["closer", "standalone"],
        "topics": ["truth", "conspiracy", "media"],
        "flow": ["accusation"],
        "weight": 2,
    },
    95: {
        "quote": "My first cat... Seymour.",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["animals", "identity"],
        "flow": ["entity", "interruption"],
        "weight": 1,
    },
    96: {
        "quote": "My hooch!",
        "rating": 4,
        "roles": ["reaction", "interjection"],
        "topics": ["paranoia", "identity"],
        "flow": ["reaction", "interruption"],
        "weight": 1,
    },
    97: {
        "quote": "The housing committee is not going to like this.",
        "rating": 4,
        "roles": ["closer", "standalone"],
        "topics": ["neighborhood", "paranoia"],
        "flow": ["accusation", "observation"],
        "weight": 2,
    },
    98: {
        "quote": "Or else, maybe...",
        "rating": 3,
        "roles": ["bridge", "fragment", "interjection"],
        "topics": ["paranoia", "conspiracy"],
        "flow": ["interruption", "connector"],
        "weight": 2,
    },
    99: {
        "quote": "In conjunction with...",
        "rating": 3,
        "roles": ["bridge", "fragment"],
        "topics": ["conspiracy", "government"],
        "flow": ["connector"],
        "weight": 2,
    },
    100: {
        "quote": "The analyticals, man...",
        "rating": 1,
        "roles": ["starter", "fragment"],
        "topics": ["government", "conspiracy"],
        "flow": ["entity"],
        "weight": 1,
    },
    101: {
        "quote": "Has been officially linked with...",
        "rating": 2,
        "roles": ["bridge", "closer"],
        "topics": ["conspiracy", "government"],
        "flow": ["connector"],
        "weight": 2,
    },
    102: {
        "quote": "And then it comes out of those wires over there, and goes straight into my head, with all its little audio tricks!",
        "rating": 2,
        "roles": ["closer", "standalone"],
        "topics": ["surveillance", "paranoia"],
        "flow": ["observation", "accusation"],
        "weight": 1,
    },
    103: {
        "quote": "And nobody, seems to care!",
        "rating": 2,
        "roles": ["closer", "reaction"],
        "topics": ["truth", "paranoia"],
        "flow": ["reaction", "collapse"],
        "weight": 1,
    },
    104: {
        "quote": "You think I'm crazy? What if I'm the only one who's sane?",
        "rating": 4,
        "roles": ["standalone", "closer"],
        "topics": ["identity", "paranoia", "truth"],
        "flow": ["collapse", "reveal"],
        "weight": 3,
    },
    105: {
        "quote": "You have to keep your guard up at all times. You gotta be like a turtle with a rocket strapped on his back, you know?",
        "rating": 4,
        "roles": ["standalone"],
        "topics": ["identity", "paranoia"],
        "flow": ["reveal", "observation"],
        "weight": 2,
    },
    106: {
        "quote": "No. I don't trust pies.",
        "rating": 4,
        "roles": ["standalone", "reaction"],
        "topics": ["food", "paranoia"],
        "flow": ["reaction", "observation"],
        "weight": 2,
    },
    107: {
        "quote": "Shh! It may be bugged!.",
        "rating": 4,
        "roles": ["interjection", "reaction"],
        "topics": ["surveillance", "paranoia"],
        "flow": ["interruption", "reaction"],
        "weight": 3,
    },
    108: {
        "quote": "Flowers to put on the grave of the truth, for those who mourn the loss of democracy!",
        "rating": 2,
        "roles": ["closer", "standalone"],
        "topics": ["truth", "government", "death"],
        "flow": ["reveal"],
        "weight": 2,
    },
    109: {
        "quote": "Gah! That's the exact model plunger they used to kill the ambassador back with in '63!",
        "rating": 4,
        "roles": ["reaction", "starter", "standalone"],
        "topics": ["government", "violence", "conspiracy"],
        "flow": ["reaction", "accusation", "observation"],
        "weight": 3,
    },
    110: {
        "quote": "Give a loaded gun to a 10 year old? Do I look crazy to you?",
        "rating": 4,
        "roles": ["standalone", "reaction"],
        "topics": ["violence", "identity"],
        "flow": ["reaction", "collapse"],
        "weight": 2,
    },
    111: {
        "quote": "Ahh! Get that away from me! I never talk on the phone. That's how they get your location!",
        "rating": 4,
        "roles": ["reaction", "standalone"],
        "topics": ["surveillance", "paranoia"],
        "flow": ["reaction", "accusation"],
        "weight": 3,
    },
    112: {
        "quote": "Big deal. I knew where he was the whole time. Getting past the red head, that's the problem.",
        "rating": 4,
        "roles": ["standalone"],
        "topics": ["identity", "paranoia"],
        "flow": ["reveal", "observation"],
        "weight": 1,
    },
    113: {
        "quote": "There's something in the fridge that might help you see the world like I do.",
        "rating": 4,
        "roles": ["starter", "standalone"],
        "topics": ["food", "milk", "paranoia"],
        "flow": ["reveal", "observation"],
        "weight": 3,
    },
    114: {
        "quote": "Beware the cows! Not all milk is enriched!",
        "rating": 4,
        "roles": ["reaction", "starter", "standalone"],
        "topics": ["animals", "milk", "paranoia"],
        "flow": ["reaction", "accusation"],
        "weight": 4,
    },
    115: {
        "quote": "Hi mom, look at me! I'm tangled in a web of deception!",
        "rating": 4,
        "roles": ["standalone", "reaction", "closer"],
        "topics": ["identity", "conspiracy", "paranoia"],
        "flow": ["reaction", "reveal", "collapse"],
        "weight": 3,
    },
}

total_quotes = len(quotes)

# Optional helper pools for newer generators
interjections = [
    q["quote"]
    for q in quotes.values()
    if "interjection" in q["roles"]
]

starters = [
    q["quote"]
    for q in quotes.values()
    if "starter" in q["roles"]
]

bridges = [
    q["quote"]
    for q in quotes.values()
    if "bridge" in q["roles"] or "fragment" in q["roles"]
]

closers = [
    q["quote"]
    for q in quotes.values()
    if "closer" in q["roles"]
]

reactions = [
    q["quote"]
    for q in quotes.values()
    if "reaction" in q["roles"]
]

entities = [
    q["quote"]
    for q in quotes.values()
    if "entity" in q["flow"]
]

connectors = [
    q["quote"]
    for q in quotes.values()
    if "connector" in q["flow"]
]

accusations = [
    q["quote"]
    for q in quotes.values()
    if "accusation" in q["flow"]
]

interruptions = [
    q["quote"]
    for q in quotes.values()
    if "interruption" in q["flow"]
]

collapses = [
    q["quote"]
    for q in quotes.values()
    if "collapse" in q["flow"]
]

reveals = [
    q["quote"]
    for q in quotes.values()
    if "reveal" in q["flow"]
]

observations = [
    q["quote"]
    for q in quotes.values()
    if "observation" in q["flow"]
]