""" Reformats list of phonemes to be interpretable by the frontend """

def table_formatter(cons_list: list[tuple]) -> dict[str, list]:
    cons_dict = {}
    label_row = ["" for _ in range(11)]
    order_list = [[] for _ in range(11)]
    
    # Sort by laryngeal features
    cons_list.sort(key=lambda cons_tup: cons_tup[1] & (7 << 5))

    # Sort by place
    for cons_tup in cons_list:
        
        places = ["Bilabial", "Labio-dental", "Dental", "Alveolar", "Retroflex", "Post-Alveolar", "Palatal", "Velar", "Uvular", "Pharyngeal", "Glottal"]
        place_nums = [12, 4, 26, 10, 2, 18, 19, 9, 17, 25, 0]
        
        i = place_nums.index(cons_tup[1] % 32)
        order_list[i] += [cons_tup]
        label_row[i] = places[i]

    # Filter out empty columns
    order_list = list(filter(lambda sublist: sublist, order_list))
    label_row = list(filter(lambda label: label, label_row))

    # Initialize cons_dict 
    cons_dict["Consonants"] = list(map(lambda label: {"isHeader": True, "text": label}, label_row))
    manners = ["Plosive", "Nasal", "Affricate", "Trill", "Fricative", "Tap", "Sibilant", "Approximant"]
    
    for manner in manners:
        cons_dict[manner] = [{"isHeader": False, "text": ""} for _ in range(len(label_row))]

    used_manners = set()
    # Add consonants to cons_dict by manner
    for i in range(len(order_list)):
        same_list = []
        
        for cons_tup in order_list[i]:    
            manner = manners[(cons_tup[1] >> 8) % 8]
            used_manners.add(manner)

            if manner in same_list:
                cons_dict[manner][i]["text"] += ", " + cons_tup[0]

            else:
                cons_dict[manner][i]["text"] = cons_tup[0]
                same_list += [manner]

    # Remove unused manner
    for manner in manners:
        if manner not in used_manners:
            del cons_dict[manner]

    return cons_dict