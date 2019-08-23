import os
def returnPath(string, switch):
    # Purpose:  break a file path into either a path string or a file string
    position = string.rfind(os.sep)
    if switch:
        return string[position + 1:] 
    else:
        return string[:position]

x = 'C:/bae/job/xmap.txt'
print(returnPath(x,True))
print(returnPath(x,False))