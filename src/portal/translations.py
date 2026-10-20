"""Kannada and Hindi text for the registry website. One place, so a native speaker can fix wording here.

How it works: after a page is built, every piece of visible text that exactly matches an English key
below is replaced. Anything not listed stays English, so a missing line never breaks a page.
The public watch page the agent reads is never translated.

TEXT:      exact English text -> {"kn": ..., "hi": ...}
PATTERNS:  English text with changing parts (names, numbers) -> templates; {1}, {2} are the changing parts
STATUS: all lines below are a first draft that needs a native-speaker review.
"""

TEXT = {
    # ---- header, footer, banner
    "DEMO REGISTRY · Fictional data only · Not an official record · Do not enter real personal or land details": {
        "kn": "ಡೆಮೊ ನೋಂದಣಿ · ಕಾಲ್ಪನಿಕ ಮಾಹಿತಿ ಮಾತ್ರ · ಅಧಿಕೃತ ದಾಖಲೆ ಅಲ್ಲ · ನಿಜವಾದ ವೈಯಕ್ತಿಕ ಅಥವಾ ಜಮೀನಿನ ವಿವರಗಳನ್ನು ನಮೂದಿಸಬೇಡಿ",
        "hi": "डेमो रजिस्ट्री · केवल काल्पनिक डेटा · आधिकारिक रिकॉर्ड नहीं · असली व्यक्तिगत या ज़मीन का विवरण दर्ज न करें"},
    "Demo Registry": {"kn": "ಡೆಮೊ ನೋಂದಣಿ", "hi": "डेमो रजिस्ट्री"},
    "Demo Land Registry": {"kn": "ಡೆಮೊ ಭೂ ನೋಂದಣಿ", "hi": "डेमो भूमि रजिस्ट्री"},
    "Land Record Watch demo registry for a hackathon project. Records here are made up and are not legal documents.": {
        "kn": "ಇದು ಹ್ಯಾಕಥಾನ್ ಯೋಜನೆಗಾಗಿ ಮಾಡಿದ ಲ್ಯಾಂಡ್ ರೆಕಾರ್ಡ್ ವಾಚ್ ಡೆಮೊ ನೋಂದಣಿ. ಇಲ್ಲಿನ ದಾಖಲೆಗಳು ಕಾಲ್ಪನಿಕ, ಕಾನೂನು ದಾಖಲೆಗಳಲ್ಲ.",
        "hi": "यह एक हैकथॉन प्रोजेक्ट के लिए बनी लैंड रिकॉर्ड वॉच की डेमो रजिस्ट्री है। यहाँ के रिकॉर्ड काल्पनिक हैं और क़ानूनी दस्तावेज़ नहीं हैं।"},
    "Log in": {"kn": "ಲಾಗಿನ್ ಮಾಡಿ", "hi": "लॉग इन करें"},
    "Log out": {"kn": "ಲಾಗ್ ಔಟ್", "hi": "लॉग आउट"},
    "Create account": {"kn": "ಖಾತೆ ರಚಿಸಿ", "hi": "खाता बनाएँ"},
    "My lands": {"kn": "ನನ್ನ ಜಮೀನುಗಳು", "hi": "मेरी ज़मीनें"},
    "Add land": {"kn": "ಜಮೀನು ಸೇರಿಸಿ", "hi": "ज़मीन जोड़ें"},
    "Search": {"kn": "ಹುಡುಕಿ", "hi": "खोजें"},
    "Pending queue": {"kn": "ಬಾಕಿ ಇರುವ ಪಟ್ಟಿ", "hi": "लंबित सूची"},
    "Landlord": {"kn": "ಭೂಮಾಲೀಕ", "hi": "भूमि मालिक"},
    "Buyer": {"kn": "ಖರೀದಿದಾರ", "hi": "खरीदार"},
    "Registrar": {"kn": "ನೋಂದಣಾಧಿಕಾರಿ", "hi": "रजिस्ट्रार"},
    "landlord": {"kn": "ಭೂಮಾಲೀಕ", "hi": "भूमि मालिक"},
    "buyer": {"kn": "ಖರೀದಿದಾರ", "hi": "खरीदार"},
    "registrar": {"kn": "ನೋಂದಣಾಧಿಕಾರಿ", "hi": "रजिस्ट्रार"},

    # ---- home
    "Who are you?": {"kn": "ನೀವು ಯಾರು?", "hi": "आप कौन हैं?"},
    "Choose how you want to use the demo registry. A landlord registers land and files changes. A buyer searches and sees the status of a record.": {
        "kn": "ಡೆಮೊ ನೋಂದಣಿಯನ್ನು ಹೇಗೆ ಬಳಸಬೇಕೆಂದು ಆಯ್ಕೆ ಮಾಡಿ. ಭೂಮಾಲೀಕರು ಜಮೀನನ್ನು ನೋಂದಾಯಿಸಿ ಬದಲಾವಣೆಗಳನ್ನು ಸಲ್ಲಿಸುತ್ತಾರೆ. ಖರೀದಿದಾರರು ದಾಖಲೆಯನ್ನು ಹುಡುಕಿ ಅದರ ಸ್ಥಿತಿಯನ್ನು ನೋಡುತ್ತಾರೆ.",
        "hi": "चुनें कि आप डेमो रजिस्ट्री का उपयोग कैसे करना चाहते हैं। भूमि मालिक ज़मीन पंजीकृत करता है और बदलाव दर्ज करता है। खरीदार रिकॉर्ड खोजकर उसकी स्थिति देखता है।"},
    "I am a landlord": {"kn": "ನಾನು ಭೂಮಾಲೀಕ", "hi": "मैं भूमि मालिक हूँ"},
    "Register your land with its survey details, file a mutation request, and get a private watch link for Land Record Watch alerts.": {
        "kn": "ನಿಮ್ಮ ಜಮೀನನ್ನು ಸರ್ವೆ ವಿವರಗಳೊಂದಿಗೆ ನೋಂದಾಯಿಸಿ, ಮ್ಯುಟೇಶನ್ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ ಮತ್ತು ಲ್ಯಾಂಡ್ ರೆಕಾರ್ಡ್ ವಾಚ್ ಎಚ್ಚರಿಕೆಗಳಿಗಾಗಿ ಖಾಸಗಿ ವಾಚ್ ಲಿಂಕ್ ಪಡೆಯಿರಿ.",
        "hi": "अपनी ज़मीन को सर्वे विवरण के साथ पंजीकृत करें, म्यूटेशन अनुरोध दर्ज करें और लैंड रिकॉर्ड वॉच अलर्ट के लिए निजी वॉच लिंक पाएँ।"},
    "Create landlord account": {"kn": "ಭೂಮಾಲೀಕರ ಖಾತೆ ರಚಿಸಿ", "hi": "भूमि मालिक का खाता बनाएँ"},
    "I am a buyer": {"kn": "ನಾನು ಖರೀದಿದಾರ", "hi": "मैं खरीदार हूँ"},
    "Search by district, taluk, village and survey number to see the extent, the status of mutations and the history of a record.": {
        "kn": "ಜಿಲ್ಲೆ, ತಾಲೂಕು, ಗ್ರಾಮ ಮತ್ತು ಸರ್ವೆ ನಂಬರ್ ಮೂಲಕ ಹುಡುಕಿ, ದಾಖಲೆಯ ವಿಸ್ತೀರ್ಣ, ಮ್ಯುಟೇಶನ್ ಸ್ಥಿತಿ ಮತ್ತು ಇತಿಹಾಸವನ್ನು ನೋಡಿ.",
        "hi": "जिला, तालुक, गाँव और सर्वे नंबर से खोजें और रिकॉर्ड का क्षेत्रफल, म्यूटेशन की स्थिति और इतिहास देखें।"},
    "Create buyer account": {"kn": "ಖರೀದಿದಾರರ ಖಾತೆ ರಚಿಸಿ", "hi": "खरीदार का खाता बनाएँ"},
    "First time? Create the registrar account": {"kn": "ಮೊದಲ ಬಾರಿಯೇ? ನೋಂದಣಾಧಿಕಾರಿ ಖಾತೆ ರಚಿಸಿ", "hi": "पहली बार? रजिस्ट्रार खाता बनाएँ"},
    "Registrar (demo staff who approve changes)?": {"kn": "ನೋಂದಣಾಧಿಕಾರಿ (ಬದಲಾವಣೆಗಳನ್ನು ಅನುಮೋದಿಸುವ ಡೆಮೊ ಸಿಬ್ಬಂದಿ)?", "hi": "रजिस्ट्रार (बदलाव मंज़ूर करने वाला डेमो स्टाफ़)?"},
    "Log in here": {"kn": "ಇಲ್ಲಿ ಲಾಗಿನ್ ಮಾಡಿ", "hi": "यहाँ लॉग इन करें"},

    # ---- login, register, setup
    "Email": {"kn": "ಇಮೇಲ್", "hi": "ईमेल"},
    "Password": {"kn": "ಪಾಸ್‌ವರ್ಡ್", "hi": "पासवर्ड"},
    "New here?": {"kn": "ಹೊಸಬರೇ?", "hi": "नए हैं?"},
    "Create an account": {"kn": "ಖಾತೆ ರಚಿಸಿ", "hi": "खाता बनाएँ"},
    "This is a demo. Use made-up names and details. Your password is stored hashed and is never shown.": {
        "kn": "ಇದು ಡೆಮೊ. ಕಾಲ್ಪನಿಕ ಹೆಸರು ಮತ್ತು ವಿವರಗಳನ್ನು ಬಳಸಿ. ನಿಮ್ಮ ಪಾಸ್‌ವರ್ಡ್ ಎನ್‌ಕ್ರಿಪ್ಟ್ ಆಗಿ ಸಂಗ್ರಹವಾಗುತ್ತದೆ ಮತ್ತು ಎಂದಿಗೂ ತೋರಿಸಲಾಗುವುದಿಲ್ಲ.",
        "hi": "यह एक डेमो है। काल्पनिक नाम और विवरण इस्तेमाल करें। आपका पासवर्ड हैश करके रखा जाता है और कभी दिखाया नहीं जाता।"},
    "Full name": {"kn": "ಪೂರ್ಣ ಹೆಸರು", "hi": "पूरा नाम"},
    "At least 10 characters, with letters and numbers.": {"kn": "ಕನಿಷ್ಠ 10 ಅಕ್ಷರಗಳು, ಅಕ್ಷರ ಮತ್ತು ಅಂಕೆಗಳೊಂದಿಗೆ.", "hi": "कम से कम 10 अक्षर, अक्षरों और अंकों के साथ।"},
    "Repeat password": {"kn": "ಪಾಸ್‌ವರ್ಡ್ ಮತ್ತೆ ನಮೂದಿಸಿ", "hi": "पासवर्ड दोबारा लिखें"},
    "Already registered?": {"kn": "ಈಗಾಗಲೇ ನೋಂದಾಯಿಸಿದ್ದೀರಾ?", "hi": "पहले से पंजीकृत हैं?"},
    "First-time setup": {"kn": "ಮೊದಲ ಬಾರಿಯ ಸೆಟಪ್", "hi": "पहली बार की सेटिंग"},
    "Create the registrar account": {"kn": "ನೋಂದಣಾಧಿಕಾರಿ ಖಾತೆ ರಚಿಸಿ", "hi": "रजिस्ट्रार खाता बनाएँ"},
    "One-time setup. The registrar is demo staff who approve or reject land changes. This page disappears once the account exists.": {
        "kn": "ಒಂದು ಬಾರಿಯ ಸೆಟಪ್. ನೋಂದಣಾಧಿಕಾರಿ ಜಮೀನಿನ ಬದಲಾವಣೆಗಳನ್ನು ಅನುಮೋದಿಸುವ ಅಥವಾ ತಿರಸ್ಕರಿಸುವ ಡೆಮೊ ಸಿಬ್ಬಂದಿ. ಖಾತೆ ರಚನೆಯಾದ ನಂತರ ಈ ಪುಟ ಮರೆಯಾಗುತ್ತದೆ.",
        "hi": "एक बार की सेटिंग। रजिस्ट्रार डेमो स्टाफ़ है जो ज़मीन के बदलाव मंज़ूर या अस्वीकार करता है। खाता बनने के बाद यह पेज गायब हो जाता है।"},
    "Setup code": {"kn": "ಸೆಟಪ್ ಕೋಡ್", "hi": "सेटअप कोड"},
    "Name": {"kn": "ಹೆಸರು", "hi": "नाम"},
    "Create registrar": {"kn": "ನೋಂದಣಾಧಿಕಾರಿ ರಚಿಸಿ", "hi": "रजिस्ट्रार बनाएँ"},

    # ---- landlord pages
    "Register land": {"kn": "ಜಮೀನು ನೋಂದಾಯಿಸಿ", "hi": "ज़मीन पंजीकृत करें"},
    "Mutation pending": {"kn": "ಮ್ಯುಟೇಶನ್ ಬಾಕಿ ಇದೆ", "hi": "म्यूटेशन लंबित है"},
    "No pending changes": {"kn": "ಬಾಕಿ ಬದಲಾವಣೆಗಳಿಲ್ಲ", "hi": "कोई लंबित बदलाव नहीं"},
    "You have not registered any land yet. Register a parcel to start.": {
        "kn": "ನೀವು ಇನ್ನೂ ಯಾವುದೇ ಜಮೀನನ್ನು ನೋಂದಾಯಿಸಿಲ್ಲ. ಪ್ರಾರಂಭಿಸಲು ಒಂದು ಜಮೀನನ್ನು ನೋಂದಾಯಿಸಿ.",
        "hi": "आपने अभी तक कोई ज़मीन पंजीकृत नहीं की है। शुरू करने के लिए एक भूखंड पंजीकृत करें।"},
    "Public identifiers only. No documents are uploaded. Use made-up details in this demo.": {
        "kn": "ಸಾರ್ವಜನಿಕ ಗುರುತಿನ ವಿವರಗಳು ಮಾತ್ರ. ಯಾವುದೇ ದಾಖಲೆಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡುವುದಿಲ್ಲ. ಈ ಡೆಮೊದಲ್ಲಿ ಕಾಲ್ಪನಿಕ ವಿವರಗಳನ್ನು ಬಳಸಿ.",
        "hi": "केवल सार्वजनिक पहचान विवरण। कोई दस्तावेज़ अपलोड नहीं होते। इस डेमो में काल्पनिक विवरण इस्तेमाल करें।"},
    "District": {"kn": "ಜಿಲ್ಲೆ", "hi": "जिला"},
    "Taluk": {"kn": "ತಾಲೂಕು", "hi": "तालुक"},
    "Hobli": {"kn": "ಹೋಬಳಿ", "hi": "होबली"},
    "Village": {"kn": "ಗ್ರಾಮ", "hi": "गाँव"},
    "Survey number": {"kn": "ಸರ್ವೆ ನಂಬರ್", "hi": "सर्वे नंबर"},
    "Surnoc": {"kn": "ಸರ್ನೋಕ್", "hi": "सरनोक"},
    "Hissa": {"kn": "ಹಿಸ್ಸಾ", "hi": "हिस्सा"},
    "Extent (acres-guntas)": {"kn": "ವಿಸ್ತೀರ್ಣ (ಎಕರೆ-ಗುಂಟೆ)", "hi": "क्षेत्रफल (एकड़-गुंटा)"},
    "Owner name on the record": {"kn": "ದಾಖಲೆಯಲ್ಲಿರುವ ಮಾಲೀಕರ ಹೆಸರು", "hi": "रिकॉर्ड में मालिक का नाम"},
    "I confirm this land belongs to me or my family.": {"kn": "ಈ ಜಮೀನು ನನಗೆ ಅಥವಾ ನನ್ನ ಕುಟುಂಬಕ್ಕೆ ಸೇರಿದ್ದು ಎಂದು ನಾನು ಖಚಿತಪಡಿಸುತ್ತೇನೆ.", "hi": "मैं पुष्टि करता/करती हूँ कि यह ज़मीन मेरी या मेरे परिवार की है।"},
    "Cancel": {"kn": "ರದ್ದುಮಾಡಿ", "hi": "रद्द करें"},
    "← My lands": {"kn": "← ನನ್ನ ಜಮೀನುಗಳು", "hi": "← मेरी ज़मीनें"},
    "File a mutation": {"kn": "ಮ್ಯುಟೇಶನ್ ಸಲ್ಲಿಸಿ", "hi": "म्यूटेशन दर्ज करें"},
    "A mutation stays Pending until the registrar approves or rejects it.": {
        "kn": "ನೋಂದಣಾಧಿಕಾರಿ ಅನುಮೋದಿಸುವವರೆಗೆ ಅಥವಾ ತಿರಸ್ಕರಿಸುವವರೆಗೆ ಮ್ಯುಟೇಶನ್ ಬಾಕಿ ಇರುತ್ತದೆ.",
        "hi": "रजिस्ट्रार के मंज़ूर या अस्वीकार करने तक म्यूटेशन लंबित रहता है।"},
    "Type": {"kn": "ಪ್ರಕಾರ", "hi": "प्रकार"},
    "Note (optional)": {"kn": "ಟಿಪ್ಪಣಿ (ಐಚ್ಛಿಕ)", "hi": "टिप्पणी (वैकल्पिक)"},
    "File mutation": {"kn": "ಮ್ಯುಟೇಶನ್ ಸಲ್ಲಿಸಿ", "hi": "म्यूटेशन दर्ज करें"},
    "Alerts link": {"kn": "ಎಚ್ಚರಿಕೆಗಳ ಲಿಂಕ್", "hi": "अलर्ट लिंक"},
    "Give this private link to Land Record Watch so it can check this record. It shows a masked owner name. Anyone who has it can view the record, so keep it private.": {
        "kn": "ಈ ದಾಖಲೆಯನ್ನು ಪರಿಶೀಲಿಸಲು ಈ ಖಾಸಗಿ ಲಿಂಕ್ ಅನ್ನು ಲ್ಯಾಂಡ್ ರೆಕಾರ್ಡ್ ವಾಚ್‌ಗೆ ನೀಡಿ. ಇದರಲ್ಲಿ ಮಾಲೀಕರ ಹೆಸರು ಮರೆಮಾಡಲ್ಪಟ್ಟಿದೆ. ಲಿಂಕ್ ಇರುವ ಯಾರಾದರೂ ದಾಖಲೆಯನ್ನು ನೋಡಬಹುದು, ಆದ್ದರಿಂದ ಅದನ್ನು ಗೌಪ್ಯವಾಗಿಡಿ.",
        "hi": "इस रिकॉर्ड की जाँच के लिए यह निजी लिंक लैंड रिकॉर्ड वॉच को दें। इसमें मालिक का नाम छिपा हुआ दिखता है। जिसके पास भी यह लिंक होगा वह रिकॉर्ड देख सकता है, इसलिए इसे गोपनीय रखें।"},
    "Alert language": {"kn": "ಎಚ್ಚರಿಕೆಯ ಭಾಷೆ", "hi": "अलर्ट की भाषा"},
    "Land Record Watch sends its alerts, text and voice, in the language you pick here.": {
        "kn": "ಲ್ಯಾಂಡ್ ರೆಕಾರ್ಡ್ ವಾಚ್ ತನ್ನ ಎಚ್ಚರಿಕೆಗಳನ್ನು, ಪಠ್ಯ ಮತ್ತು ಧ್ವನಿ ಎರಡನ್ನೂ, ನೀವು ಇಲ್ಲಿ ಆರಿಸುವ ಭಾಷೆಯಲ್ಲಿ ಕಳುಹಿಸುತ್ತದೆ.",
        "hi": "लैंड रिकॉर्ड वॉच अपने अलर्ट, टेक्स्ट और आवाज़ दोनों, उसी भाषा में भेजता है जो आप यहाँ चुनते हैं।"},
    "Language": {"kn": "ಭಾಷೆ", "hi": "भाषा"},
    "Save language": {"kn": "ಭಾಷೆ ಉಳಿಸಿ", "hi": "भाषा सहेजें"},
    "History": {"kn": "ಇತಿಹಾಸ", "hi": "इतिहास"},
    "Sale": {"kn": "ಮಾರಾಟ", "hi": "बिक्री"},
    "Inheritance": {"kn": "ಪಿತ್ರಾರ್ಜಿತ", "hi": "विरासत"},
    "Partition": {"kn": "ವಿಭಜನೆ", "hi": "बँटवारा"},
    "Gift": {"kn": "ದಾನ", "hi": "उपहार"},
    "Correction": {"kn": "ತಿದ್ದುಪಡಿ", "hi": "सुधार"},

    # ---- record view (landlord, buyer, registrar)
    "Place": {"kn": "ಸ್ಥಳ", "hi": "स्थान"},
    "Survey / surnoc / hissa": {"kn": "ಸರ್ವೆ / ಸರ್ನೋಕ್ / ಹಿಸ್ಸಾ", "hi": "सर्वे / सरनोक / हिस्सा"},
    "Owner": {"kn": "ಮಾಲೀಕರು", "hi": "मालिक"},
    "Last updated": {"kn": "ಕೊನೆಯ ಬಾರಿ ನವೀಕರಿಸಿದ್ದು", "hi": "अंतिम अपडेट"},
    "No pending mutations": {"kn": "ಬಾಕಿ ಮ್ಯುಟೇಶನ್‌ಗಳಿಲ್ಲ", "hi": "कोई लंबित म्यूटेशन नहीं"},
    "Nothing is waiting for a decision on this record.": {"kn": "ಈ ದಾಖಲೆಯ ಮೇಲೆ ಯಾವುದೇ ತೀರ್ಮಾನ ಬಾಕಿ ಇಲ್ಲ.", "hi": "इस रिकॉर्ड पर किसी निर्णय का इंतज़ार नहीं है।"},
    "This record may change when the registrar decides.": {"kn": "ನೋಂದಣಾಧಿಕಾರಿ ತೀರ್ಮಾನಿಸಿದಾಗ ಈ ದಾಖಲೆ ಬದಲಾಗಬಹುದು.", "hi": "रजिस्ट्रार के निर्णय के बाद यह रिकॉर्ड बदल सकता है।"},
    "Mutation history": {"kn": "ಮ್ಯುಟೇಶನ್ ಇತಿಹಾಸ", "hi": "म्यूटेशन इतिहास"},
    "Reference": {"kn": "ಉಲ್ಲೇಖ", "hi": "संदर्भ"},
    "Date": {"kn": "ದಿನಾಂಕ", "hi": "तारीख"},
    "Status": {"kn": "ಸ್ಥಿತಿ", "hi": "स्थिति"},
    "No mutations on this record yet.": {"kn": "ಈ ದಾಖಲೆಯಲ್ಲಿ ಇನ್ನೂ ಯಾವುದೇ ಮ್ಯುಟೇಶನ್ ಇಲ್ಲ.", "hi": "इस रिकॉर्ड पर अभी कोई म्यूटेशन नहीं है।"},
    "Pending": {"kn": "ಬಾಕಿ", "hi": "लंबित"},
    "Approved": {"kn": "ಅನುಮೋದಿತ", "hi": "मंज़ूर"},
    "Rejected": {"kn": "ತಿರಸ್ಕೃತ", "hi": "अस्वीकृत"},
    "← Back to search": {"kn": "← ಹುಡುಕಾಟಕ್ಕೆ ಹಿಂತಿರುಗಿ", "hi": "← खोज पर वापस"},
    "Record status": {"kn": "ದಾಖಲೆಯ ಸ್ಥಿತಿ", "hi": "रिकॉर्ड की स्थिति"},
    "The owner's name is masked. Fictional data, not an official record.": {"kn": "ಮಾಲೀಕರ ಹೆಸರು ಮರೆಮಾಡಲಾಗಿದೆ. ಕಾಲ್ಪನಿಕ ಮಾಹಿತಿ, ಅಧಿಕೃತ ದಾಖಲೆ ಅಲ್ಲ.", "hi": "मालिक का नाम छिपाया गया है। काल्पनिक डेटा, आधिकारिक रिकॉर्ड नहीं।"},
    "Open registrar tools": {"kn": "ನೋಂದಣಾಧಿಕಾರಿ ಸಾಧನಗಳನ್ನು ತೆರೆಯಿರಿ", "hi": "रजिस्ट्रार टूल खोलें"},

    # ---- search
    "Search a record": {"kn": "ದಾಖಲೆ ಹುಡುಕಿ", "hi": "रिकॉर्ड खोजें"},
    "Enter at least the district and the survey number. Add more details to narrow the search.": {
        "kn": "ಕನಿಷ್ಠ ಜಿಲ್ಲೆ ಮತ್ತು ಸರ್ವೆ ನಂಬರ್ ನಮೂದಿಸಿ. ಹುಡುಕಾಟವನ್ನು ಕಿರಿದಾಗಿಸಲು ಹೆಚ್ಚಿನ ವಿವರಗಳನ್ನು ಸೇರಿಸಿ.",
        "hi": "कम से कम जिला और सर्वे नंबर लिखें। खोज को सीमित करने के लिए और विवरण जोड़ें।"},
    "District *": {"kn": "ಜಿಲ್ಲೆ *", "hi": "जिला *"},
    "Survey number *": {"kn": "ಸರ್ವೆ ನಂಬರ್ *", "hi": "सर्वे नंबर *"},
    "No record found. Check the spelling and the survey number.": {"kn": "ಯಾವುದೇ ದಾಖಲೆ ಸಿಗಲಿಲ್ಲ. ಕಾಗುಣಿತ ಮತ್ತು ಸರ್ವೆ ನಂಬರ್ ಪರಿಶೀಲಿಸಿ.", "hi": "कोई रिकॉर्ड नहीं मिला। वर्तनी और सर्वे नंबर जाँचें।"},

    # ---- registrar pages
    "Pending mutations": {"kn": "ಬಾಕಿ ಮ್ಯುಟೇಶನ್‌ಗಳು", "hi": "लंबित म्यूटेशन"},
    "Demo staff view. Approve or reject each request.": {"kn": "ಡೆಮೊ ಸಿಬ್ಬಂದಿ ನೋಟ. ಪ್ರತಿ ಅರ್ಜಿಯನ್ನು ಅನುಮೋದಿಸಿ ಅಥವಾ ತಿರಸ್ಕರಿಸಿ.", "hi": "डेमो स्टाफ़ दृश्य। हर अनुरोध को मंज़ूर या अस्वीकार करें।"},
    "Ref": {"kn": "ಉಲ್ಲೇಖ", "hi": "संदर्भ"},
    "Land": {"kn": "ಜಮೀನು", "hi": "ज़मीन"},
    "Filed": {"kn": "ಸಲ್ಲಿಸಿದ್ದು", "hi": "दर्ज किया गया"},
    "Review": {"kn": "ಪರಿಶೀಲಿಸಿ", "hi": "समीक्षा करें"},
    "Nothing is waiting. 🎉": {"kn": "ಯಾವುದೂ ಬಾಕಿ ಇಲ್ಲ. 🎉", "hi": "कुछ भी लंबित नहीं है। 🎉"},
    "Search any record": {"kn": "ಯಾವುದೇ ದಾಖಲೆ ಹುಡುಕಿ", "hi": "कोई भी रिकॉर्ड खोजें"},
    "← Pending queue": {"kn": "← ಬಾಕಿ ಇರುವ ಪಟ್ಟಿ", "hi": "← लंबित सूची"},
    "Decision note (optional)": {"kn": "ತೀರ್ಮಾನದ ಟಿಪ್ಪಣಿ (ಐಚ್ಛಿಕ)", "hi": "निर्णय की टिप्पणी (वैकल्पिक)"},
    "Approve": {"kn": "ಅನುಮೋದಿಸಿ", "hi": "मंज़ूर करें"},
    "Reject": {"kn": "ತಿರಸ್ಕರಿಸಿ", "hi": "अस्वीकार करें"},
    "Correct the extent": {"kn": "ವಿಸ್ತೀರ್ಣ ತಿದ್ದಿ", "hi": "क्षेत्रफल सुधारें"},
    "New extent (acres-guntas)": {"kn": "ಹೊಸ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ-ಗುಂಟೆ)", "hi": "नया क्षेत्रफल (एकड़-गुंटा)"},
    "Update extent": {"kn": "ವಿಸ್ತೀರ್ಣ ನವೀಕರಿಸಿ", "hi": "क्षेत्रफल अपडेट करें"},
    "Record an ownership transfer": {"kn": "ಮಾಲೀಕತ್ವ ವರ್ಗಾವಣೆ ದಾಖಲಿಸಿ", "hi": "स्वामित्व हस्तांतरण दर्ज करें"},
    "New owner name (made up)": {"kn": "ಹೊಸ ಮಾಲೀಕರ ಹೆಸರು (ಕಾಲ್ಪನಿಕ)", "hi": "नए मालिक का नाम (काल्पनिक)"},
    "Record transfer": {"kn": "ವರ್ಗಾವಣೆ ದಾಖಲಿಸಿ", "hi": "हस्तांतरण दर्ज करें"},

    # ---- errors
    "Go to home": {"kn": "ಮುಖಪುಟಕ್ಕೆ ಹೋಗಿ", "hi": "होम पर जाएँ"},
    "You do not have access to this page.": {"kn": "ಈ ಪುಟಕ್ಕೆ ನಿಮಗೆ ಪ್ರವೇಶವಿಲ್ಲ.", "hi": "आपको इस पेज तक पहुँच नहीं है।"},
    "We could not find that page.": {"kn": "ಆ ಪುಟ ಸಿಗಲಿಲ್ಲ.", "hi": "वह पेज नहीं मिला।"},
    "That request could not be processed. Go back and try again.": {"kn": "ಆ ಕೋರಿಕೆಯನ್ನು ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ಹಿಂದಕ್ಕೆ ಹೋಗಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.", "hi": "वह अनुरोध पूरा नहीं हो सका। वापस जाकर फिर कोशिश करें।"},

    # ---- messages shown after an action
    "Account created. Welcome.": {"kn": "ಖಾತೆ ರಚಿಸಲಾಗಿದೆ. ಸ್ವಾಗತ.", "hi": "खाता बन गया। स्वागत है।"},
    "Registrar account created.": {"kn": "ನೋಂದಣಾಧಿಕಾರಿ ಖಾತೆ ರಚಿಸಲಾಗಿದೆ.", "hi": "रजिस्ट्रार खाता बन गया।"},
    "Too many wrong attempts. Try again in a few minutes.": {"kn": "ಹಲವು ತಪ್ಪು ಪ್ರಯತ್ನಗಳು. ಕೆಲವು ನಿಮಿಷಗಳ ನಂತರ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.", "hi": "बहुत ज़्यादा ग़लत कोशिशें। कुछ मिनट बाद फिर कोशिश करें।"},
    "Email or password is wrong.": {"kn": "ಇಮೇಲ್ ಅಥವಾ ಪಾಸ್‌ವರ್ಡ್ ತಪ್ಪಾಗಿದೆ.", "hi": "ईमेल या पासवर्ड ग़लत है।"},
    "Land registered.": {"kn": "ಜಮೀನು ನೋಂದಾಯಿಸಲಾಗಿದೆ.", "hi": "ज़मीन पंजीकृत हो गई।"},
    "You already have 3 pending mutations on this land. Wait for the registrar.": {"kn": "ಈ ಜಮೀನಿನ ಮೇಲೆ ನಿಮಗೆ ಈಗಾಗಲೇ 3 ಮ್ಯುಟೇಶನ್‌ಗಳು ಬಾಕಿ ಇವೆ. ನೋಂದಣಾಧಿಕಾರಿಗಾಗಿ ಕಾಯಿರಿ.", "hi": "इस ज़मीन पर आपके 3 म्यूटेशन पहले से लंबित हैं। रजिस्ट्रार का इंतज़ार करें।"},
    "Alert language saved. The next check will send alerts in this language.": {"kn": "ಎಚ್ಚರಿಕೆಯ ಭಾಷೆ ಉಳಿಸಲಾಗಿದೆ. ಮುಂದಿನ ಪರಿಶೀಲನೆಯಿಂದ ಎಚ್ಚರಿಕೆಗಳು ಈ ಭಾಷೆಯಲ್ಲಿ ಬರುತ್ತವೆ.", "hi": "अलर्ट की भाषा सहेज ली गई। अगली जाँच से अलर्ट इसी भाषा में आएँगे।"},
    "Too many searches. Wait a minute.": {"kn": "ಹಲವು ಹುಡುಕಾಟಗಳು. ಒಂದು ನಿಮಿಷ ಕಾಯಿರಿ.", "hi": "बहुत ज़्यादा खोजें। एक मिनट रुकें।"},
    "Enter at least the district and the survey number.": {"kn": "ಕನಿಷ್ಠ ಜಿಲ್ಲೆ ಮತ್ತು ಸರ್ವೆ ನಂಬರ್ ನಮೂದಿಸಿ.", "hi": "कम से कम जिला और सर्वे नंबर लिखें।"},
    "Extent must look like 2-10.": {"kn": "ವಿಸ್ತೀರ್ಣ 2-10 ರೀತಿಯಲ್ಲಿರಬೇಕು.", "hi": "क्षेत्रफल 2-10 जैसा होना चाहिए।"},
    "Extent updated.": {"kn": "ವಿಸ್ತೀರ್ಣ ನವೀಕರಿಸಲಾಗಿದೆ.", "hi": "क्षेत्रफल अपडेट हो गया।"},
    "Enter the new owner's name.": {"kn": "ಹೊಸ ಮಾಲೀಕರ ಹೆಸರು ನಮೂದಿಸಿ.", "hi": "नए मालिक का नाम लिखें।"},
    "Ownership transfer recorded.": {"kn": "ಮಾಲೀಕತ್ವ ವರ್ಗಾವಣೆ ದಾಖಲಿಸಲಾಗಿದೆ.", "hi": "स्वामित्व हस्तांतरण दर्ज हो गया।"},
    "Enter a valid email address.": {"kn": "ಸರಿಯಾದ ಇಮೇಲ್ ವಿಳಾಸ ನಮೂದಿಸಿ.", "hi": "सही ईमेल पता लिखें।"},
    "Enter your name.": {"kn": "ನಿಮ್ಮ ಹೆಸರು ನಮೂದಿಸಿ.", "hi": "अपना नाम लिखें।"},
    "Enter a name.": {"kn": "ಹೆಸರು ನಮೂದಿಸಿ.", "hi": "नाम लिखें।"},
    "The two passwords do not match.": {"kn": "ಎರಡು ಪಾಸ್‌ವರ್ಡ್‌ಗಳು ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ.", "hi": "दोनों पासवर्ड मेल नहीं खाते।"},
    "That email is already registered. Try logging in.": {"kn": "ಆ ಇಮೇಲ್ ಈಗಾಗಲೇ ನೋಂದಾಯಿತವಾಗಿದೆ. ಲಾಗಿನ್ ಮಾಡಲು ಪ್ರಯತ್ನಿಸಿ.", "hi": "वह ईमेल पहले से पंजीकृत है। लॉग इन करके देखें।"},
    "That email is already registered.": {"kn": "ಆ ಇಮೇಲ್ ಈಗಾಗಲೇ ನೋಂದಾಯಿತವಾಗಿದೆ.", "hi": "वह ईमेल पहले से पंजीकृत है।"},
    "Wrong setup code.": {"kn": "ಸೆಟಪ್ ಕೋಡ್ ತಪ್ಪಾಗಿದೆ.", "hi": "सेटअप कोड ग़लत है।"},
    "Use at least 10 characters.": {"kn": "ಕನಿಷ್ಠ 10 ಅಕ್ಷರಗಳನ್ನು ಬಳಸಿ.", "hi": "कम से कम 10 अक्षर इस्तेमाल करें।"},
    "Use both letters and numbers.": {"kn": "ಅಕ್ಷರ ಮತ್ತು ಅಂಕೆ ಎರಡನ್ನೂ ಬಳಸಿ.", "hi": "अक्षर और अंक दोनों इस्तेमाल करें।"},
    "Do not put your email name in your password.": {"kn": "ನಿಮ್ಮ ಇಮೇಲ್ ಹೆಸರನ್ನು ಪಾಸ್‌ವರ್ಡ್‌ನಲ್ಲಿ ಬಳಸಬೇಡಿ.", "hi": "अपने ईमेल का नाम पासवर्ड में न रखें।"},
    "District, taluk, hobli and village need letters or numbers only (2 to 60 characters).": {"kn": "ಜಿಲ್ಲೆ, ತಾಲೂಕು, ಹೋಬಳಿ ಮತ್ತು ಗ್ರಾಮಕ್ಕೆ ಅಕ್ಷರ ಅಥವಾ ಅಂಕೆಗಳು ಮಾತ್ರ ಬೇಕು (2 ರಿಂದ 60 ಅಕ್ಷರಗಳು).", "hi": "जिला, तालुक, होबली और गाँव में केवल अक्षर या अंक हों (2 से 60 अक्षर)।"},
    "Survey number, surnoc and hissa can only use letters, numbers, / and -.": {"kn": "ಸರ್ವೆ ನಂಬರ್, ಸರ್ನೋಕ್ ಮತ್ತು ಹಿಸ್ಸಾದಲ್ಲಿ ಅಕ್ಷರ, ಅಂಕೆ, / ಮತ್ತು - ಮಾತ್ರ ಬಳಸಬಹುದು.", "hi": "सर्वे नंबर, सरनोक और हिस्सा में केवल अक्षर, अंक, / और - चल सकते हैं।"},
    "Extent must look like 2-10 (acres-guntas).": {"kn": "ವಿಸ್ತೀರ್ಣ 2-10 (ಎಕರೆ-ಗುಂಟೆ) ರೀತಿಯಲ್ಲಿರಬೇಕು.", "hi": "क्षेत्रफल 2-10 (एकड़-गुंटा) जैसा होना चाहिए।"},
    "Enter the owner's name.": {"kn": "ಮಾಲೀಕರ ಹೆಸರು ನಮೂದಿಸಿ.", "hi": "मालिक का नाम लिखें।"},
    "Please confirm this land belongs to you or your family.": {"kn": "ಈ ಜಮೀನು ನಿಮಗೆ ಅಥವಾ ನಿಮ್ಮ ಕುಟುಂಬಕ್ಕೆ ಸೇರಿದ್ದು ಎಂದು ದಯವಿಟ್ಟು ಖಚಿತಪಡಿಸಿ.", "hi": "कृपया पुष्टि करें कि यह ज़मीन आपकी या आपके परिवार की है।"},
    "This survey number is already registered in the demo registry.": {"kn": "ಈ ಸರ್ವೆ ನಂಬರ್ ಈಗಾಗಲೇ ಡೆಮೊ ನೋಂದಣಿಯಲ್ಲಿ ನೋಂದಾಯಿತವಾಗಿದೆ.", "hi": "यह सर्वे नंबर डेमो रजिस्ट्री में पहले से पंजीकृत है।"},

    # ---- history lines and words used inside patterns
    "Ownership transfer recorded": {"kn": "ಮಾಲೀಕತ್ವ ವರ್ಗಾವಣೆ ದಾಖಲಿಸಲಾಗಿದೆ", "hi": "स्वामित्व हस्तांतरण दर्ज हुआ"},
    "kn": {"kn": "ಕನ್ನಡ", "hi": "कन्नड़"},
    "hi": {"kn": "ಹಿಂದಿ", "hi": "हिन्दी"},
    "en": {"kn": "ಇಂಗ್ಲಿಷ್", "hi": "अंग्रेज़ी"},
    "approved": {"kn": "ಅನುಮೋದಿಸಲಾಗಿದೆ", "hi": "मंज़ूर हुआ"},
    "rejected": {"kn": "ತಿರಸ್ಕರಿಸಲಾಗಿದೆ", "hi": "अस्वीकृत हुआ"},
}

