#!/usr/bin/env python3
"""
Simple RBAC System Test for AMR Control System
Tests core functionality with proper session handling
"""

import requests
import json
import time
from datetime import datetime

class SimpleRBACTest:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, status, details=""):
        """Log test results with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = {
            "timestamp": timestamp,
            "test": test_name,
            "status": status,
            "details": details
        }
        self.test_results.append(result)
        
        # Print with emoji
        emoji = "✅" if status == "PASS" else "❌"
        print(f"{emoji} {timestamp} - {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_basic_access(self):
        """Test basic access control"""
        try:
            # Test homepage redirect when not logged in
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 302 and "/login" in response.headers.get("Location", ""):
                self.log_test("Homepage Redirect", "PASS", "Redirects to login when not authenticated")
            else:
                self.log_test("Homepage Redirect", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Homepage Redirect", "FAIL", str(e))
    
    def test_admin_login(self):
        """Test admin user login and access"""
        try:
            # Login as admin
            login_data = {"username": "admin", "password": "123"}
            response = self.session.post(f"{self.base_url}/login", data=login_data, allow_redirects=False)
            
            if response.status_code == 302:
                # Follow redirect to dashboard
                dashboard_response = self.session.get(f"{self.base_url}/")
                if dashboard_response.status_code == 200:
                    self.log_test("Admin Login", "PASS", "Admin login successful")
                    
                    # Test admin-specific access
                    admin_response = self.session.get(f"{self.base_url}/admin")
                    if admin_response.status_code == 200:
                        self.log_test("Admin Access", "PASS", "Admin can access admin page")
                    else:
                        self.log_test("Admin Access", "FAIL", f"Status: {admin_response.status_code}")
                else:
                    self.log_test("Admin Login", "FAIL", f"Dashboard access failed: {dashboard_response.status_code}")
            else:
                self.log_test("Admin Login", "FAIL", f"Login failed: {response.status_code}")
        except Exception as e:
            self.log_test("Admin Login", "FAIL", str(e))
    
    def test_operator_login(self):
        """Test operator user login and access"""
        try:
            # Logout first
            self.session.get(f"{self.base_url}/logout")
            
            # Login as operator
            login_data = {"username": "operator", "password": "operator123"}
            response = self.session.post(f"{self.base_url}/login", data=login_data, allow_redirects=False)
            
            if response.status_code == 302:
                # Follow redirect to dashboard
                dashboard_response = self.session.get(f"{self.base_url}/")
                if dashboard_response.status_code == 200:
                    self.log_test("Operator Login", "PASS", "Operator login successful")
                    
                    # Test operator access to database (should work)
                    db_response = self.session.get(f"{self.base_url}/database")
                    if db_response.status_code == 200:
                        self.log_test("Operator Database Access", "PASS", "Operator can access database")
                    else:
                        self.log_test("Operator Database Access", "FAIL", f"Status: {db_response.status_code}")
                    
                    # Test operator access to admin (should fail)
                    admin_response = self.session.get(f"{self.base_url}/admin")
                    if admin_response.status_code in [302, 401, 403]:
                        self.log_test("Operator Admin Restriction", "PASS", "Operator correctly restricted from admin")
                    else:
                        self.log_test("Operator Admin Restriction", "FAIL", f"Status: {admin_response.status_code}")
                else:
                    self.log_test("Operator Login", "FAIL", f"Dashboard access failed: {dashboard_response.status_code}")
            else:
                self.log_test("Operator Login", "FAIL", f"Login failed: {response.status_code}")
        except Exception as e:
            self.log_test("Operator Login", "FAIL", str(e))
    
    def test_viewer_login(self):
        """Test viewer user login and access"""
        try:
            # Logout first
            self.session.get(f"{self.base_url}/logout")
            
            # Login as viewer
            login_data = {"username": "viewer", "password": "viewer123"}
            response = self.session.post(f"{self.base_url}/login", data=login_data, allow_redirects=False)
            
            if response.status_code == 302:
                # Follow redirect to dashboard
                dashboard_response = self.session.get(f"{self.base_url}/")
                if dashboard_response.status_code == 200:
                    self.log_test("Viewer Login", "PASS", "Viewer login successful")
                    
                    # Test viewer access to database (should fail)
                    db_response = self.session.get(f"{self.base_url}/database")
                    if db_response.status_code in [302, 401, 403]:
                        self.log_test("Viewer Database Restriction", "PASS", "Viewer correctly restricted from database")
                    else:
                        self.log_test("Viewer Database Restriction", "FAIL", f"Status: {db_response.status_code}")
                    
                    # Test viewer access to admin (should fail)
                    admin_response = self.session.get(f"{self.base_url}/admin")
                    if admin_response.status_code in [302, 401, 403]:
                        self.log_test("Viewer Admin Restriction", "PASS", "Viewer correctly restricted from admin")
                    else:
                        self.log_test("Viewer Admin Restriction", "FAIL", f"Status: {admin_response.status_code}")
                else:
                    self.log_test("Viewer Login", "FAIL", f"Dashboard access failed: {dashboard_response.status_code}")
            else:
                self.log_test("Viewer Login", "FAIL", f"Login failed: {response.status_code}")
        except Exception as e:
            self.log_test("Viewer Login", "FAIL", str(e))
    
    def test_package_delivery(self):
        """Test package delivery with numeric level conversion"""
        try:
            # Login as admin for full access
            self.session.get(f"{self.base_url}/logout")
            login_data = {"username": "admin", "password": "123"}
            self.session.post(f"{self.base_url}/login", data=login_data, allow_redirects=False)
            
            # Test package delivery with different levels
            packages = [
                {"id": "PKG001", "level": "level1", "expected": 1},
                {"id": "PKG002", "level": "level2", "expected": 2},
                {"id": "PKG003", "level": "level3", "expected": 3}
            ]
            
            for package in packages:
                delivery_data = {
                    "package_id": package["id"],
                    "target_x": 5.2649,
                    "target_y": -1.01,
                    "target_theta": -2.29,
                    "level": package["level"]
                }
                
                response = self.session.post(f"{self.base_url}/deliver_package", json=delivery_data)
                if response.status_code == 200:
                    try:
                        result = response.json()
                        if "target" in result and "level" in result["target"]:
                            actual_level = result["target"]["level"]
                            if actual_level == package["expected"]:
                                self.log_test(f"Package {package['id']} Delivery", "PASS", 
                                            f"{package['level']} -> {package['expected']}")
                            else:
                                self.log_test(f"Package {package['id']} Delivery", "FAIL", 
                                            f"Expected {package['expected']}, got {actual_level}")
                        else:
                            self.log_test(f"Package {package['id']} Delivery", "FAIL", "No level in response")
                    except json.JSONDecodeError:
                        self.log_test(f"Package {package['id']} Delivery", "FAIL", "Invalid JSON response")
                else:
                    self.log_test(f"Package {package['id']} Delivery", "FAIL", f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Package Delivery", "FAIL", str(e))
    
    def test_unauthorized_access(self):
        """Test unauthorized access to protected endpoints"""
        try:
            # Ensure we're logged out
            self.session.get(f"{self.base_url}/logout")
            
            # Test access to protected endpoints without login
            protected_endpoints = [
                ("/", "GET"),
                ("/admin", "GET"),
                ("/database", "GET"),
                ("/deliver_package", "POST")
            ]
            
            for endpoint, method in protected_endpoints:
                if method == "POST":
                    response = self.session.post(f"{self.base_url}{endpoint}", json={})
                else:
                    response = self.session.get(f"{self.base_url}{endpoint}")
                
                if response.status_code in [302, 401, 403]:
                    self.log_test(f"Unauthorized {endpoint}", "PASS", f"Status: {response.status_code}")
                else:
                    self.log_test(f"Unauthorized {endpoint}", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Unauthorized Access", "FAIL", str(e))
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🧪 Simple RBAC System Test")
        print("=" * 40)
        print()
        
        # Basic functionality tests
        self.test_basic_access()
        
        # User authentication and authorization tests
        self.test_admin_login()
        self.test_operator_login()
        self.test_viewer_login()
        
        # Package delivery with numeric level conversion
        self.test_package_delivery()
        
        # Security tests
        self.test_unauthorized_access()
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("📊 Test Summary")
        print("=" * 40)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['details']}")
        
        print("\n🎯 RBAC System Status:")
        if failed_tests == 0:
            print("✅ COMPLETE - All tests passed!")
            print("✅ Role-based access control working correctly")
            print("✅ User authentication functioning")
            print("✅ Numeric level conversion implemented")
            print("✅ Security measures in place")
        else:
            print("⚠️  PARTIAL - Some tests failed")
            print("Please review failed tests above")

if __name__ == "__main__":
    test_suite = SimpleRBACTest()
    test_suite.run_all_tests() 