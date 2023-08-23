def flatten_list2darr(lst):
    full_list = []
    for ls in lst:
        for item in ls:
            full_list.append(item)
    return full_list        

# print(flatten_list2darr([[1,2], [3,4,5]]))
