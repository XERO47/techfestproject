import sys
sys.path.append('src')


def alert(min_temp,max_temp,actual_temp):
    if(min_temp<actual_temp<max_temp):
        return False
    else:
        return True

alert=alert(12,20,21)