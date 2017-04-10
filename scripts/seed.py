import sys
from os.path import dirname, join
sys.path.append(join(dirname(dirname(__file__))))

from praelatus.lib import session, clean_db
import praelatus.lib.users as usr


print(sys.path)

db = session()
# clean_db()

users = [
    {
        'username': 'testadmin',
        'password': 'test',
        'email': 'test@example.com',
        'full_name': 'Test Testerson',
        'is_admin': True,
    },
    {
        'username': 'anonymous',
        'password': 'none',
        'email': 'anonymous',
        'full_name': 'Anonymous User',
        'is_active': False,
    },
    {
        'username': 'testuser',
        'password': 'test',
        'email': 'test@example.com',
        'full_name': 'Test Testerson II',
    }
]


for u in users:
    try:
        usr.new(db, **u)
    except:
        continue
