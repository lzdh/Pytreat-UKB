import fileinput

column_headings = []
counter = 0

output_file=open('process_ukb825.csv','w')

for line in fileinput.input():
	if counter == 0:
		column_headings = line.strip().split(' ')
		counter += 1
		continue
	cells = line.strip().split(' ')
	
	for column_index in range(len(cells)):
		cell = cells[column_index]
		if cell != 'NaN':
		#	output_file.write(str(counter)+','+column_headings[column_index]+','+str(cell)+'\n')
			output_file.write(str(counter)+','+str(column_index)+','+str(cell)+'\n')
	if counter % 10000 == 0:
		print(counter)

	counter += 1

output_file.close()
