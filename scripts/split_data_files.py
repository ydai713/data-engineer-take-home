import os


OUTPUT_DIR = "token_data"


def split_sql_file(kind, lines_per_file=5000):
    """
    Split a large SQL file into smaller files with a specified number of lines.
    """
    if kind == "log":
        input_file_path = os.path.join(OUTPUT_DIR, "logs_data.sql")
    elif kind == "txs":
        input_file_path = os.path.join(OUTPUT_DIR, "txs_data.sql")
    else:
        raise ValueError("Wrong date type")

    with open(input_file_path, "r") as file:
        file_number = 1
        line_count = 0
        current_chunk = []

        for line in file:
            current_chunk.append(line)
            line_count += 1

            if line_count >= lines_per_file:
                output_file = os.path.join(OUTPUT_DIR, f"{kind}_{file_number}.sql")
                print(output_file)
                with open(output_file, "w") as chunk_file:
                    chunk_file.writelines(current_chunk)

                print(f"Created: {output_file}")
                file_number += 1
                line_count = 0
                current_chunk = []

        # Handle the last chunk
        if current_chunk:
            output_file = os.path.join(OUTPUT_DIR, f"{kind}_{file_number}.sql")
            with open(output_file, "w") as chunk_file:
                chunk_file.writelines(current_chunk)


if __name__ == "__main__":
    split_sql_file(kind="log")
    split_sql_file(kind="txs")
