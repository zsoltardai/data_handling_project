from mysql.connector import MySQLConnection
from data.project.handler import CSVHandler, JSONHandler, XLSXHandler, SQLHandler
from data.project.model import DeliveryDataset
from visualization import couriers_by_delivery_methods, clients_by_gender, number_of_restaurants_by_profile


def help_message() -> str:
    """
    Returns a help message which can be displayed for the users.
    :return: the message
    """

    return """
Welcome to our fantastic data handling software which deals with data of trips. In this example, you can generate,
read, write and query a schema which belongs to a car-rental company and contains four types of records:
people, cars, airports and transactions.
Commands:
    help
        You can display this message whenever you want to.
    exit
        Terminates the program.
    generate <count-of-people> <count-of-cars> <count-of-airports> <count-of-transactions>
        Generates a dataset which contains a given number of people, cars, airports
        and transactions. Also generates their relationships.
    read <format> <path>
        Reads the dataset in a given format, from a given place of your file system.
        <format> is one of the following parameters: csv, json, xlsx, mysql
        <path> is a path of a folder which contains the needed file(s). The parameter 
        must be omitted when you select mysql as the format.
    write <format> <path>
        Writes the dataset in a given format, to a given place of your file system.
        <format> is one of the following parameters: csv, json, xlsx, mysql
        <path> is a path of a folder which will contain the generated file(s).
        The parameter must be omitted when you select mysql as the format.
    query-<id>
        Executes the queries, explains and visualizes their output.
"""


def get_connection() -> MySQLConnection:
    """
    Reads properties of a MySQL connection, then creates the connection.
    :return: the connection
    """

    print("Enter db host:")
    print("$", end=" ")
    host = input()

    print("Enter db user:")
    print("$", end=" ")
    user = input()

    print("Enter db password:")
    print("$", end=" ")
    password = input()

    print("Enter db name:")
    print("$", end=" ")
    database = input()

    return MySQLConnection(
        host=host,
        user=user,
        passwd=password,
        database=database
    )


def main() -> None:
    """
    Starts an interactive shell.
    :return: nothing
    """
    print(help_message())

    connection = get_connection()

    dataset = None
    dataset_type = DeliveryDataset

    writers = {
        "csv": lambda t: CSVHandler.write_dataset(dataset, t[2]),
        "xlsx": lambda t: XLSXHandler.write_dataset(dataset, t[2]),
        "json": lambda t: JSONHandler.write_dataset(dataset, t[2]),
        "mysql": lambda t: SQLHandler.write_dataset(dataset, connection)
    }

    readers = {
        "csv": lambda t: CSVHandler.read_dataset(dataset_type, t[2]),
        "xlsx": lambda t: XLSXHandler.read_dataset(dataset_type, t[2]),
        "json": lambda t: JSONHandler.read_dataset(dataset_type, t[2]),
        "mysql": lambda t: SQLHandler.read_dataset(dataset_type, connection)
    }

    while True:
        try:
            print("$", end=" ")
            line = input()
            tokens = line.split(" ")
            if tokens[0] == "exit":
                connection.close()
                break
            elif tokens[0] == "help":
                print(help_message())
            elif len(tokens) == 5 and tokens[0] == "generate":
                dataset = dataset_type.generate(int(tokens[1]), int(tokens[2]), int(tokens[3]), int(tokens[4]))
            elif tokens[0] == "write":
                writers[tokens[1]](tokens)
            elif tokens[0] == "read":
                dataset = readers[tokens[1]](tokens)
            elif tokens[0] == "query-1":
                couriers_by_delivery_methods(dataset)
            elif tokens[0] == "query-2":
                clients_by_gender(dataset)
            elif tokens[0] == "query-3":
                number_of_restaurants_by_profile(dataset)
            else:
                raise RuntimeError("unknown command")
        except Exception:
            print("command cannot be executed")


if __name__ == "__main__":
    main()
