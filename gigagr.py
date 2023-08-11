import argparse
import multiprocessing
from Bio import SeqIO
import time

def get_delete_regions(gff_file, type_value):
    delete_regions = {}
    print(f"Reading GFF file: {gff_file}")
    with open(gff_file, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.strip().split("\t")
            seqid = fields[0]
            seq_type = fields[2]
            start = int(fields[3])
            end = int(fields[4])
            if seq_type == type_value:
                if seqid not in delete_regions:
                    delete_regions[seqid] = []
                delete_regions[seqid].append((start, end))
    print("Finished processing GFF file and obtained delete regions.")
    return delete_regions

def process_and_write_record(record, delete_regions, output_file):
    seqid = record.id
    seq = record.seq
    print(f"Processing sequence {seqid}")

    if seqid in delete_regions:
        delete_regions[seqid].sort()
        new_seq = ""
        pointer = 0
        deleted_region_count = 0
        for start, end in delete_regions[seqid]:
            new_seq += seq[pointer:start - 1]
            pointer = end
            deleted_region_count += 1
            if deleted_region_count % 100000 == 0:
                print(f"Deleted {deleted_region_count} regions in sequence {seqid}")

        new_seq += seq[pointer:]
        new_record = record[:]
        new_record.seq = new_seq
        with open(output_file, "a") as f:
            SeqIO.write(new_record, f, "fasta")
    else:
        with open(output_file, "a") as f:
            SeqIO.write(record, f, "fasta")
    
    print(f"Finished processing and writing sequence {seqid}")

def process_records(records, delete_regions, output_file):
    for record in records:
        process_and_write_record(record, delete_regions, output_file)

def main():
    parser = argparse.ArgumentParser(description="Delete sequences from a genome file based on a gff file and a type value")
    parser.add_argument("-genome", "-g", help="genome file path", required=True)
    parser.add_argument("-gff", "-f", help="gff file path", required=True)
    parser.add_argument("-output", "-o", help="output file path", default="output.fasta")
    parser.add_argument("-type", "-t", help="type value to delete", default="gene")
    parser.add_argument("-threads", "-n", help="number of threads to use", type=int, default=1)
    args = parser.parse_args()

    genome_file = args.genome
    gff_file = args.gff
    output_file = args.output
    type_value = args.type
    num_threads = args.threads

    delete_regions = get_delete_regions(gff_file, type_value)
    print("Finished reading GFF file.")

    with open(output_file, "w") as f:
        pass

    with open(genome_file, "r") as genome_f:
        genome_records = list(SeqIO.parse(genome_f, "fasta"))

    chunk_size = len(genome_records) // num_threads
    chunks = [genome_records[i:i+chunk_size] for i in range(0, len(genome_records), chunk_size)]

    processes = []
    for chunk in chunks:
        process = multiprocessing.Process(target=process_records, args=(chunk, delete_regions, output_file))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    print("Program completed.")

if __name__ == "__main__":
    main()
