# coding=utf-8
# @author: zenganiu
# @time: 2019/2/16 17:45

'''
给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。
输入: [0,1,0,3,12]
输出: [1,3,12,0,0]

说明:

必须在原数组上操作，不能拷贝额外的数组。
尽量减少操作次数。
'''

nums = [0,0,1]
for index,values in enumerate(nums):
    print(values)
    if values == 0:
        nums.pop(index)
        nums.append(0)
print(nums)
