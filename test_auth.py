#!/usr/bin/env python3
"""
Simple test script to verify authentication system functionality
"""
import requests
import re
from urllib.parse import urljoin


class AuthTester:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_home_page(self):
        """Test home page accessibility"""
        print("🏠 Testing home page...")
        response = self.session.get(self.base_url)
        if response.status_code == 200 and "Welcome to My Personal Website" in response.text:
            print("✅ Home page accessible")
            return True
        else:
            print("❌ Home page failed")
            return False
    
    def test_login_page(self):
        """Test login page accessibility"""
        print("🔑 Testing login page...")
        response = self.session.get(urljoin(self.base_url, '/auth/login'))
        if response.status_code == 200 and "Sign In" in response.text:
            print("✅ Login page accessible")
            return True
        else:
            print("❌ Login page failed")
            return False
    
    def test_register_page(self):
        """Test registration page accessibility"""
        print("📝 Testing registration page...")
        response = self.session.get(urljoin(self.base_url, '/auth/register'))
        if response.status_code == 200 and "Create Account" in response.text:
            print("✅ Registration page accessible")
            return True
        else:
            print("❌ Registration page failed")
            return False
    
    def test_protected_redirect(self):
        """Test that protected routes redirect to login"""
        print("🛡️ Testing protected route redirection...")
        response = self.session.get(urljoin(self.base_url, '/dashboard'), allow_redirects=False)
        if response.status_code == 302 and '/auth/login' in response.headers.get('Location', ''):
            print("✅ Protected routes properly redirect to login")
            return True
        else:
            print("❌ Protected route redirection failed")
            return False
    
    def extract_csrf_token(self, html):
        """Extract CSRF token from HTML"""
        match = re.search(r'name="csrf_token"[^>]*value="([^"]*)"', html)
        return match.group(1) if match else None
    
    def test_registration(self, username="testuser123", email="test@example.com", password="testpass123"):
        """Test user registration"""
        print(f"📋 Testing user registration for {username}...")
        
        # Get registration page and CSRF token
        response = self.session.get(urljoin(self.base_url, '/auth/register'))
        csrf_token = self.extract_csrf_token(response.text)
        
        if not csrf_token:
            print("❌ Could not extract CSRF token")
            return False
        
        # Submit registration form
        data = {
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password,
            'csrf_token': csrf_token,
            'submit': 'Register'
        }
        
        response = self.session.post(urljoin(self.base_url, '/auth/register'), data=data)
        
        if response.status_code == 200 and ("already taken" in response.text or "already registered" in response.text):
            print("ℹ️ User already exists (expected for repeated tests)")
            return True
        elif "Congratulations" in response.text or response.url.endswith('/auth/login'):
            print("✅ User registration successful")
            return True
        else:
            print("❌ User registration failed")
            return False
    
    def test_login(self, username="admin", password="admin123"):
        """Test user login"""
        print(f"🔐 Testing user login for {username}...")
        
        # Get login page and CSRF token
        response = self.session.get(urljoin(self.base_url, '/auth/login'))
        csrf_token = self.extract_csrf_token(response.text)
        
        if not csrf_token:
            print("❌ Could not extract CSRF token")
            return False
        
        # Submit login form
        data = {
            'email_or_username': username,
            'password': password,
            'csrf_token': csrf_token,
            'submit': 'Sign In'
        }
        
        response = self.session.post(urljoin(self.base_url, '/auth/login'), data=data)
        
        if "Welcome back" in response.text or response.url.endswith('/'):
            print("✅ User login successful")
            return True
        else:
            print("❌ User login failed")
            return False
    
    def test_dashboard_access(self):
        """Test dashboard access after login"""
        print("📊 Testing dashboard access...")
        response = self.session.get(urljoin(self.base_url, '/dashboard'))
        
        if response.status_code == 200 and "Dashboard" in response.text:
            print("✅ Dashboard accessible after login")
            return True
        else:
            print("❌ Dashboard access failed")
            return False
    
    def test_profile_access(self):
        """Test profile access after login"""
        print("👤 Testing profile access...")
        response = self.session.get(urljoin(self.base_url, '/profile'))
        
        if response.status_code == 200 and "User Profile" in response.text:
            print("✅ Profile accessible after login")
            return True
        else:
            print("❌ Profile access failed")
            return False
    
    def test_logout(self):
        """Test user logout"""
        print("🚪 Testing user logout...")
        response = self.session.get(urljoin(self.base_url, '/auth/logout'))
        
        if "logged out" in response.text or response.url.endswith('/'):
            print("✅ User logout successful")
            return True
        else:
            print("❌ User logout failed")
            return False
    
    def run_all_tests(self):
        """Run all authentication tests"""
        print("🧪 Starting Authentication System Tests\n")
        print("=" * 50)
        
        tests = [
            self.test_home_page,
            self.test_login_page,
            self.test_register_page,
            self.test_protected_redirect,
            self.test_registration,
            self.test_login,
            self.test_dashboard_access,
            self.test_profile_access,
            self.test_logout
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
                print()
            except Exception as e:
                print(f"❌ Test failed with error: {e}\n")
        
        print("=" * 50)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Authentication system is working correctly.")
        else:
            print("⚠️ Some tests failed. Please check the implementation.")
        
        return passed == total


if __name__ == '__main__':
    tester = AuthTester()
    tester.run_all_tests()