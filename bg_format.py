# NEED A CASE FOR EMPTY LINE [DONE]
# NEED A CASE FOR WHITE SPACES IN LINE [DONE]
# NEED A CASE FOR NOT CAPITALIZED LETTER [DONE]

# NEED A CASE FOR CHEKING IF FOLDER ALREADY EXISTS [DONE]
# NEED A CASE FOR OPTIONAL PARTITION SIZE INPUT [DONE]
# Can concat per line into a text file until a limit is reached 

# command runs under the following template:
# ./bg_format.py <ADM host list> <ADM number> <username> <role/revoke> <optional partition size>
# example: host.txt ADM-1234 sandeeps application

import sys, os, shutil # import libraries

if os.stat(sys.argv[1]).st_size == 0:
    print("\nTerminating, host list is empty")
    exit()
else:
    print("Processing...")

hostname = sys.argv[2].upper() # ADM number 
user_name = " --user " + sys.argv[3].lower() # username
role = " --role " + sys.argv[4].lower() # ADM role / or revoke
partition_size = 50
main_dir = ("./" + hostname) # relative path to temp ADM folder
text = "" # temp reusable variable
host_count = 0
file_count = 1

if sys.argv[4] == 'revoke': # check if it's a revoke request
    role = " --revoke"

if sys.argv[5]: # if partition size is provided
    partition_size = sys.argv[5] # set it instead of the default value


filename = open(sys.argv[1], 'r') # open host list file with read permissions
Lines = filename.readlines() # begin reading 

if not os.path.exists(main_dir): # check if folder for the ADM already exists
    os.makedirs(main_dir) # if not, create one and give it ADM name
    os.chdir(main_dir) # cd into that directory
else:
    shutil.rmtree(main_dir) # if folder with the same ADM number exists, remove it
    os.makedirs(main_dir) # create one and give it ADM name
    os.chdir(main_dir) # cd into that directory
 

for line in Lines: # going through each line, one at a time

    if (line != "\n"): # check if line is empty
        host_count += 1 # increment host count
        line = line.replace(" ", "").upper() # trim space and format to upper case
        text = text+line.strip()+"," # for every line, concatenate a comma 

        if host_count == int(partition_size): # if threshold reached, write out to file and reset host_counter and increment file_counter

            host_count = 0 # reset the counter
            fname = hostname + "_" + str(file_count) # file name
            f = open(fname + ".txt", "x") # create new text file for host list 
            f.write("./breakglass --limit " + text[:-1] + user_name + role) # concat the script inside the file
            f.close()

            text = "" # reset string
            file_count += 1 # incrementing for the naming convention
if (text):
    f = open(hostname + "_" + str(file_count) + ".txt", "x") # create new text file for host list 
    f.write("./breakglass --limit " + text[:-1] + user_name + role) # concat the BG script
    f.close()
    filename.close()
print("Formatting complete")