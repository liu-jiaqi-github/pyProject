import re

find_sql = f"strSQL := '(.*?)';"


def main():
    sql = ""
    falg = False
    with open("脚本.txt", mode="r", encoding="utf-8") as f:
        with open("脚本2.txt", mode="w", encoding="utf-8") as f2:
            lines = f.readlines()
            for line in lines:
                if line.find("strSQL := '") >= 0:
                    falg = True
                    sql = ""
                if falg:
                    if line.find("raise info '%', strSQL;") >= 0:
                        # print(sql.replace("\n", "").replace("        strSQL := '",""))
                        rep_sql = sql.replace("\n", "").replace("        strSQL := '","")[0:-2]\
                            .replace("''","'").replace("	"," ")
                        print(rep_sql)
                        falg = False
                        f2.write(f"        strSQL := '{rep_sql}';\n")
                        f2.write(f"        raise info '%', strSQL;\n")
                    sql += line
                else:
                    f2.write(line.replace("	"," "))


if __name__ == '__main__':
    main()
