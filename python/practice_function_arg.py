korean, english, mathematics, science = 100, 86, 81, 91
 
def get_max_score(*args):                                   
   #args = [korean, english, mathematics, science]
    for arg in args:
        # max_score = args[0]
        # max_score = arg if arg > max_score else max_score
        max_score = max(args)
    return max_score
                                             
max_score = get_max_score(korean, english, mathematics, science)
print('높은 점수:', max_score)
 
max_score = get_max_score(english, science)
print('높은 점수:', max_score)