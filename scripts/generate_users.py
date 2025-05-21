"""Script to generate multiple users in the database."""

import asyncio
import logging
import random
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Sample data to generate random users
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Susan", "Richard", "Jessica", "Joseph", "Sarah",
    "Thomas", "Karen", "Charles", "Nancy", "Christopher", "Lisa", "Daniel", "Betty",
    "Matthew", "Dorothy", "Anthony", "Sandra", "Mark", "Ashley", "Donald", "Kimberly"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson",
    "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin",
    "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee",
    "Walker", "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez"
]

DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "example.com", "mail.com", "fastmail.com"]


async def generate_users(count: int = 10) -> None:
    """Generate the specified number of random users."""
    logger.info(f"Generating {count} random users")
    
    async with SessionLocal() as db:
        for i in range(1, count + 1):
            try:
                # Generate random user data
                first_name = random.choice(FIRST_NAMES)
                last_name = random.choice(LAST_NAMES)
                full_name = f"{first_name} {last_name}"
                
                # Create a unique username by appending a number if necessary
                base_username = f"{first_name.lower()}{last_name.lower()}"
                username = f"{base_username}{random.randint(1, 999)}"
                
                # Create a unique email
                domain = random.choice(DOMAINS)
                email = f"{username}@{domain}"
                
                # Generate a random password (in real scenarios, provide stronger passwords)
                password = f"Password{random.randint(100, 999)}!"
                
                # Create the user
                user = User(
                    username=username,
                    email=email,
                    full_name=full_name,
                    hashed_password=get_password_hash(password),
                    is_active=random.choice([True, True, True, False]),  # 75% active
                    is_superuser=False,
                    is_verified=random.choice([True, False])  # 50% verified
                )
                
                db.add(user)
                await db.commit()
                
                logger.info(f"Created user {i}/{count}: {username} ({email}) with password: {password}")
                
            except Exception as e:
                logger.error(f"Error creating user {i}: {e}")
                continue
    
    logger.info("User generation completed!")


if __name__ == "__main__":
    print("Starting user generation script...")
    try:
        asyncio.run(generate_users(10))
        print("Script completed successfully!")
    except Exception as e:
        print(f"Script failed with error: {e}")
        import traceback
        traceback.print_exc()
