

# get the most frequency letter of a string
def max_count_letter():
 s = str(input())

 max_frequency = {}

 for i in s:
   if i in max_frequency:
     max_frequency[i] += 1
   else:
     max_frequency[i] = 1

 my_result = max(max_frequency, key=max_frequency.get)

 print(my_result)


max_count_letter()