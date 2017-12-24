# Sublime Lines - Multisets
This Sublime Text plugin allows you to compare, merge and manipulate lists of things,
whether they are todo items, lists of files or arrays from API responses:
![Demo - comparing a giveaway list with two wishlists](https://github.com/heldev/sublime-lines-multisets/raw/master/demo-giveaway-list.gif)

## How to use
Switch to a file with a list you want to modify and select an operation to perform from the Command Palette
(or using `Edit -> Lines - Multisets` menu).
## Operations
### Add
The result is all items from both lists. Example:

List 1 | List 2 
-------|-------
one | two
three | three
four | four
four |

Result: one, two, three, three, four, four, four

### [Union](https://en.wikipedia.org/wiki/Set_(mathematics)#Unions)
The result is items from both lists, but only one item for every match. Example:

List 1 | List 2 | Match 
-------|--------|------
one | two |
three | three | :heavy_check_mark:
four | four | :heavy_check_mark:
four |  |

Result: one, two, three, four, four

### [Intersection](https://en.wikipedia.org/wiki/Set_(mathematics)#Intersections)
The result is only items that exist in both lists. Example:

List 1 | List 2 | Match | Result
-------|--------|-------|-------
one | two | |
three | three | :heavy_check_mark: | three
four | four | :heavy_check_mark: | four
four | five | |
five | five | :heavy_check_mark: | five
five | five | :heavy_check_mark: | five

### [Difference](https://en.wikipedia.org/wiki/Complement_(set_theory))
The result is items from list 1 that don't have a match in list 2. Example:

List 1 | List 2 | Match | Result
-------|--------|-------|-------
one | two | | one
three | three | :heavy_check_mark: |
four | four | :heavy_check_mark: | 
four | five | | four
five | five | :heavy_check_mark: |
five | five | :heavy_check_mark: |

### [Symmetric difference](https://en.wikipedia.org/wiki/Symmetric_difference)
The result is items that exist in only one of the lists. Example:

List 1 | List 2 | Match 
-------|--------|------
one | two |
three | three | :heavy_check_mark:
four | four | :heavy_check_mark:
four | five | 
five | five | :heavy_check_mark:
five | five | :heavy_check_mark:

Result: one, two, four, five
