#use these four global variables to set the directories for your data and output files for each
#phase.  P.S.  Don't tell Dr Fagin I'm using global variables.  I distinctly remember him telling
#me not to while standing on a soap box in CS210
P1_data_path=".\\data\\"
P1_soln_path=".\\data\\soln\\"
P2_data_path=".\\P2data\\"
P2_soln_path=".\\P2data\\soln\\"

#This function reads a priorities CSV file and returns the priorities in a single data structure
#as follows:  The top level data structure is a dictionary with two entries.  Each entry is
#indexed by a string that also serves as the prefix for each entity to be paired.  For example,
#when reading size_6_priorities.csv, the two top level keys are 'B' (for blue) and 'R' (for red).
#The values stored in the top level dictionary are two more dictionaries.  This lower level
#dictionary is indexed by an entity name (e.g. 'B3' or 'R2' from size_6_priorities.csv).  The
#lower level dictionary values are lists that indicate priorities from most desired to least
#desired.  For example, calling priorities['B']['B3'][1] would return 'R2' indicating that R2
#is B3's second choice mate.
def read_priorities(csv_filepath):
    priorities={}
    file=open(csv_filepath,"r")
    lines=file.read().split("\n")
    for line in lines:
        if line:
            tokens=line.split(",")
            label=tokens[0].strip(':')
            row_priorities=[]
            for token in tokens[1:]:
                if token.strip()!="":
                    row_priorities.append(token.strip())
            if label[0] in priorities:
                priorities[label[0]][label]=row_priorities
            else:
                priorities[label[0]]={}
                priorities[label[0]][label]=row_priorities
    file.close()
    return priorities

#This function prints a priorities structure from a file to the console.
def show_priorities(csv_path):
    priorities=read_priorities(csv_path)
    for key in priorities:
        for row in priorities[key]:
            print(row,end=": ")
            for col in priorities[key][row]:
                print(col,end=", ")
            print("")
        print("")
    return 0

#This funciton reads a set of parings from a CSV file and returns a dictionary as described:
#The entities that were designated as boys during pairing are used as the keys in the
#dictionary.  The values that are stored are the entities that the boys ended up paired to.
#For example, after reading size_6_pairings_0.csv, pairs['B2'] would return 'R4' indicating
#B2 was paired with R4.
def read_pairs(csv_filename):
    pairs={}
    file=open(csv_filename,"r")
    lines=file.read().split("\n")
    for line in lines:
        if line:
            tokens=line.split(",")
            label=tokens[0].strip(": ")
            pairs[label]=tokens[1]
    file.close()
    return pairs

#This function writes a pairs structure (as defined in the comment for read_pairs() to a CSV
#at the filepath given as a parameter.
def write_pairs(csv_filename,pairs):
    of=open(csv_filename,"w")
    for boy in pairs:
        of.write(boy)
        of.write(": ,")
        of.write(pairs[boy])
        of.write("\n")
    of.close()
    return 0

#this is where you will test whether a set of proposed pairings are stable or not.  It should
#return a set of touples.  Each touple represents a rogue pairing.  A stable pairing should
#return an empty set.
def find_rogues(pairs_filename, priorities_filename):
    #TODO: identify rogue pairings
    outputfile = open("roguepairings.txt", "w")
    pairs = read_pairs(pairs_filename)
    priorities = read_priorities(priorities_filename)

    show_priorities(pairs_filename)
    show_priorities(priorities_filename)
    
    length = len(priorities['B'])

    counter = 0

    for i in range(length):
    
        blueIndex = 0
        currentBPair = pairs['B' + str(i)]
        while priorities['B']['B' + str(i)][blueIndex] != currentBPair:
            blueIndex += 1
        print('\n')
        print('priority B',i ,':', blueIndex)

        for j in range(0 , blueIndex):
            redIndex = 0
            rblueIndex = 0
            currentR = priorities['B']['B' + str(i)][j]
            while priorities['R'][currentR][redIndex] != 'B' + str(i):
                redIndex += 1

            # print(currentR, 'priority for B' + str(i) ,':', redIndex)

            for k in range(length):
                if (pairs['B' + str(k)] == currentR):
                    while priorities['R'][currentR][rblueIndex] != 'B' + str(k):
                        rblueIndex += 1
                    # print(currentR, 'priority for Current Pair B' + str(k) ,':', rblueIndex)

                    # print('B' + str(k),'Difference in value =', (redIndex - rblueIndex))
                    if (redIndex - rblueIndex < 0):
                        print(currentR, 'and', 'B' + str(i), 'are a rogue pair')
                        outputfile.write('B' + str(i))
                        outputfile.write(' and ')
                        outputfile.write(currentR)
                        outputfile.write(' are a rogue pair')
                        outputfile.write('\n')
                        counter+=1

        # print('\n')
    
    print(counter)
    if (counter == 0):
        outputfile.write('stable')
    return 0

