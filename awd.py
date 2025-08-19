input_file = "input.csv"
# Output CSV file
output_file = "output.csv"

with open(input_file, newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    for row in reader:
        new_row = []
        temp = []
        for val in row:
            # if the value is a comma inside quotes, it marks a separator
            if val == ',':
                if temp:
                    new_row.append(''.join(temp))  # join collected chars
                    temp = []
            elif val != '':  # ignore empty strings
                temp.append(val)
        # append any remaining chars
        if temp:
            new_row.append(''.join(temp))
        writer.writerow(new_row)
