

def remap(val, old_min, old_max, new_min, new_max):
    'remaps val from old range to new range'
    return (new_max - new_min)*(val - old_min) / (old_max - old_min) + new_min

def clamp(val, _min, _max):
    'clamps value in the range _min and _max'
    return min(max(val,_min),_max)