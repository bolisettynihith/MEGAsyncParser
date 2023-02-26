#----------------------------
# Author: Nihith (https://solo.to/g4rud4)
# Version: 1.0
#----------------------------

import argparse
import sqlite3
import csv
import os

def get_MEGAcloudFiles(cursor):
    print("[+] Extracting the Files Present in MEGA Cloud!")

# mimetype == 0 -> Folder/Archive(7z,zip)
# mimetype == 1 -> JPG/PNG
# mimetype == 2 -> wav (Audio files)
# mimetype == 4 -> PDF/TXT

# node is a blob data, seems to be a protobuf data.

    cursor.execute('''
        SELECT
            datetime(ctime,'unixepoch') AS "Uploaded Time",
            name,
            size,
            CASE
                WHEN type == 0 THEN "File"
                WHEN type == 1 THEN "Folder"
                Else type
            END AS "File Type",
            CASE
                WHEN mimetype == 0 THEN "Folder/Archive"
                WHEN mimetype == 1 THEN "Image Files (JPG/PNG)"
                WHEN mimetype == 2 THEN "Audio Files"
                WHEN mimetype == 4 THEN "PDF/Text Files"
                ELSE mimetype
            END AS "MIME type",
            nodehandle,
            parenthandle,
            node
        FROM
            nodes;
    ''')

    all_rows = cursor.fetchall()
    return all_rows

def generateCSV(results, output_folder):
    '''
    Generates CSV Reports
    '''
    # If output folder exists then proceeds in report generation,
    # else creates the output folder and starts the report generation.
    # If output folder argument is not set then default folder is
    # created in the path script was run.

    if(os.path.exists(output_folder)):
        pass
    elif(output_folder == 'Reports'):
        print(f"[+] Output folder does not exist. Creating the '{output_folder}' folder.\n")
        os.mkdir(output_folder)
    else:
        print("[+] Output Folder doesn't exist!")

    output = os.path.join(os.path.abspath(output_folder), 'MEGAsync_CloudFiles.csv')

    # Creating CSV file
    out = open(output, 'w', encoding="utf-8")
    csv_out = csv.writer(out, lineterminator='\n')

    csv_out.writerow(['Uploaded Time', 'File Name', 'File/Folder Size', 'File Type', 'MIME Type', 'Node Handle', 'Parent Handle', 'Node(RAW, Protobuf data)'])
    for row in results:
        csv_out.writerow(row)

    # Checking if the CSV report generated or not
    if(os.path.exists(output)):
        print(f"[+] Report Successfully generated and saved to {os.path.abspath(output)}")
    else:
        print('[+] Report generation Failed')

def MEGAsyncParser(input_db, output_folder):
    file_in = str(input_db)
    db = sqlite3.connect(file_in)
    cursor = db.cursor()

    cloudFiles = get_MEGAcloudFiles(cursor)

    if(len(cloudFiles) > 0):
        generateCSV(cloudFiles, output_folder)
    else:
        print("[+] No data found in Mega Database")

    db.close()

def main():
    parser = argparse.ArgumentParser(description="MEGAsync Database Parser")
    parser.add_argument('-f', '--input_file', required=True, action="store", help="Path to megaclient_statecache13_<RANDOM 36 chars>.db")
    parser.add_argument('-o', '--output_folder', required=False, action="store", help="Path to the parsed CSV file")

    args = parser.parse_args()
    in_file = args.input_file
    out_folder = args.output_folder

    # Checking if output folder is current folder or No output folder
    if (os.path.exists(in_file) and (out_folder == None or (os.path.abspath(out_folder) == os.getcwd()))):
        MEGAsyncParser(in_file, 'Reports')
    elif(os.path.exists(in_file) and os.path.exists(out_folder)):
        MEGAsyncParser(in_file, out_folder)
    elif(not (os.path.exists(out_folder))):
        print('[+] Output path does not exist.')
    else:
        print(parser.print_help())

if __name__ == '__main__':
    main()