#This is where you need to implement the Gale-Shapley algorithm on a set of priorities defined
#in a CSV file located by the csv_path parameter.  boy_set_label and girl_set_label are strings
#used to label the boy set and the girl set.  Each label are also used as a prefix for each
#individual boy and girl.  Boys propose to girls and girls reject boys as described in the
#assigned videos.  This function should return a dictionary where the indexes are the boys
#and the values are the girls.
def pair(csv_path,boy_set_label,girl_set_label):
    #TODO: implement the Gale-Shapley algorithm
    priorities = read_priorities("size_6_priorities.csv")
    show_priorities("size_6_priorities.csv")
    length = len(priorities['B'])

    matched_pairs = {}
    temp_list_girl = []
    temp_list_boy = []
    counter = 0
    while (len(matched_pairs) < length):
        boy = 'B' + str(counter)
        boypref = priorities['B'][boy]
        girl = priorities['B'][boy][0]
        girlpref = priorities['R'][girl]
        if not (girl in temp_list_girl):
            temp_list_girl.append(girl)
            temp_list_boy.append(boy)
        else:
            rank = 0
        counter+=1
        if counter == 2:
            break


    return 0

#This function should test Hall's conditions on a graph defined in a priorities CSV file.  It
#will ensure that all members of the boys set can be paired to a girl from the girls set.  It
#makes no guarantees that all girls can be paired to a boy.  I wrote it to return "pass" or
#"fail" as strings.
def test_halls(priorities_filename,boy_set_label,girl_set_label):
    #This helper function generates and returns the powerset of the input collection (with the
    #exception of null set).
    #source: https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
    def powerset(iterable):
        from itertools import chain, combinations
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1))
    #TODO: test Hall's condition
    return 0

#This is the main program.  It has code to loop through all files provided.  My suggestion is that
#you only use it once you have all the funcitons working, or at least all the code for one of the
#three tasks.  (Commenting out an entire block at a time may makes sense.)  Use the test()
#function as your main program as you're developing and debugging.
def main():
    #find rogue pairs for each proposed
    for size in (6,10,25,100):
        for pairing in(0,1,2,3):
            rogues=find_rogues(P1_data_path+"size_"+str(size)+"_parings_"+str(pairing)+".csv", P1_data_path+"size_"+str(size)+"_priorities.csv")
            of=open(P1_soln_path+"size_"+str(size)+"_rogues_"+str(pairing)+".txt","w")
            of.write(str(rogues))
            of.close()
    
    #generate the blue and red optimal solutions for each
    for size in (6,10,25,100):
        priorities_filename=P1_data_path+"size_"+str(size)+"_priorities.csv"
        pairs=pair(priorities_filename,'B','R')
        write_pairs(P1_soln_path+"size_"+str(size)+"_B-R_soln.csv",pairs)
        pairs=pair(priorities_filename,'R','B')
        write_pairs(P1_soln_path+"size_"+str(size)+"_R-B_soln.csv",pairs)
    
    #test Hall's Condition for each
    for size in (6,10,20):
        for file in range(1,5):
            print("size "+str(size)+" file "+str(file),end=": ")
            halls_result=test_halls(P2_data_path+"size"+str(size)+"-"+str(file)+".txt",'B','R')
            print(halls_result)
    return 0

#As stated in the comment for main(), I suggest you use this as the main program while you're
#developing and debugging.
def test():
    filepairings = "size_10_parings_2.csv"
    filepriorities = "size_10_priorities.csv"
    find_rogues(filepairings, filepriorities)
    return 0

#Here's where main() and/or test() gets executed when you run this script.
#main()
test()
