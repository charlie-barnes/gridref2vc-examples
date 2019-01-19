import csv
import sys

tetrad_suffix = [["A","A","B","B","C","C","D","D","E","E"],
                 ["A","A","B","B","C","C","D","D","E","E"],
                 ["F","F","G","G","H","H","I","I","J","J"],
                 ["F","F","G","G","H","H","I","I","J","J"],
                 ["K","K","L","L","M","M","N","N","P","P"],
                 ["K","K","L","L","M","M","N","N","P","P"],
                 ["Q","Q","R","R","S","S","T","T","U","U"],
                 ["Q","Q","R","R","S","S","T","T","U","U"],
                 ["V","V","W","W","X","X","Y","Y","Z","Z"],
                 ["V","V","W","W","X","X","Y","Y","Z","Z"]]     
                        
data = {}

# read the csv into a dict
with open('./data/all.csv', 'rb') as f:
    reader = csv.reader(f)

    for row in reader:
        data[row[0]] = row[1]
                  
def vc(grid):      
               
    grid = grid.upper()

    # If the grid reference is in the data just return the relevant vc(s), if
    # not then try each parent grid in turn until we find the one that exists.
    
    try:
        return data[grid]
    except KeyError:
    
        # get the prefix
        if grid[1:2].isalpha():
            prefix = grid[0:2]
            grid = grid[2:]
        else:
            prefix = grid[0:1]
            grid = grid[1:]
       
        try:
            # create a 1m grid reference if we can and test
            if len(grid) >= 10:
                test = prefix + grid[0:5] + grid[(len(grid)/2):(len(grid)/2)+5]
            return data[test]
        except (NameError, KeyError):
            try:
                # create a 10m grid reference if we can and test
                if len(grid) >= 8:
                    test = prefix + grid[0:4] + grid[(len(grid)/2):(len(grid)/2)+4]
                return data[test]
            except (NameError, KeyError):
                try:
                    # create a 100m grid reference if we can and test
                    if len(grid) >= 6:
                        test = prefix + grid[0:3] + grid[(len(grid)/2):(len(grid)/2)+3]
                    return data[test]
                except (NameError, KeyError):
                    try:
                        # create a 1km grid reference if we can and test
                        # (we can't create a 1km from a 5km grid reference)
                        if len(grid) >= 4 and grid[-2:] not in ('NE', 'NW', 'SE', 'SW'):
                            test = prefix + grid[0:2] + grid[(len(grid)/2):(len(grid)/2)+2]
                        
                        return data[test]
                    except (NameError, KeyError):  
                        try:
                            # create a 2km grid reference if we can and test
                            # (if we've been given a 2km grid reference then just
                            # test that; we know it will raise an error having got
                            # this far)
                            # (we can't create a 2km from a 5km grid reference)
                            if len(grid) == 3 and grid[-1:].isalpha():
                                test = grid
                            elif len(grid) >= 3 and grid[-2:] not in ('NE', 'NW', 'SE', 'SW'):
                                test = prefix + grid[0:1] + grid[(len(grid)/2):(len(grid)/2)+1] + tetrad_suffix[int(grid[1:2])][int(grid[(len(grid)/2)+1:(len(grid)/2)+2])]
                                
                            return data[test]
                        except (NameError, KeyError):         
                            try:
                                # create a 10km grid reference if we can and test
                                # (asutute readers will notice we don't try and
                                # create a 5km grid reference at this point.
                                # this is because 5km grid references aren't included
                                # in the parentage hierachy as they cross odd-numbered
                                # boundaries and therefore don't fully encompass child
                                # grid references.)
                                if len(grid) >= 2:
                                    # if we've been given a 5km grid reference
                                    # strip the pentad
                                    if grid[-2:] in ('NE', 'NW', 'SE', 'SW'): 
                                        grid = grid[:-2] 
                                    test = prefix + grid[0:1] + grid[(len(grid)/2):(len(grid)/2)+1]

                                return data[test]
                            except (NameError, KeyError):        
                                try:
                                    # create a 100km grid reference if we can and test
                                    if len(grid) >= 0:
                                        # if we've been given a 5km grid reference
                                        # stip the pentad
                                        if grid[-2:] in ('NE', 'NW', 'SE', 'SW'): 
                                            grid = grid[:-2] 
                                        test = prefix
                                    return data[test]
                                except (NameError, KeyError):        
                                    return None
                                       
if __name__ == '__main__':
    print vc(sys.argv[1])
