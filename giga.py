import sys
import argparse
import threading
from Bio import SeqIO
from queue import Queue, Empty

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
    print("Finished processing GFF file.")
    return delete_regions

def process_and_write_record(record, delete_regions, output_file, write_lock):
    seqid = record.id
    seq = record.seq
    print(f"Processing and writing sequence {seqid}")
    
    if seqid in delete_regions:
        delete_regions[seqid].sort()
        new_seq = ""
        pointer = 0
        for start, end in delete_regions[seqid]:
            new_seq += seq[pointer:start - 1]
            pointer = end
        new_seq += seq[pointer:]
        new_record = record[:]
        new_record.seq = new_seq
    else:
        new_record = record
    
    with open(output_file, "a") as f:
        with write_lock:
            SeqIO.write(new_record, f, "fasta")
    
    print(f"Finished processing and writing sequence {seqid}")

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

    print("Reading genome file...")
    delete_regions = get_delete_regions(gff_file, type_value)
    print("Finished reading genome file and GFF file.")
    
    with open(output_file, "w") as f:
        pass

    write_lock = threading.Lock()

    print(f"Processing genome using {num_threads} threads and writing output to file...")
    for record in SeqIO.parse(genome_file, "fasta"):
        thread = threading.Thread(target=process_and_write_record, args=(record, delete_regions, output_file, write_lock))
        thread.start()
    
    print("Waiting for all threads to complete...")
    main_thread = threading.currentThread()
    for thread in threading.enumerate():
        if thread is not main_thread:
            thread.join()

    print("Program completed.")

if __name__ == "__main__":
    main()
