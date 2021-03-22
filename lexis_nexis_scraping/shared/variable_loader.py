import json

def write_offset_to_file(value):
    print("\nWriting new offset - %d - to offset file" % (value))
    f = open("/home/sam/dev/fyp/lexis_nexis_scraping/shared/offset.txt", "w")
    f.write("%d" % (value))
    f.close()

def read_offset_from_file():
    f = open("/home/sam/dev/fyp/lexis_nexis_scraping/shared/offset.txt", "r")
    value = int(f.read())
    f.close()
    return value

def write_to_file(value, file):
    print("\nWriting to file - %s" % (file))
    f = open("/home/sam/dev/fyp/lexis_nexis_scraping/data/" + file, "w")
    f.write(json.dumps(value))
    print("Done!")
    f.close()