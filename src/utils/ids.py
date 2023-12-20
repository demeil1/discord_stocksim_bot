import random

def getTransacId():

    random.seed()
    id_len = 16
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nums = "0123456789"
    t_id = ""
    for i in range(id_len):
        rand_int = random.randint(1,3)
        if rand_int == 1 :
            num_ind = random.randint(0, len(nums) - 1)
            t_id += nums[num_ind]
        else: 
            char_ind = random.randint(0, len(chars) - 1)
            t_id += chars[char_ind]

    return t_id
