"""
Filters out differences between user and Relang notation. Most of these will be
easier symbols to type than IPA ones (i.e. ' instead of ’ for ejectives), but
Relang also just doesn't use the combining bar (͡ ) for affricates, so that needs
to be removed as well.  
"""
def clean_input(phoneme: str) -> str:

    # It's impossible to see, but the second element in the list below is an umlaut (̈ )
    for diacritic in ["͡", "̈", "̯", "̩"]:
        if diacritic in phoneme:
            phoneme = phoneme[:phoneme.index(diacritic)] + phoneme[phoneme.index(diacritic) + 1:]
    
    if "'" in phoneme:
        phoneme = phoneme[:phoneme.index("'")] + "’" + phoneme[phoneme.index("'") + 1:] 

    if "ˀ" in phoneme:
        phoneme = phoneme[:phoneme.index("ˀ")] + "’" + phoneme[phoneme.index("ˀ") + 1:] 

    # There's likely more notationaal differences to be found, but those require some more user testing

    return phoneme