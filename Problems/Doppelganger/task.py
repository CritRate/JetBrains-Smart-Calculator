# the object_list has already been defined
# write your code here
d = dict()
count = 0
for i in object_list:
    if isinstance(i, collections.Hashable):
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
print(sum(x for x in d.values() if x > 1))
