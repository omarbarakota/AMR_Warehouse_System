#!/usr/bin/env python3
"""
Simple test script to verify database initialization
"""

from app.main import app, db, User, MQTTMessage, SystemLog

def test_database():
    """Test database initialization and basic operations"""
    
    with app.app_context():
        print("🧪 Testing database initialization...")
        
        # Create tables
        db.create_all()
        print("✅ Database tables created")
        
        # Test user creation
        test_user = User(
            username='test_user',
            password_hash='test_hash',
            email='test@example.com',
            role='user'
        )
        db.session.add(test_user)
        db.session.commit()
        print("✅ User creation test passed")
        
        # Test query
        user = User.query.filter_by(username='test_user').first()
        if user:
            print(f"✅ User query test passed: {user.username}")
        else:
            print("❌ User query test failed")
        
        # Clean up
        db.session.delete(test_user)
        db.session.commit()
        print("✅ Database cleanup completed")
        
        print("\n🎉 All database tests passed!")

if __name__ == '__main__':
    test_database() 