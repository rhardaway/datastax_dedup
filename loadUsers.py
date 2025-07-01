from quickstart_connect import connect_to_database
from astrapy.data_types import DataAPIDate
import json


def main() -> None:
    database = connect_to_database()

    table = database.get_table("user_table")

    data_file_path = "/Users/bob.hardaway/work/astra/dedup/users.json"

    with open(data_file_path, "r", encoding="utf8") as file:
        json_data = json.load(file)

    rows = [
        {
            **data,
            "summary_user_vector": (
                f"uuid: {data['uuid']} | "
                f"first_name: {data['first_name']} | last_name: {data['last_name']} | "
                f"email: {data['email']} | userName: {data['userName']}"    
                f"gender: {data['gender']} | loyalty_tier: {data['loyalty_tier']}"    
            ),
        }
        for data in json_data
    ]

    insert_result = table.insert_many(rows)

    print(f"Inserted {len(insert_result.inserted_ids)} rows")


if __name__ == "__main__":
    main()