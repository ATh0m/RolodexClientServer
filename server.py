from xmlrpc.server import SimpleXMLRPCServer
import shelve

file_name = 'cache'


def read_from_database():
    print("read_from_database")

    with shelve.open(file_name, 'c') as db:
        if 'Contacts' not in db.keys():
            db['Contacts'] = []

        data = db['Contacts']
        print(data)

        return data


def save_to_database(data):
    print("save_to_database")
    print(data)

    with shelve.open(file_name) as db:
        db['Contacts'] = data


server = SimpleXMLRPCServer(("localhost", 8123), allow_none=True)
server.register_function(read_from_database)
server.register_function(save_to_database)

server.serve_forever()