from ntlk import FregDist, Text, ngrams
# using the method of ntlk to analys the html of the website that contains
# Amtliche Bekanntmachung

######-------------------------------------URL levels
# DynmoDB connections

# Count most 10 /20 frequent words for each urls
text = Text('')
fdist = FregDist(text)
ten = fdist.most_comment(10)

# Count the most 10 common 2 grams word
twograms = ngrams (text,2)

# Count the 10 most common nouns that appear

# Count the most commom 4 words
fourgrams = ngrams (text,4)

# Update the result_summerizer table
# New column (ten_most_common_word)(two_grams)(four_grams)


#####----------------------------------------Loop over all urls
# Select the most common words agrain from each column word, 2 grams, 4 grams and noun