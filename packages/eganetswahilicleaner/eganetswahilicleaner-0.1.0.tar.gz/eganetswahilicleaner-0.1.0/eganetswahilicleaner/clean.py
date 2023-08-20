import nltk
import nltk.corpus
import re
import unicodedata
from string import punctuation

STOPWORD=['na',
 'lakini','ingawa','ingawaje',
 'kwa','sababu','hadi','hata',
 'kama','ambapo','ambamo',
 'ambako','ambacho','ambao','ambaye','ilhali','ya','yake','yao','yangu','yetu',
 'yenu','vya','ee','so','vyao','vyake','vyangu','vyenu','vyetu','yako','yao','hizo','yenu','mimi',
'sisi','wewe','nyinyi','yeye','wao','nao','nasi','nanyi','ni','alikuwa','atakuwa','hii','hizi',
'zile','ile','hivi','vile','za','zake','zao','zenu','kwenye','katika','kwa','kwao','kwenu','kwetu',
'dhidi','kati','miongoni','katikati','wakati','kabla','baada','baadaye','nje','tena','mbali',
'halafu','hapa','pale','mara','mara','yoyote','wowote','chochote','vyovyote','yeyote','lolote',
'mwenye','mwenyewe','lenyewe','lenye','wote','lote','vyote','nyote','kila','zaidi','hapana',
'ndiyo','au','ama','ama','sio','siye','tu','budi','nyingi','nyingine','wengine','mwingine','zingine',
'lingine','kingine','chote','sasa','basi','bila','cha','chini','hapo','pale','huku','kule',
'humu','hivyo','hivyohivyo','vivyo','palepale','fauka','hiyohiyo','zile','zilezile','hao','haohao',
'huku','hukuhuku','humuhumu','huko','hukohuko','huo','huohuo','hili','hilihili','ilikuwa',
'juu','karibu','kila','kima','kisha','kutoka','kwenda','kubwa','ndogo','kwamba','kuwa','la',
'lao','lo','mara','na','mdogo','mkubwa','pia','aidha','vile','kadhalika','halikadhalika',
'ni','sana','pamoja','pamoja','tafadhali','tena','wa','wake','wao','ya','yule','wale','zangu',
'nje','afanaleki','salale','oyee','yupi','ipi','lipi','ngapi','yetu','si','angali','wangali',
'loo','la','ohoo','barabara','oyee','ewaa','walahi','masalale','duu','toba','mh','kumbe',
'ala','ebo','haraka','pole','polepole','harakaharaka','hiyo','hivyo','vyovyote','atakuwa',
'itakuwa','mtakuwa','tutakuwa','labda','yumkini','haiyumkini','yapata','takribani','hususani',
'yawezekana','nani','juu','chini','ndani','baadhi','kuliko','vile','mwa','kwa','hasha','hivyo',
'moja','kisha','pili','kwanza','ili','je','jinsi','ila','ila','nini','hasa','huu','zako',
'mimi','a', 'about', 'above', 'after', 'again', 'against', 'all', 'also', 'am', 'an', 'and',
'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below',
'between', 'both', 'but', 'by', 'can', "can't", 'cannot', 'com', 'could', "couldn't", 'did',
"didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'else', 'ever',
'few', 'for', 'from', 'further', 'get', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having',
'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how',
"how's", 'however', 'http', 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it',
"it's", 'its', 'itself', 'just', 'k', "let's", 'like', 'me', 'more', 'most', "mustn't", 'my', 'myself',
'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'otherwise', 'ought', 'our', 'ours',
'ourselves', 'o ut', 'over', 'own', 'r', 'same', 'shall', "shan't", 'she', "she'd", "she'll", "she's",
'should', "shouldn't", 'since', 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs',
'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're",
"they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't",
'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where',
"where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't",
'www', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']

# def remove_emojis(text):
#     return emoji.demojize(text)


def clean_text(text):
    # Remove emojis
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove non-alphanumeric characters
    text = re.sub(r"[^A-Za-z0-9]", " ", text)
    
    # Remove numbers
    text = re.sub(r'\b\d+(?:\.\d+)?\s+', '', text)
    
    # Remove Unicode characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove punctuation
    text = ''.join([c for c in text if c not in punctuation])
    
    # Remove parentheses
    text = re.sub('[()]', '', text)
    
    # Remove non-alphabetic characters
    text = re.sub("[^a-zA-Z]", " ", text)
    
    # Remove consecutive "h" characters
    text = re.sub(u"h{1,}", "", text)
    
    # Remove short words
    text = ' '.join([w for w in text.split() if len(w) > 2])
    
    # Remove stop words
    text = ' '.join([word for word in text.split() if word not in STOPWORD])
    
    # Remove excess whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text