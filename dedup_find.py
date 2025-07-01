from quickstart_connect import connect_to_database

def main() -> None:
    database = connect_to_database()

    collection = database.get_collection("dedup_collection")

    # Find documents that match a filter
    print("\nFinding books with rating greater than 4.7...")

    rating_cursor = collection.find({"last_name": "Stading"})

    for document in rating_cursor:
        print(f"{document['last_name']} is of gender {document['gender']}")

    # Perform a vector search to find the closest match to a search string
    print("\nUsing vector search to find a single scary novel...")

    single_vector_match = collection.find_one(sort={"$vectorize": "Jerrilyn Rangell"})

    print(f"{single_vector_match['userName']} is registered")

    # Combine a filter, vector search, and projection to find the 3 books with
    # more than 400 pages that are the closest matches to a search string,
    # and just return the title and author
    print("\nUsing filters and vector search to isolate different users...")

    vector_cursor = collection.find(
        {"gender": {"$gt": "Female"}},
        sort={"$vectorize": "c8b9d7b4-065f-4af8-a109-9fb4b905e74d Bob Hardaway bob@datastax.com Male Gold bob12"},
        limit=5,
        include_similarity=True,
        include_sort_vector=True
        #projection={"first_name": True, "last_name": True}
    )

    for document in vector_cursor:
        print(document)


if __name__ == "__main__":
    main()