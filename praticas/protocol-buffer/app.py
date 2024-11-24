from models import bookstore_pb2 as bookstore_model


author1 = bookstore_model.Author()
author1.id = "1"
author1.name = "George Orwell"
author1.age = 42
author1.bio = "Orwell's bio"

book1 = bookstore_model.Book()
book1.id = "1"
book1.title = "1984"
book1.author.CopyFrom(author1)
book1.year = 1949
book1.price = 15.99

book2 = bookstore_model.Book()
book2.id = "2"
book2.title = "Animal Farm"
book2.author.CopyFrom(author1)
book2.year = 1945
book2.price = 12.99

bookstore = bookstore_model.Bookstore()
bookstore.books.append(book1)
bookstore.books.append(book2)

serializated_bookstore = bookstore.SerializeToString()

print(f"\nBookstore serialized data: {serializated_bookstore}\n")

deserialized_bookstore = bookstore_model.Bookstore()
deserialized_bookstore.ParseFromString(serializated_bookstore)

print(f"Bookstore deserialized data: {deserialized_bookstore}\n")
