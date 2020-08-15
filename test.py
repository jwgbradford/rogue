def find_lowest_room(unordered_list, required_index):
    sorted_list = sorted(unordered_list)
    distance = sorted_list[required_index]
    distances = [i for i, e in enumerate(unordered_list) if e == distance]
    return distances

original_list = [
    [0, 1, 7, 3, 4, 6],
    [1, 0, 4, 6, 8, 3],
    [7, 4, 0, 2, 7, 3],
    [3, 6, 2, 0, 1, 5],
    [4, 8, 7, 1, 0, 3],
    [6, 3, 3, 5, 3, 0]
]
target_index = 2
target_list = 5
target_value = find_lowest_room(original_list[target_list], target_index)
print(target_value)