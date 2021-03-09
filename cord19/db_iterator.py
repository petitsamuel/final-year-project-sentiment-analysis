from db_helpers import init_db, close_db, load_metadata, show_db_count

try:
    init_db()
except Exception as err:
    print("Could not initialise DB: %s" % err)
    quit()

# Builds a list of offsets to load values from the database using
# for offset in build_offset_list():
def build_offset_list(total, size = 100):
    offsets = []
    current_offset = 0
    offsets.append(current_offset)
    while current_offset + size < total:
        current_offset += size
        offsets.append(current_offset)
    return offsets

def iterate_through_data():
    total = show_db_count()
    limit = 1000
    for offset in build_offset_list(total, limit):
        data = load_metadata(limit, offset, shuffled=True)
        # TODO : do something with the data here
        print(data[0][0], len(data))
        quit()
# iterates through data
iterate_through_data()
