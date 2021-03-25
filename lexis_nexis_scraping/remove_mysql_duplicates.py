from shared.db_helpers import init_db, load_duplicates, load_by_title, remove_by_ids
from shared.files import compute_similarity

def remove_db_duplicates():
    init_db()
    duplicates = load_duplicates()
    for _, title in duplicates:
        all_duplicates = load_by_title(title)
        if len(all_duplicates) >= 100:
            print("Skipping duplicate checking - over 100 articles have the same type")
            continue
        print("Loaded %d potential duplicates" % (len(all_duplicates)))
        to_remove = []
        while len(all_duplicates) > 1:
            i_id, i_body = all_duplicates.pop(0)
            tmp_to_remove = []
            for j_id, j_body in all_duplicates:
                if compute_similarity(i_body, j_body) >= 0.90:
                    tmp_to_remove.append(j_id)
            to_remove = to_remove + tmp_to_remove
            
            # Remove ids in tmp_to_remove from all_duplicates
            # these will be removed so we don't need to consider them anymore
            all_duplicates = [(x, y) for x, y in all_duplicates if not x in tmp_to_remove]
        if len(to_remove):
            remove_by_ids(to_remove)

remove_db_duplicates()
