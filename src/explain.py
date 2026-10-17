"""Fixed, reviewed messages. Every fact comes from the diff, nothing else.
Have a native speaker review the Kannada and Hindi, and listen to the audio, before the demo."""

FRAME = {
    "en": "Alert for {label}: the public land record changed. {details} This does not prove anything is wrong. Please check with your local land records office.",
    "kn": "{label} ಜಮೀನಿನ ಸಾರ್ವಜನಿಕ ಭೂ ದಾಖಲೆಯಲ್ಲಿ ಬದಲಾವಣೆ ಕಂಡುಬಂದಿದೆ. {details} ಇದರಿಂದ ಏನೋ ತಪ್ಪಾಗಿದೆ ಎಂದು ಅರ್ಥವಲ್ಲ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಸ್ಥಳೀಯ ಭೂ ದಾಖಲೆ ಕಚೇರಿಯಲ್ಲಿ ವಿಚಾರಿಸಿ.",
    "hi": "{label} की जमीन के सार्वजनिक भूमि रिकॉर्ड में बदलाव मिला है। {details} इसका मतलब यह नहीं कि कुछ गलत है। कृपया अपने स्थानीय भूमि रिकॉर्ड कार्यालय में जांच करें।",
}

PART = {
    "new_mutation": {
        "en": "A new mutation entry was added, number {id}, dated {date}, status {status}.",
        "kn": "ಹೊಸ ಮ್ಯುಟೇಶನ್ ನಮೂದು ಸೇರಿದೆ, ಸಂಖ್ಯೆ {id}, ದಿನಾಂಕ {date}, ಸ್ಥಿತಿ {status}.",
        "hi": "नई म्यूटेशन एंट्री जुड़ी है, संख्या {id}, तारीख {date}, स्थिति {status}।",
    },
    "mutation_status_changed": {
        "en": "Mutation entry {id} changed from {old} to {new}.",
        "kn": "ಮ್ಯುಟೇಶನ್ ನಮೂದು {id} {old} ಇಂದ {new} ಗೆ ಬದಲಾಗಿದೆ.",
        "hi": "म्यूटेशन एंट्री {id} {old} से {new} में बदली है।",
    },
    "extent_changed": {
        "en": "The land extent changed from {old} to {new}.",
        "kn": "ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣ {old} ಇಂದ {new} ಗೆ ಬದಲಾಗಿದೆ.",
        "hi": "जमीन का क्षेत्रफल {old} से {new} हो गया है।",
    },
    "owner_changed": {
        "en": "The owner details on the record changed.",
        "kn": "ದಾಖಲೆಯಲ್ಲಿರುವ ಮಾಲೀಕರ ವಿವರಗಳು ಬದಲಾಗಿವೆ.",
        "hi": "रिकॉर्ड में मालिक का विवरण बदला है।",
    },
}

OPS = {
    "en": "The check for {label} could not run today, so I cannot say whether anything changed.",
    "kn": "{label} ಜಮೀನಿನ ಪರಿಶೀಲನೆ ಇಂದು ನಡೆಯಲಿಲ್ಲ, ಆದ್ದರಿಂದ ಏನಾದರೂ ಬದಲಾಗಿದೆಯೇ ಎಂದು ಹೇಳಲಾಗದು.",
    "hi": "{label} की जांच आज नहीं हो सकी, इसलिए मैं नहीं कह सकता कि कुछ बदला या नहीं।",
}


def build_message(label, changes, lang="kn"):
    parts = " ".join(PART[c["type"]][lang].format(**c) for c in changes)
    return FRAME[lang].format(label=label, details=parts)


def ops_message(label, lang="kn"):
    return OPS[lang].format(label=label)


def grounded(message, changes):
    """Every id, date and extent value in the message must come from the diff."""
    for c in changes:
        for key in ("id", "date", "old", "new"):
            if key in c and str(c[key]) not in message:
                return False
    return True
