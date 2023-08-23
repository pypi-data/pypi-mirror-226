def flatten_list2darr(lst):
    full_list = []
    for ls in lst:
        for item in ls:
            full_list.append(item)
    return full_list        

# print(flatten_list2darr([[1,2], [3,4,5]]))

def flatten_list3darr(list):
    full_list = []
    for sublist in list:
        for sublist2 in sublist:
            for element in sublist2:
                full_list.append(element)
    return full_list

# print(flatten_list3darr([[[1,2], [3,4], [5,6,7]]]))
