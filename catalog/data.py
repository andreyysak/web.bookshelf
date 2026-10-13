from datetime import date

BOOKS = [
    {
        'title': 'the great gatsby',
        'author': 'F. Scott Fitzgerald',
        'year': 1925,
        'pages': 1,
        'description': (
            'A mysterious millionaire named Jay Gatsby throws extravagant '
            'parties in the hope of reuniting with his former love, Daisy Buchanan. '
            'Through the eyes of Nick Carraway, the story explores wealth, ambition, '
            'love, and the American Dream.'
        ),
        'published': date(1925, 4, 10),
    },
    {
        'title': '1984',
        # 'author': 'George Orwell',
        'year': 1949,
        'pages': 328,
        'description': (
            'Winston Smith lives in a society controlled by the Party and its '
            'leader, Big Brother. The government monitors citizens and manipulates '
            'the truth to maintain absolute power. Winston begins to question '
            'the system and searches for freedom and individuality.'
        ),
        'published': date(1949, 6, 8),
    },
    {
        'title': 'to kill a mockingbird',
        'author': 'Harper Lee',
        'year': 1960,
        'pages': 281,
        'description': (
            'Scout Finch grows up in a small town in Alabama during the 1930s. '
            'Her father, Atticus Finch, defends a Black man who has been '
            'unjustly accused of a crime. Through Scout’s experiences, the novel '
            'explores justice, prejudice, compassion, and moral courage.'
        ),
        'published': date(1960, 7, 11),
    },
    {
        'title': 'the hobbit',
        'author': None,
        'year': 1937,
        'pages': 310,
        'description': (
            'Bilbo Baggins is a hobbit who enjoys a peaceful and comfortable life. '
            'Everything changes when the wizard Gandalf and a group of dwarves '
            'invite him on a dangerous adventure. Along the way, Bilbo discovers '
            'his courage and encounters mysterious creatures and unexpected challenges.'
        ),
        'published': date(1937, 9, 21),
    },
    {
        'title': 'pride and prejudice',
        'author': 'Jane Austen',
        'year': 1813,
        'pages': 432,
        'description': (
            'Elizabeth Bennet navigates questions of love, marriage, and social '
            'expectations in nineteenth-century England. Her first impressions '
            'of the wealthy Mr. Darcy lead to misunderstandings and conflict. '
            'As they learn more about each other, both characters reconsider '
            'their prejudices and discover the importance of personal growth.'
        ),
        'published': date(1813, 1, 28),
    },
]
