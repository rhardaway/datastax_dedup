from quickstart_connect import connect_to_database
from astrapy.info import (
    CreateTableDefinition,
    ColumnType,
    TableVectorIndexOptions,
    VectorServiceOptions,
)
from astrapy.constants import VectorMetric


def main() -> None:
    database = connect_to_database()

    table_definition = (
        CreateTableDefinition.builder()
        # Define all of the columns in the table
        .add_column("id", ColumnType.INT)
        .add_column("uuid", ColumnType.TEXT)
        .add_column("first_name", ColumnType.TEXT)
        .add_column("last_name", ColumnType.TEXT)
        .add_column("email", ColumnType.TEXT)
        .add_column("gender", ColumnType.TEXT)
        .add_column("loyalty_tier", ColumnType.TEXT)
        .add_column("userName", ColumnType.TEXT)
        # This column will store vector embeddings
        # The column will use an embedding model from NVIDIA to generate the
        # vector embeddings when data is inserted to the column.
        .add_vector_column(
            "summary_user_vector",
            dimension=1024,
            service=VectorServiceOptions(
                provider="nvidia",
                model_name="NV-Embed-QA",
            ),
        )
        # Define the primary key for the table.
        # In this case, the table uses a composite primary key.
        .add_partition_by(["first_name", "last_name"])
        # Finally, build the table definition.
        .build()
    )

    table = database.create_table(
        "user_table",
        definition=table_definition,
    )

    print("Created table")

    # Index any columns that you want to sort and filter on.
    table.create_index(
        "loyalty_tier_index",
        column="loyalty_tier",
    )
    table.create_index(
        "first_name_index",
        column="first_name",
    )
    table.create_index(
        "last_name_index",
        column="last_name",
    )
    table.create_index(
        "id_index",
        column="id",
    )

    table.create_vector_index(
        "summary_user_vector_index",
        column="summary_user_vector",
        options=TableVectorIndexOptions(
            metric=VectorMetric.COSINE,
        ),
    )

    print("Indexed columns")

if __name__ == "__main__":
    main()