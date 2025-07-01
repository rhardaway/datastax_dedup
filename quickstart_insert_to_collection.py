import json
from quickstart_connect import connect_to_database
from astrapy.data_types import DataAPIDate


def main() -> None:
    database = connect_to_database()

    collection = database.get_collection("dedup_collection")

    # data_file_path = "PATH_TO_DATA_FILE"
    data_file_path = "/Users/bob.hardaway/work/astra/dedup/bob.json"

    # Read the JSON file and parse it into a JSON array
    with open(data_file_path, "r", encoding="utf8") as file:
        json_data = json.load(file)

    # Assemble the documents to insert:
    # - Convert the date string into a DataAPIDate
    # - Add a $vectorize field
    documents = [
        {
            **data,
            "$vectorize": (
                f"uuid: {data['uuid']} | "
                f"first_name: {data['first_name']} | last_name: {data['last_name']} | "
                f"email: {data['email']} | userName: {data['userName']}"    
                f"gender: {data['gender']} | loyalty_tier: {data['loyalty_tier']}"    
            ),
        }
        for data in json_data
    ]

    # Insert the data
    inserted = collection.insert_many(documents)

    print(f"Inserted {len(inserted.inserted_ids)} documents.")


if __name__ == "__main__":
    main()