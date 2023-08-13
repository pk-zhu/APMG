import argparse

parser = argparse.ArgumentParser(description="Process GFF3 file")
parser.add_argument("-i", "--input", required=True, help="Input GFF3 file")
parser.add_argument("-o", "--output", required=True, help="Output file for processed content")
args = parser.parse_args()

with open(args.input, "r") as f:
    lines = f.readlines()

new_lines = []

for line in lines:
    line = line.strip()
    if not line or line.startswith("###"):
        continue
    
    fields = line.split("\t")
    
    # Check if there are enough fields and the score column (index 5) is present
    if len(fields) >= 9 and len(fields) >= 6:
        try:
            score = float(fields[5])
            if score < 85:
                continue
        except ValueError:
            pass
    
        fields[1] = "gmap"
        attributes = fields[-1]
        attributes = attributes.split(";")
        new_attributes = []
        for attribute in attributes:
            if attribute.startswith("ID=") or attribute.startswith("Parent="):
                new_attributes.append(attribute)
        new_attributes = ";".join(new_attributes)
        fields[-1] = new_attributes
        
    new_line = "\t".join(fields)
    new_line = new_line.replace(".path1", "")
    
    if "mrna" in new_line:
        new_line = new_line.replace("mrna", "")
    
    new_lines.append(new_line)

with open(args.output, "w") as f:
    for line in new_lines:
        f.write(line + "\n")
