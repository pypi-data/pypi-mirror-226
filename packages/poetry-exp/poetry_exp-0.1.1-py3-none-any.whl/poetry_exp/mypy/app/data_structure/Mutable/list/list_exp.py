#http://www.sanfoundry.com/python-programming-questions-answers/
#http://www.sanfoundry.com/1000-python-questions-answers/

import random

list1= list()
print list1 #[]

list2=[]
print list2 #[]

list3= list([1,2,3])
print list3 #[1,2,3]

list4 = [1,2,3]
print list4 #[1,2,3]


print list("Hello") #['H', 'e', 'l', 'l', 'o']

list5= ['h','e','l','l','o']
print len(list5) #5


list6=[2445,133,12454,123]
print max(list6) #12454
print min(list6) #123

list7=[1,2,3]
print sum(list7) #6

random.shuffle(list7)
print list7 #random.shuffle(list7)  , it can varry


list1 =  [4, 2, 2, 4, 5, 2, 1, 0]
print(list1[0]) #4
print(list1[:2]) # [4,2]
print(list1[:-2]) #[4,2,2,4,5,2]
print(list1[4:6]) #[5,2]
print(list1[-1]) #0
print(list1[:-1]) #[4,2,2,4,5,2,1]


names = ['Amir', 'Bear', 'Charlton', 'Daman']
print names[-1][-1] #n

list8 = [1, 3, 2]
print list8*2 #[1, 3, 2, 1, 3, 2]

list9 = [0.5 * x for x in range(0, 4)]  #exclude 4
print list9 #[0.0,0.5,1.0,1.5]


list10 = [11, 2, 23]
list11= [11, 2, 23]
print list10<list11 #False, :Elements are compared one by one.


list10 = [11, 2, 22]
list11= [11, 2, 23]
print list10<list11 #True, :Elements are compared one by one.


# append to add an element to the list. 

#insert To add element to list in a specific position
list13 = [1,2,3]
print "Insert demo"
print list13.insert(1,10) # None
print list13 #[1,10,2,3]
#list13.insert(30)  #TypeError: insert() takes exactly 2 arguments (1 given)


list14=["Hello","world"]
print list14.remove("Hello")  #None
print list14 #['world']

list15 =  [3, 4, 5, 20, 5]
print list15.index(5) #2

"""
>>>help(list.index)
index(...)
    L.index(value, [start, [stop]]) -> integer -- return first index of value.
    Raises ValueError if the value is not present.
"""

print list15.count(5) #2
print list15.reverse() #None
print list15 #[5,20,5,4,3]

list16=[1,2,3]
print list16.extend([4,5]) # None
print list16 # [1,2,3,4,5]

#pop() removes the element at the position specified in the parameter. 

print list16.pop(1) #2, returns the element that removed
print list16 #[1,3,4,5]


print list16.pop() #5, pop() by default will remove the last element.
print list16 #[1,3,4]

print "Welcome to Python".split() # ['Welcome' 'to' 'Python']

print list("a#b#c#d".split('#')) #['a','b','c','d']


myList = [1, 5, 5, 5, 5, 1]
max = myList[0]
indexOfMax = 0
for i in range(1, len(myList)):
    if myList[i] > max:
        max = myList[i]
        indexOfMax = i     
print(indexOfMax) #1


list1 = [1, 3]
list2 = list1
list1[0] = 4 # update the element, not shift
print(list2) #[4,3]


def f(values):
    values[0] = 44 

v = [1, 2, 3]
f(v)
print(v) #[44,2,3]


myList2 = [1, 2, 3, 4, 5, 6]
for i in range(1, 6):
    myList2[i - 1] = myList2[i] 
for i in range(0, 6): 
    print myList2[i]


list = ['a', 'b', 'c', 'd', 'e']
print list[10:]  # []

"""
attempting to access a slice of a list at a starting index that exceeds the number of members in the list
 will not result in an IndexError and will simply return an empty list.

What makes this a particularly nasty gotcha is that it can lead to bugs that are really hard to track down
 since no error is raised at runtime.
"""


list = [[ ]] * 5
print list
list[0].append(10)
print list
list[1].append(20)
print list
list.append(30)
print list

"""
[[], [], [], [], []]
[[10], [10], [10], [10], [10]]
[[10, 20], [10, 20], [10, 20], [10, 20], [10, 20]]
[[10, 20], [10, 20], [10, 20], [10, 20], [10, 20], 30]

 the key thing to understand here is that the statement list = [ [ ] ] * 5 does NOT create a list
  containing 5 distinct lists; rather, it creates a a list of 5 references to the same list.
   With this understanding, we can better understand the rest of the output.

list[0].append(10) appends 10 to the first list. But since all 5 lists refer to the same list,
 the output is: [[10], [10], [10], [10], [10]].

Similarly, list[1].append(20) appends 20 to the second list. But again, since all 5 lists refer to the same list,
 the output is now: [[10, 20], [10, 20], [10, 20], [10, 20], [10, 20]].

In contrast, list.append(30) is appending an entirely new element to the outer list,
 which therefore yields the output: [[10, 20], [10, 20], [10, 20], [10, 20], [10, 20], 30].
"""