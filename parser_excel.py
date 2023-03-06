from dbcon import Database
import argparse
import sys
import os
import pandas

db_name = "result_db.sqlite3"
mnth = "02"
year = "2023"
types = ["fact", "forecast"]  # The type of possible values in file

global Db
Db = Database(db_name)


def parse_args():
    parser = argparse.ArgumentParser(description='Utility to parse Excel')
    parser.add_argument('-f', '--input', help="File for parsing", dest='file', required=True)
    parser.add_argument('-o', '--output', help="Total output", dest='output', required=False, default="output.xlsx")
    parser.add_argument('-m', '--mode', help="Append or overwrite data", dest='mode', required=False, default="APPEND")
    parser.add_argument('-d', '--delcompany', help="Delete Company by Name", dest='delcomp', required=False, default="")
    arguments = parser.parse_args()
    return arguments


def load_data(file: str):
    df = pandas.ExcelFile(file)
    sheet1 = df.parse(0)
    type_1_data_start = -1
    type_2_data_start = -1
    for i, el_ in enumerate(sheet1.head(0).columns):
        if types[0] in el_:
            type_1_data_start = i
        elif types[1] in el_:
            type_2_data_start = i

    for el_ in sheet1.values:
        try: # Skipping head
            if int(el_[0]) > 0:
                day = f"0{str(int(el_[0]) % 28 + 1)}" # Generates day for program date below
                dt = f"{year}-{mnth}-{day[-2:]}"
                comp = el_[1]
                for j, type_ in enumerate(types):
                    qliq = []
                    qoil = []
                    if j == 0:
                        tp_1 = type_1_data_start
                        tp_2 = type_2_data_start
                    else:
                        tp_1 = type_2_data_start
                        tp_2 = len(el_)
                    for i in range(tp_1, tp_2):
                        if i in range(tp_1, tp_1 + (tp_2 - tp_1) // 2):
                            # The number of data (data1, data2) for each type can be different.
                            qliq.append(el_[i])
                        elif i in range(tp_1 + (tp_2 - tp_1) // 2, tp_2):
                            qoil.append(el_[i])
                    if Db.add_data(company=comp, type=type_, qliq=qliq, qoil=qoil, dt=dt) < 0:
                        print("Please check structure of input file")
                        exit(-1)
        except:
            pass
    print("Data was uploaded successfully")


def main():
    args = parse_args()
    if not os.path.exists(args.file):
        print(f"The input file {args.file} does not exist")
        return -1
    print("Started parsing")
    if args.mode.lower() != "append":
        Db.truncate_data()
    if args.delcomp:
        Db.delete_company(args.delcomp)
    load_data(args.file)
    try:
        output_data = Db.print_total() # Generates Totals data
        pandas.DataFrame(output_data).to_excel(f'{args.output}', header=False, index=False)
        print(f"File {args.output} was created successfully")
    except Exception as err:
        print(f"File {args.output} was not created. Error: {err}")


if __name__ == '__main__':
    sys.exit(main())
