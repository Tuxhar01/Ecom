from models import User, Book, init_db

def seed_database():
    """Seed the database with initial data."""
    
    print("Seeding database...")
    
    # Initialize database
    init_db()
    
    # Create test users
    users_data = [
        {
            'email': 'admin@bookstore.com',
            'username': 'admin',
            'password': 'admin123'
        },
        {
            'email': 'john@example.com',
            'username': 'john_doe',
            'password': 'password123'
        },
        {
            'email': 'jane@example.com',
            'username': 'jane_smith',
            'password': 'password123'
        }
    ]
    
    print("\nCreating users...")
    for user_data in users_data:
        user = User(
            email=user_data['email'],
            username=user_data['username'],
            password=user_data['password']
        )
        user.save()
        print(f"  - Created user: {user.username} ({user.email})")
    
    # Create sample books
    books_data = [
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'price': 12.99,
            'stock': 50,
            'description': 'A classic American novel set in the Jazz Age.',
            'cover_image': 'https://covers.openlibrary.org/b/id/7222246-L.jpg',
            'isbn': '9780743273565'
        },
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'price': 14.99,
            'stock': 45,
            'description': 'A gripping tale of racial injustice and childhood innocence.',
            'cover_image': 'https://covers.openlibrary.org/b/id/8228691-L.jpg',
            'isbn': '9780061120084'
        },
        {
            'title': '1984',
            'author': 'George Orwell',
            'price': 13.99,
            'stock': 60,
            'description': 'A dystopian social science fiction novel.',
            'cover_image': 'https://covers.openlibrary.org/b/id/7222246-L.jpg',
            'isbn': '9780451524935'
        },
        {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'price': 11.99,
            'stock': 40,
            'description': 'A romantic novel of manners.',
            'cover_image': 'https://covers.openlibrary.org/b/id/8235657-L.jpg',
            'isbn': '9780141439518'
        },
        {
            'title': 'The Catcher in the Rye',
            'author': 'J.D. Salinger',
            'price': 13.49,
            'stock': 35,
            'description': 'A story about teenage rebellion and angst.',
            'cover_image': 'https://covers.openlibrary.org/b/id/8228691-L.jpg',
            'isbn': '9780316769174'
        },
        {
            'title': 'Harry Potter and the Sorcerer\'s Stone',
            'author': 'J.K. Rowling',
            'price': 15.99,
            'stock': 100,
            'description': 'The first book in the Harry Potter series.',
            'cover_image': 'https://covers.openlibrary.org/b/id/10521270-L.jpg',
            'isbn': '9780439708180'
        },
        {
            'title': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'price': 14.49,
            'stock': 55,
            'description': 'A fantasy novel and children\'s book.',
            'cover_image': 'https://covers.openlibrary.org/b/id/8235657-L.jpg',
            'isbn': '9780547928227'
        },
        {
            'title': 'Fahrenheit 451',
            'author': 'Ray Bradbury',
            'price': 12.49,
            'stock': 42,
            'description': 'A dystopian novel about a future where books are banned.',
            'cover_image': 'https://covers.openlibrary.org/b/id/7222246-L.jpg',
            'isbn': '9781451673319'
        },
        {
            'title': 'The Lord of the Rings',
            'author': 'J.R.R. Tolkien',
            'price': 25.99,
            'stock': 30,
            'description': 'An epic high-fantasy novel.',
            'cover_image': 'https://covers.openlibrary.org/b/id/8235657-L.jpg',
            'isbn': '9780544003415'
        },
        {
            'title': 'Animal Farm',
            'author': 'George Orwell',
            'price': 10.99,
            'stock': 48,
            'description': 'An allegorical novella about Soviet totalitarianism.',
            'cover_image': 'https://covers.openlibrary.org/b/id/7222246-L.jpg',
            'isbn': '9780451526342'
        },
        {
            'title': 'Brave New World',
            'author': 'Aldous Huxley',
            'price': 13.99,
            'stock': 38,
            'description': 'A dystopian novel set in a futuristic World State.',
            'cover_image': 'https://covers.openlibrary.org/b/id/8228691-L.jpg',
            'isbn': '9780060850524'
        },
        {
            'title': 'The Chronicles of Narnia',
            'author': 'C.S. Lewis',
            'price': 22.99,
            'stock': 32,
            'description': 'A series of seven fantasy novels.',
            'cover_image': 'https://covers.openlibrary.org/b/id/8235657-L.jpg',
            'isbn': '9780066238500'
        },
        {
            'title': 'Moby-Dick',
            'author': 'Herman Melville',
            'price': 16.99,
            'stock': 25,
            'description': 'The narrative of Captain Ahab\'s obsessive quest.',
            'cover_image': 'https://covers.openlibrary.org/b/id/7222246-L.jpg',
            'isbn': '9781503280786'
        },
        {
            'title': 'War and Peace',
            'author': 'Leo Tolstoy',
            'price': 18.99,
            'stock': 20,
            'description': 'A novel that chronicles the French invasion of Russia.',
            'cover_image': 'https://covers.openlibrary.org/b/id/8228691-L.jpg',
            'isbn': '9781400079988'
        },
        {
            'title': 'The Odyssey',
            'author': 'Homer',
            'price': 14.99,
            'stock': 28,
            'description': 'An ancient Greek epic poem.',
            'cover_image': 'https://covers.openlibrary.org/b/id/8235657-L.jpg',
            'isbn': '9780140268867'
        },
        {
            'title': 'Crime and Punishment',
            'author': 'Fyodor Dostoevsky',
            'price': 15.49,
            'stock': 33,
            'description': 'A psychological novel about a poor ex-student.',
            'cover_image': 'https://covers.openlibrary.org/b/id/7222246-L.jpg',
            'isbn': '9780486415871'
        },
        {
            'title': 'The Divine Comedy',
            'author': 'Dante Alighieri',
            'price': 17.99,
            'stock': 22,
            'description': 'An Italian long narrative poem.',
            'cover_image': 'https://covers.openlibrary.org/b/id/8228691-L.jpg',
            'isbn': '9780142437223'
        },
        {
            'title': 'Wuthering Heights',
            'author': 'Emily Brontë',
            'price': 12.99,
            'stock': 36,
            'description': 'A novel about the intense, almost demonic love.',
            'cover_image': 'https://covers.openlibrary.org/b/id/8235657-L.jpg',
            'isbn': '9780141439556'
        },
        {
            'title': 'Jane Eyre',
            'author': 'Charlotte Brontë',
            'price': 13.49,
            'stock': 41,
            'description': 'A novel that follows the experiences of its eponymous heroine.',
            'cover_image': 'https://covers.openlibrary.org/b/id/7222246-L.jpg',
            'isbn': '9780141441146'
        },
        {
            'title': 'The Picture of Dorian Gray',
            'author': 'Oscar Wilde',
            'price': 11.49,
            'stock': 44,
            'description': 'A philosophical novel about a young man who sells his soul.',
            'cover_image': 'https://covers.openlibrary.org/b/id/8228691-L.jpg',
            'isbn': '9780141439570'
        }
    ]
    
    print("\nCreating books...")
    for book_data in books_data:
        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            price=book_data['price'],
            stock=book_data['stock'],
            description=book_data['description'],
            cover_image=book_data['cover_image'],
            isbn=book_data['isbn']
        )
        book.save()
        print(f"  - Created book: {book.title} by {book.author}")
    
    print(f"\nDatabase seeded successfully!")
    print(f"  - {len(users_data)} users created")
    print(f"  - {len(books_data)} books created")
    print("\nTest credentials:")
    print("  Email: admin@bookstore.com")
    print("  Password: admin123")


if __name__ == '__main__':
    seed_database()

# Made with Bob
