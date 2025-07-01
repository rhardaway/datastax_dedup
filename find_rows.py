from quickstart_connect import connect_to_database


def main() -> None:
    database = connect_to_database()

    table = database.get_table("user_table")

    # Find rows that match a filter
    print("\nFind users...")

    user_cursor = table.find(
        {"first_name": "Shae","last_name": "Harrop","loyalty_tier": "Gold"},
        projection={"email": True, "loyalty_tier": True, "first_name": True, "last_name": True}
    )

    for row in user_cursor:
        print(f"{row['last_name']} has level: {row['loyalty_tier']}")

    # Perform a vector search to find the closest match to a search string
    print("\nUsing vector search to find a single scary novel...")

    single_vector_match = table.find_one(
        {},
        sort={"summary_user_vector": "Shae Harrop"},
        projection={"uuid": True}
    )

    print(f"{single_vector_match['uuid']} is a good match")

    multi_vector_match = table.find(
        {},
        sort={"summary_user_vector": "Bob Hardaway"},
        limit=3,
        include_similarity=True,
        include_sort_vector=True
       # projection={"uuid": True, "first_name": True, "last_name": True, "$similarity": True}
    )

    for row in multi_vector_match:
        print(row)
      #  print(f"{row['first_name']} {row['last_name']} (uuid: {row['uuid']}) - score: {row['$similarity']}")
       # print(f"{row['last_name']} has uuid: {row['uuid']}")

    exit()

    # Combine a filter and vector search to find the 3 books with
    # more than 400 pages that are the closest matches to a search string
    print(
        "\nUsing filters and vector search to find 3 books with more than 400 pages that are set in the arctic, returning just the title and author..."
    )

    vector_cursor = table.find(
        {"number_of_pages": {"$gt": 400}},
        sort={"summary_user_vector": "A book set in the arctic"},
        limit=3,
        projection={"title": True, "author": True},
    )

    for row in vector_cursor:
        print(row)


if __name__ == "__main__":
    main()