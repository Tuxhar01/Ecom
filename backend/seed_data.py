from models import User, Book, db_session, init_db, drop_db
from datetime import datetime


def seed_database():
    """Seed the database with sample data."""
    
    print("Initializing database...")
    # Drop existing tables and recreate
    try:
        drop_db()
    except:
        pass
    init_db()
    
    print("Creating sample users...")
    # Create sample users
    users = [
        {
            'email': 'user@example.com',
            'username': 'johndoe',
            'password': 'password123'
        },
        {
            'email': 'admin@example.com',
            'username': 'admin',
            'password': 'admin123'
        },
        {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'test123'
        }
    ]
    
    for user_data in users:
        user = User(
            email=user_data['email'],
            username=user_data['username']
        )
        user.set_password(user_data['password'])
        db_session.add(user)
    
    print("Creating sample books...")
    # Create sample books
    books = [
        {
            'title': 'Clean Code',
            'author': 'Robert C. Martin',
            'price': 29.99,
            'stock': 15,
            'description': 'A Handbook of Agile Software Craftsmanship',
            'isbn': '9780132350884',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/41xShlnTZTL._SX376_BO1,204,203,200_.jpg'
        },
        {
            'title': 'The Pragmatic Programmer',
            'author': 'Andrew Hunt, David Thomas',
            'price': 34.99,
            'stock': 12,
            'description': 'Your Journey To Mastery',
            'isbn': '9780135957059',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51W1sBPO7tL._SX380_BO1,204,203,200_.jpg'
        },
        {
            'title': 'Design Patterns',
            'author': 'Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides',
            'price': 39.99,
            'stock': 8,
            'description': 'Elements of Reusable Object-Oriented Software',
            'isbn': '9780201633610',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51szD9HC9pL._SX395_BO1,204,203,200_.jpg'
        },
        {
            'title': 'Refactoring',
            'author': 'Martin Fowler',
            'price': 32.99,
            'stock': 10,
            'description': 'Improving the Design of Existing Code',
            'isbn': '9780134757599',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/41LBzpPXCOL._SX379_BO1,204,203,200_.jpg'
        },
        {
            'title': 'Introduction to Algorithms',
            'author': 'Thomas H. Cormen, Charles E. Leiserson',
            'price': 89.99,
            'stock': 5,
            'description': 'A comprehensive textbook on algorithms',
            'isbn': '9780262033848',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/41T0iBxY8FL._SX440_BO1,204,203,200_.jpg'
        },
        {
            'title': 'You Don\'t Know JS',
            'author': 'Kyle Simpson',
            'price': 24.99,
            'stock': 20,
            'description': 'Up & Going',
            'isbn': '9781491924464',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/41jEbK-jG+L._SX379_BO1,204,203,200_.jpg'
        },
        {
            'title': 'Eloquent JavaScript',
            'author': 'Marijn Haverbeke',
            'price': 27.99,
            'stock': 18,
            'description': 'A Modern Introduction to Programming',
            'isbn': '9781593279509',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51InjRPaF7L._SX377_BO1,204,203,200_.jpg'
        },
        {
            'title': 'Python Crash Course',
            'author': 'Eric Matthes',
            'price': 31.99,
            'stock': 14,
            'description': 'A Hands-On, Project-Based Introduction to Programming',
            'isbn': '9781593279288',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51Ieh-EWJnL._SX376_BO1,204,203,200_.jpg'
        },
        {
            'title': 'Automate the Boring Stuff with Python',
            'author': 'Al Sweigart',
            'price': 29.99,
            'stock': 16,
            'description': 'Practical Programming for Total Beginners',
            'isbn': '9781593279929',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51SYS7RbN7L._SX376_BO1,204,203,200_.jpg'
        },
        {
            'title': 'The Mythical Man-Month',
            'author': 'Frederick P. Brooks Jr.',
            'price': 26.99,
            'stock': 7,
            'description': 'Essays on Software Engineering',
            'isbn': '9780201835953',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51WIp-ZuXWL._SX334_BO1,204,203,200_.jpg'
        },
        {
            'title': 'Code Complete',
            'author': 'Steve McConnell',
            'price': 44.99,
            'stock': 9,
            'description': 'A Practical Handbook of Software Construction',
            'isbn': '9780735619678',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51FUYfErOXL._SX408_BO1,204,203,200_.jpg'
        },
        {
            'title': 'The Clean Coder',
            'author': 'Robert C. Martin',
            'price': 28.99,
            'stock': 11,
            'description': 'A Code of Conduct for Professional Programmers',
            'isbn': '9780137081073',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/41yafGMO+rL._SX382_BO1,204,203,200_.jpg'
        },
        {
            'title': 'Head First Design Patterns',
            'author': 'Eric Freeman, Elisabeth Robson',
            'price': 36.99,
            'stock': 13,
            'description': 'A Brain-Friendly Guide',
            'isbn': '9780596007126',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51S8VRFX1CL._SX430_BO1,204,203,200_.jpg'
        },
        {
            'title': 'Cracking the Coding Interview',
            'author': 'Gayle Laakmann McDowell',
            'price': 33.99,
            'stock': 25,
            'description': '189 Programming Questions and Solutions',
            'isbn': '9780984782857',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51l5XzLln+L._SX348_BO1,204,203,200_.jpg'
        },
        {
            'title': 'Effective Java',
            'author': 'Joshua Bloch',
            'price': 38.99,
            'stock': 10,
            'description': 'Best Practices for the Java Platform',
            'isbn': '9780134685991',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/41qzW7WHDNL._SX379_BO1,204,203,200_.jpg'
        },
        {
            'title': 'JavaScript: The Good Parts',
            'author': 'Douglas Crockford',
            'price': 22.99,
            'stock': 17,
            'description': 'Unearthing the Excellence in JavaScript',
            'isbn': '9780596517748',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/5166ztxN-FL._SX381_BO1,204,203,200_.jpg'
        },
        {
            'title': 'Domain-Driven Design',
            'author': 'Eric Evans',
            'price': 42.99,
            'stock': 6,
            'description': 'Tackling Complexity in the Heart of Software',
            'isbn': '9780321125217',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51OWGtzQLLL._SX375_BO1,204,203,200_.jpg'
        },
        {
            'title': 'Working Effectively with Legacy Code',
            'author': 'Michael Feathers',
            'price': 35.99,
            'stock': 8,
            'description': 'Strategies for working with large, untested legacy code bases',
            'isbn': '9780131177055',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51U6aF7JxBL._SX376_BO1,204,203,200_.jpg'
        },
        {
            'title': 'Continuous Delivery',
            'author': 'Jez Humble, David Farley',
            'price': 37.99,
            'stock': 9,
            'description': 'Reliable Software Releases through Build, Test, and Deployment Automation',
            'isbn': '9780321601919',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51yF2SYUi7L._SX379_BO1,204,203,200_.jpg'
        },
        {
            'title': 'The DevOps Handbook',
            'author': 'Gene Kim, Jez Humble, Patrick Debois, John Willis',
            'price': 34.99,
            'stock': 12,
            'description': 'How to Create World-Class Agility, Reliability, and Security',
            'isbn': '9781942788003',
            'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51Jrw7a5CyL._SX379_BO1,204,203,200_.jpg'
        }
    ]
    
    for book_data in books:
        book = Book(**book_data)
        db_session.add(book)
    
    # Commit all changes
    db_session.commit()
    
    print("\n" + "="*60)
    print("✅ Database seeded successfully!")
    print("="*60)
    print(f"📚 Created {len(books)} books")
    print(f"👥 Created {len(users)} users")
    print("\nTest User Credentials:")
    print("-" * 60)
    for user_data in users:
        print(f"  Email: {user_data['email']}")
        print(f"  Password: {user_data['password']}")
        print()
    print("="*60)


if __name__ == '__main__':
    seed_database()

# Made with Bob
