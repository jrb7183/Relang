""" Reformats list of phonemes to be interpretable by the frontend """

def tableFormatter(cons_list):
    cons_dict = {}
    for cons_tup in cons_list:
        
        # Find Place
        place = ""
        match cons_tup[1] % 32:
            case 12:
                place = "Bilabial"
            case 4:
                place = "Labio-dental"
            case 26:
                place = "Dental"
            case 10:
                place = "Alveolar"
            case 2:
                place = "Retroflex"
            case 18:
                place = "Post-Alveolar"
            case 19:
                place = "Palatal"
            case 9:
                place = "Velar"
            case 17:
                place = "Uvular"
            case 25:
                place = "Pharyngeal"
            case 0:
                place = "Glottal"

        if place in cons_dict:
            cons_dict[place] += [cons_tup[0]]
        else:
            cons_dict[place] = [cons_tup[0]]

    return cons_dict