import math
''' '''


def num_digits(num):
    if num > 0:
        return int(math.log10(num))+1
    elif num == 0:
        return 1
    else:
        return int(math.log10(-num))+2  # +1 if you don't count the '-'


def bucket_sort_unsigned_ints(array):
    # Step 1: Create buckets

    # Ok so we are sorting ints so we know that every digit place can be one of
    # ten options (0-9) so we will create 10 buckets
    # Each bucket index will represent a digit value.  IE : index 0 will represent
    # the digit 0 and index 1 will represent the digit 1.

    # A bucket in our situation will just be an array.
    bucket_arr = []
    for i in range(0, 10):
        bucket_arr.append([])

    largest_value = -1
    for item in array:
        if item > largest_value:
            largest_value = item

    # Start with at least one int.  Also handles case where 0 is the max int
    max_digits = num_digits(largest_value)

    # Step 2: 'Scatter' - Go over the original array, putting objects into buckets
    for num in array:
        most_sig_digit = num // math.pow(10, max_digits - 1)
        bucket_arr[int(most_sig_digit)].append(num)


    # Step 3: Sort each non-empty bucket (using bucket_sort)
    for bucket in bucket_arr:
        bucket_len = len(bucket)
        if bucket_len > len(array) / 3:  # If it is > 33% bucket sort that
            bucket = bucket_sort_unsigned_ints(bucket)
        elif len(bucket) != 0:
            bucket.sort()

    # Step 4: 'Gather' - Visit the buckets in order and put all elements back into the original array
    index = 0
    for bucket in bucket_arr:
        for num in bucket:
            array[index] = num
            index += 1
    return array


test_arr = [0,1,2,3,2,5,6,12,13,14,123]
print(bucket_sort_unsigned_ints(test_arr))
