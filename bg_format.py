# Format: <hostname file> <ADM number> <ADM users> <ADM role or revoke> <partition size>

# Need to work on multiple users.
# What do you do with the folder after the script was executed? Maybe create only one txt file with partitions separated
# in paragraphs? Also this file can be emailed to the user for conveniece?
# Need to check how openning excel files is different from txt files.

import os, shutil # import libraries


### Variables ###

adm_hostname = input("Enter host list filename: ") 
adm_num = input("Enter ADM number: ")
adm_users = input("Enter usernames: ")
adm_role = " --" + input("Enter ADM role: ")
partition = input("Enter preferred partition size: ")

script_user = os.getlogin() # username of the user executing the script
script_dir = ("./" + adm_num + "_" + script_user) # relative path to the temp ADM folder
host_count = 0 # host counter
file_count = 1 # partition counter
text = "" # temp string variable

### Script start conditions check ###   

if not adm_hostname:
    print("No host file selected. \nTerminating...")
else:
    print("Processing...")
    
if not partition:
    adm_partition = 30
else:
    adm_partition = int(partition)

### Opening the host file ###
 
hostname = open(adm_hostname, 'r') # open host list file with read permissions

### Creating temp folder ###
    
if not os.path.exists(script_dir): # check if folder for the ADM already exists
    os.makedirs(script_dir) # if not, create one and give it ADM name
    os.chdir(script_dir) # cd into that directory
else:
    shutil.rmtree(script_dir) # if folder with the same ADM number exists, remove it
    os.makedirs(script_dir) # create one and give it ADM name
    os.chdir(script_dir) # cd into that directory

### Iterating through the host file ###
       
host_list = hostname.readlines() # begin reading the lines 

for line in host_list:
    if (line != "\n"): # check if line is empty
        host_count += 1 # increment host count
        line = line.replace(" ", "").upper() # trim space and format to upper case
        text = text+line.strip()+"," # for every host, concatenate a comma 

        if host_count == int(adm_partition): # if threshold reached, write out to file and reset host_counter and increment file_counter

            host_count = 0 # reset the counter
            f = open(adm_num + "_" + str(file_count) + ".txt", "x") 
            f.write("./breakglass --limit " + text[:-1] + adm_users + adm_role) # concat the script inside the file
            f.close()

            text = "" # reset temp string
            file_count += 1 # incrementing for partition naming convention
if (text):
    f = open(adm_num + "_" + str(file_count) + ".txt", "x") # create new text file for host list 
    f.write("./breakglass --limit " + text[:-1] + adm_users + adm_role) # concat the BG script
    f.close()

hostname.close()

print(str(file_count - 1) + " partitions were created \nFormatting complete")


    
