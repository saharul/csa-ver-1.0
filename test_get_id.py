

def get_record(self, record_id):
    dbfilename = "service_master.csv"
    with open(self.dbfilename,"r") as f:
        for line in f:
            line = line.rstrip()
            line = line.split(",", 9)
            if (line[0] == str(record_id)):
            return line


def main():
    #*********************** BEGINING OF MAIN PROGRAM *******************
    print(get_record(2))

if __name__ == "__main__":
    main()