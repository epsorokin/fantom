#########################################################
### Search Fantom database for specific gene IDs  #######
### Elena Sorokin								  #######
### 11-11-2015 				     				  #######
#########################################################


'''
Search Fantom database (http://fantom.gsc.riken.jp/) 
for gene records by Entrez ID and report all matching records.

'''
import re
import os
import csv

class Fantom: 

	def __init__(self, GO_id, GO_term, pvalue, entrez_gene_id):

		self.GO_id = GO_id
		self.GO_term = GO_term
		self.pvalue = pvalue
		self.entrez_gene_id = entrez_gene_id
		self.source = f


# Read in entrez filenames from a directory
my_dir = raw_input('Specify path to entrez files (RETURN for default [current dir]) : \n')
if my_dir == '':	
	my_dir = '.'

# Choose an Entrez ID to search for
query = raw_input("Search for Entrez ID (RETURN for default [6469]): \n")
if query == '':
	query = '6469'

contents = os.listdir(my_dir)
contents = [x for x in contents if x.endswith('.entrez')]

# Initialize counter
row_counter = 0
outfile_header = list(["GO_id,", "GO_term", "pvalue", "entrez_gene_id","source_file"])
matches = []
matches.append(outfile_header)

# Enter a name for output file
print str("Default output file name will be: matches_for_entrez" + query + ".csv")
outfile_name = raw_input("Enter output filename (RETURN for default): \n")
if outfile_name == '':
	outfile_name = str("matches_for_entrez" + query + ".csv")

# Loop through entrez files 
for f in contents:
	rows = []
	outfile_header = []

 	with open(f, 'rU') as myfile: 
 		rows = myfile.readlines()
 		outfile_header= rows.pop(0) # Pop off the header 

 		# For each line, make a Fantom instance, and see if it matches 
 		for line in rows:
		
 			curr_entry = Fantom(line.split('\t')[0], line.split('\t')[1], line.split('\t')[2],line.split('\t')[3].split('\n')[0])
 			# Here is the meat of the nested for loop--string match
 			match = []
 			
 			for item in curr_entry.entrez_gene_id.split(';'):

 				#print "On this item:", item
	 			if item == query:
	 				print "...Found a match within:", curr_entry.source, "\n...Here is some info about the match:", curr_entry.GO_id, curr_entry.GO_term

	 				match = [curr_entry.GO_id, curr_entry.GO_term, curr_entry.pvalue, curr_entry.entrez_gene_id, curr_entry.source]
	 				matches.append(match)
	 				row_counter += 1
				else:
					pass
					row_counter += 1

# Just print a nice summary statement to the screen			
print "...SUMMARY:\n...Found", len(matches)-1, "Entrez ID matches within", row_counter, "rows of", len(contents), "files."

# Write all these lovely matches to a CSV file
with open(outfile_name, 'w') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter = ',')
	spamwriter.writerows(matches)