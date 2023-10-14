import os
import json
import pandas as pd

"""

https://www.upwork.com/jobs/~01ab12fc34bbc35c50

There are 25 zipped sample data files each representing a particular year that contains XML code.  
The XML code is consistent within each file but varies over the years of files.  
Each zipped  file contains about 4000 XML files that are concatenated together to make up 1 file.  

1. Group the individual files with the same xml code together in a directory and 
2. write python code that will unzip these similar files into a data directory and 
3. pull two pieces of data from the files and store in a dataframe:  
   
   - application year
   - application number
   
   There will be an application year (based on the application date (yearmonthday) (not unique) and a 
   unique application number for each of the 4000 entries in 1 file so pull all 
   application years and application numbers within each file. The XML identifying field code has changed over the 
   years though not every year.  
   
4. Save the dataframe into an excel file csv or tsv. 
   There is likely 4-7 various XML code variations over the years.  
   See example file attached. 
   What I request from potential programmers is a projected cost and deliverable date including the number hours you 
   see the task taking and your hourly rate or fixed rate.

"""
verbose = False
data_folder = "data"
xml_input_folder = os.path.join(data_folder, "01_xml_src")
xml_output_folder = os.path.join(data_folder, "02_xml_dst")
os.makedirs(data_folder, exist_ok=True)
os.makedirs(xml_input_folder, exist_ok=True)
os.makedirs(xml_output_folder, exist_ok=True)


def parse_xml_data(input_file_name, xml_content_data):

    xml_type_folder = os.path.join(data_folder, "02_xml_dst", input_file_name, "xml_files")
    os.makedirs(xml_type_folder, exist_ok=True)

    data_map = []
    keep_line = False
    last_line = False
    new_xml_contents = ""
    x = 0
    for line in xml_content_data.split("\n"):

        if line.__contains__("<?xml version"):
            x += 1
            keep_line = True

        elif line.lower().__contains__("</patent-application-publication>"):
            last_line = True

        if keep_line:
            new_xml_contents += line + "\n"

        if last_line:
            last_line = False

            end_parse = False
            next_number = 0
            document_date = None
            doc_date = None
            document_number = None
            doc_num = None
            z = 0
            for row in new_xml_contents.split("\n"):
                row = row.rstrip()
                if row:
                    z += 1
                    if "<document-date>" in row and "</document-date>" in row:
                        document_date = row
                        doc_date = document_date.split(">")[1].split("</")[0].strip()

                    elif "<application-number>" in row:
                        next_number = z + 1
                    elif z == next_number:
                        document_number = row
                        doc_num = document_number.split(">")[1].split("</")[0].strip()

                        if doc_date is not None and doc_num is not None:
                            xml_file = input_file_name + "_" + doc_num + "_ " + doc_date + ".xml"
                            xml_file = xml_file.replace(" ", "")
                            xml_output_file = os.path.join(xml_type_folder, xml_file)
                            doc_year = doc_date[0:4]

                            relative_path = os.path.join("xml_files", xml_file)
                            if verbose:
                                print()
                                print("document_date:".ljust(30), doc_date)
                                print("document_number:".ljust(30), doc_num)
                                print("xml_output_file:".ljust(30), xml_output_file)
                            key = {
                                "application_number": doc_num,
                                "application_year": doc_year,
                                "application_date": doc_date,
                                "xml_relative_path": relative_path
                            }
                            if key not in data_map:
                                data_map.append(key)
                            with open(xml_output_file, "w", encoding="utf-8") as xml_out:
                                xml_out.write(new_xml_contents)
                            new_xml_contents = ""
                            break
    print("Created:".ljust(30), str(x) + " records from_file.")
    return data_map


def read_source_files(xml_src):

    for xml_input in os.listdir(xml_src):
        simple_xml_name = xml_input.replace(".xml", "")
        sample_file_path = os.path.join(xml_src, xml_input)
        print("Reading XML SourceFile:".ljust(30), xml_input)
        with open(sample_file_path, 'r', encoding="utf-8") as f:
            data = f.read()
        xml_map = parse_xml_data(simple_xml_name, data)
        json_string = json.dumps(xml_map, indent=4, sort_keys=False)

        xml_mapped_json = os.path.join(xml_output_folder, simple_xml_name, simple_xml_name + "_mapped.json")
        with open(xml_mapped_json, "w", encoding="utf-8") as json_out:
            json_out.write(json_string)

        xml_mapped_csv = os.path.join(xml_output_folder, simple_xml_name, simple_xml_name + "_mapped.csv")
        with open(xml_mapped_json, encoding='utf-8') as input_json:
            df = pd.read_json(input_json)
        df.to_csv(xml_mapped_csv, encoding='utf-8', index=False)

        return xml_mapped_json, xml_mapped_csv


def main():
    map_json, map_csv = read_source_files(xml_input_folder)
    print("Created DataMap JSON:".ljust(30), map_json)
    print("Created DataMap CSV:".ljust(30), map_csv)


if __name__ == '__main__':
    main()
