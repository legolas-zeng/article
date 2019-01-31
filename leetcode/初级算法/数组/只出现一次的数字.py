# coding=utf-8
'''
给定一个非空整数数组，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素。
说明：
你的算法应该具有线性时间复杂度。 你可以不使用额外空间来实现吗？
输入: [4,1,2,1,2]
输出: 4
'''
'''
把全部元素放进set里面，然后有重复的元素就马上剔除，最后能得到结果，时间复杂度O(n),空间复杂度O(n)
'''
nums = [4,1,2,1,2]
d = set()
for i in range(0,len(nums)):
    if nums[i] not in d:
        d.add(nums[i])
    else:
        d.remove(nums[i])
print(d)


