#!/usr/bin/env python3
"""
Complete RBAC System Test for AMR Control System
Tests user authentication, role-based access, and numeric level conversion
"""

import requests
import json
import time
from datetime import datetime

class RBACSystemTest:
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
    
    def test_homepage_redirect(self):
        """Test homepage redirects to login"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 302 and "/login" in response.headers.get("Location", ""):
                self.log_test("Homepage Redirect", "PASS", "Redirects to /login")
            else:
                self.log_test("Homepage Redirect", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Homepage Redirect", "FAIL", str(e))
    
    def test_login_page(self):
        """Test login page accessibility"""
        try:
            response = self.session.get(f"{self.base_url}/login")
            if response.status_code == 200 and "Login" in response.text:
                self.log_test("Login Page", "PASS", "Login page accessible")
            else:
                self.log_test("Login Page", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Login Page", "FAIL", str(e))
    
    def test_admin_login(self):
        """Test admin user login"""
        try:
            login_data = {"username": "admin", "password": "123"}
            response = self.session.post(f"{self.base_url}/login", data=login_data)
            if response.status_code == 302 and "/" in response.headers.get("Location", ""):
                self.log_test("Admin Login", "PASS", "Admin login successful")
            else:
                self.log_test("Admin Login", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Admin Login", "FAIL", str(e))
    
    def test_dashboard_access(self):
        """Test dashboard access after login"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200 and "AMR Control" in response.text:
                self.log_test("Dashboard Access", "PASS", "Dashboard accessible")
            else:
                self.log_test("Dashboard Access", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Dashboard Access", "FAIL", str(e))
    
    def test_admin_permissions(self):
        """Test admin user permissions"""
        try:
            response = self.session.get(f"{self.base_url}/")
            content = response.text
            
            # Check for admin-specific features (these should be available in the main dashboard)
            admin_features = [
                "AMR Control",
                "Manual Control",
                "Database",
                "Admin"
            ]
            
            missing_features = []
            for feature in admin_features:
                if feature not in content:
                    missing_features.append(feature)
            
            if not missing_features:
                self.log_test("Admin Permissions", "PASS", "All admin features present")
            else:
                self.log_test("Admin Permissions", "FAIL", f"Missing: {', '.join(missing_features)}")
        except Exception as e:
            self.log_test("Admin Permissions", "FAIL", str(e))
    
    def test_operator_login(self):
        """Test operator user login"""
        try:
            # First logout
            self.session.get(f"{self.base_url}/logout")
            
            login_data = {"username": "operator", "password": "operator123"}
            response = self.session.post(f"{self.base_url}/login", data=login_data)
            if response.status_code == 302 and "/" in response.headers.get("Location", ""):
                self.log_test("Operator Login", "PASS", "Operator login successful")
            else:
                self.log_test("Operator Login", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Operator Login", "FAIL", str(e))
    
    def test_operator_permissions(self):
        """Test operator user permissions"""
        try:
            response = self.session.get(f"{self.base_url}/")
            content = response.text
            
            # Check for operator-specific features
            operator_features = [
                "AMR Control",
                "Manual Control",
                "Database"
            ]
            
            # Check for restricted features (should NOT be present)
            restricted_features = [
                "Admin"
            ]
            
            missing_features = []
            for feature in operator_features:
                if feature not in content:
                    missing_features.append(feature)
            
            present_restricted = []
            for feature in restricted_features:
                if feature in content:
                    present_restricted.append(feature)
            
            if not missing_features and not present_restricted:
                self.log_test("Operator Permissions", "PASS", "Correct permissions applied")
            else:
                details = []
                if missing_features:
                    details.append(f"Missing: {', '.join(missing_features)}")
                if present_restricted:
                    details.append(f"Should not have: {', '.join(present_restricted)}")
                self.log_test("Operator Permissions", "FAIL", "; ".join(details))
        except Exception as e:
            self.log_test("Operator Permissions", "FAIL", str(e))
    
    def test_viewer_login(self):
        """Test viewer user login"""
        try:
            # First logout
            self.session.get(f"{self.base_url}/logout")
            
            login_data = {"username": "viewer", "password": "viewer123"}
            response = self.session.post(f"{self.base_url}/login", data=login_data)
            if response.status_code == 302 and "/" in response.headers.get("Location", ""):
                self.log_test("Viewer Login", "PASS", "Viewer login successful")
            else:
                self.log_test("Viewer Login", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Viewer Login", "FAIL", str(e))
    
    def test_viewer_permissions(self):
        """Test viewer user permissions"""
        try:
            response = self.session.get(f"{self.base_url}/")
            content = response.text
            
            # Check for viewer-specific features (limited access)
            viewer_features = [
                "AMR Control"
            ]
            
            # Check for restricted features (should NOT be present)
            restricted_features = [
                "Manual Control",
                "Database",
                "Admin"
            ]
            
            missing_features = []
            for feature in viewer_features:
                if feature not in content:
                    missing_features.append(feature)
            
            present_restricted = []
            for feature in restricted_features:
                if feature in content:
                    present_restricted.append(feature)
            
            if not missing_features and not present_restricted:
                self.log_test("Viewer Permissions", "PASS", "Correct permissions applied")
            else:
                details = []
                if missing_features:
                    details.append(f"Missing: {', '.join(missing_features)}")
                if present_restricted:
                    details.append(f"Should not have: {', '.join(present_restricted)}")
                self.log_test("Viewer Permissions", "FAIL", "; ".join(details))
        except Exception as e:
            self.log_test("Viewer Permissions", "FAIL", str(e))
    
    def test_numeric_level_conversion(self):
        """Test numeric level conversion in package delivery"""
        try:
            # Login as admin to access all features
            self.session.get(f"{self.base_url}/logout")
            login_data = {"username": "admin", "password": "123"}
            self.session.post(f"{self.base_url}/login", data=login_data)
            
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
                    result = response.json()
                    if "level" in result.get("target", {}) and result["target"]["level"] == package["expected"]:
                        self.log_test(f"Numeric Level {package['id']}", "PASS", 
                                    f"{package['level']} -> {package['expected']}")
                    else:
                        self.log_test(f"Numeric Level {package['id']}", "FAIL", 
                                    f"Expected {package['expected']}, got {result.get('target', {}).get('level', 'N/A')}")
                else:
                    self.log_test(f"Numeric Level {package['id']}", "FAIL", f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Numeric Level Conversion", "FAIL", str(e))
    
    def test_unauthorized_access(self):
        """Test unauthorized access to restricted endpoints"""
        try:
            # Test without login
            self.session.get(f"{self.base_url}/logout")
            
            restricted_endpoints = [
                "/",
                "/deliver_package",
                "/admin",
                "/database"
            ]
            
            for endpoint in restricted_endpoints:
                if endpoint == "/deliver_package":
                    response = self.session.post(f"{self.base_url}{endpoint}", json={})
                else:
                    response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code in [302, 401, 403]:  # Redirect or unauthorized
                    self.log_test(f"Unauthorized {endpoint}", "PASS", f"Status: {response.status_code}")
                else:
                    self.log_test(f"Unauthorized {endpoint}", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Unauthorized Access", "FAIL", str(e))
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🧪 Complete RBAC System Test")
        print("=" * 50)
        print()
        
        # Basic functionality tests
        self.test_homepage_redirect()
        self.test_login_page()
        
        # Admin user tests
        self.test_admin_login()
        self.test_dashboard_access()
        self.test_admin_permissions()
        
        # Operator user tests
        self.test_operator_login()
        self.test_operator_permissions()
        
        # Viewer user tests
        self.test_viewer_login()
        self.test_viewer_permissions()
        
        # Numeric level conversion tests
        self.test_numeric_level_conversion()
        
        # Security tests
        self.test_unauthorized_access()
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("📊 Test Summary")
        print("=" * 50)
        
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
    test_suite = RBACSystemTest()
    test_suite.run_all_tests() 