# (regular expression, {"kn": template, "hi": template}); {1}, {2} are the matched parts, translated if known
PATTERNS = [
    (r"Log in as (\w+)", {"kn": "{1} ಆಗಿ ಲಾಗಿನ್ ಮಾಡಿ", "hi": "{1} के रूप में लॉग इन करें"}),
    (r"Create (landlord|buyer) account", {"kn": "{1} ಖಾತೆ ರಚಿಸಿ", "hi": "{1} का खाता बनाएँ"}),
    (r"(.+) · Sy\. (.+)", {"kn": "{1} · ಸರ್ವೆ ನಂ. {2}", "hi": "{1} · सर्वे नं. {2}"}),
    (r"(.+) · extent (\S+)", {"kn": "{1} · ವಿಸ್ತೀರ್ಣ {2}", "hi": "{1} · क्षेत्रफल {2}"}),
    (r"(.+) · (Landlord|Buyer|Registrar)", {"kn": "{1} · {2}", "hi": "{1} · {2}"}),
    (r"(\d+) mutations? pending", {"kn": "{1} ಮ್ಯುಟೇಶನ್ ಬಾಕಿ", "hi": "{1} म्यूटेशन लंबित"}),
    (r"(\d+) results?", {"kn": "{1} ಫಲಿತಾಂಶ", "hi": "{1} परिणाम"}),
    (r"(MR-\d+) · (\w+)", {"kn": "{1} · {2}", "hi": "{1} · {2}"}),
    (r"Filed (\S+)( · .*)?", {"kn": "ಸಲ್ಲಿಸಿದ ದಿನಾಂಕ {1}{2}", "hi": "दर्ज करने की तारीख {1}{2}"}),
    (r"Mutation (MR-\d+) filed\. It stays Pending until the registrar decides\.",
        {"kn": "ಮ್ಯುಟೇಶನ್ {1} ಸಲ್ಲಿಸಲಾಗಿದೆ. ನೋಂದಣಾಧಿಕಾರಿ ತೀರ್ಮಾನಿಸುವವರೆಗೆ ಇದು ಬಾಕಿ ಇರುತ್ತದೆ.",
         "hi": "म्यूटेशन {1} दर्ज हो गया। रजिस्ट्रार के निर्णय तक यह लंबित रहेगा।"}),
    (r"(MR-\d+) (approved|rejected)\.", {"kn": "{1} {2}.", "hi": "{1} {2}।"}),
    (r"Land registered, extent (\S+)", {"kn": "ಜಮೀನು ನೋಂದಾಯಿಸಲಾಗಿದೆ, ವಿಸ್ತೀರ್ಣ {1}", "hi": "ज़मीन पंजीकृत हुई, क्षेत्रफल {1}"}),
    (r"Mutation (MR-\d+) filed \((\w+)\)", {"kn": "ಮ್ಯುಟೇಶನ್ {1} ಸಲ್ಲಿಸಲಾಗಿದೆ ({2})", "hi": "म्यूटेशन {1} दर्ज हुआ ({2})"}),
    (r"Mutation (MR-\d+) (approved|rejected)", {"kn": "ಮ್ಯುಟೇಶನ್ {1} {2}", "hi": "म्यूटेशन {1} {2}"}),
    (r"Extent changed from (\S+) to (\S+)", {"kn": "ವಿಸ್ತೀರ್ಣ {1} ರಿಂದ {2} ಕ್ಕೆ ಬದಲಾಯಿತು", "hi": "क्षेत्रफल {1} से {2} हो गया"}),
    (r"Alert language changed to (\w+)", {"kn": "ಎಚ್ಚರಿಕೆಯ ಭಾಷೆ {1} ಗೆ ಬದಲಾಯಿತು", "hi": "अलर्ट की भाषा बदलकर {1} हुई"}),
    (r"(.+?) · Land Record Watch", {"kn": "{1} · ಲ್ಯಾಂಡ್ ರೆಕಾರ್ಡ್ ವಾಚ್", "hi": "{1} · लैंड रिकॉर्ड वॉच"}),
]
