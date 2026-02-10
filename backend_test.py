import requests
import sys
import json
from datetime import datetime

class ValentineProposalAPITester:
    def __init__(self, base_url="https://cutematch-1.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            details = f"Status: {response.status_code}"
            
            if not success:
                details += f" (Expected: {expected_status})"
                try:
                    error_data = response.json()
                    details += f" - {error_data}"
                except:
                    details += f" - {response.text[:200]}"

            self.log_test(name, success, details)
            
            if success:
                try:
                    return True, response.json()
                except:
                    return True, {}
            else:
                return False, {}

        except Exception as e:
            self.log_test(name, False, f"Exception: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test API root endpoint"""
        return self.run_test("API Root", "GET", "", 200)

    def test_create_proposal_valid(self):
        """Test creating a valid proposal"""
        data = {
            "valentine_name": "Alice",
            "custom_message": "Will you be my Valentine?",
            "character_choice": "panda"
        }
        success, response = self.run_test("Create Valid Proposal", "POST", "proposals", 200, data)
        
        if success and 'id' in response:
            # Store the ID for later tests
            self.proposal_id = response['id']
            return True, response
        return False, {}

    def test_create_proposal_minimal(self):
        """Test creating proposal with minimal data"""
        data = {
            "valentine_name": "Bob"
        }
        return self.run_test("Create Minimal Proposal", "POST", "proposals", 200, data)

    def test_create_proposal_invalid(self):
        """Test creating proposal with invalid data"""
        data = {
            "valentine_name": "",  # Empty name should fail
            "custom_message": "Test message"
        }
        success, _ = self.run_test("Create Invalid Proposal (Empty Name)", "POST", "proposals", 422, data)
        return success

    def test_get_proposal_valid(self):
        """Test getting a valid proposal"""
        if hasattr(self, 'proposal_id'):
            return self.run_test("Get Valid Proposal", "GET", f"proposals/{self.proposal_id}", 200)
        else:
            self.log_test("Get Valid Proposal", False, "No proposal ID available")
            return False, {}

    def test_get_proposal_invalid(self):
        """Test getting a non-existent proposal"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        return self.run_test("Get Invalid Proposal", "GET", f"proposals/{fake_id}", 404)

    def test_update_proposal_accept(self):
        """Test accepting a proposal"""
        if hasattr(self, 'proposal_id'):
            data = {"accepted": True}
            return self.run_test("Accept Proposal", "PATCH", f"proposals/{self.proposal_id}", 200, data)
        else:
            self.log_test("Accept Proposal", False, "No proposal ID available")
            return False, {}

    def test_update_proposal_reject(self):
        """Test rejecting a proposal"""
        if hasattr(self, 'proposal_id'):
            data = {"accepted": False}
            return self.run_test("Reject Proposal", "PATCH", f"proposals/{self.proposal_id}", 200, data)
        else:
            self.log_test("Reject Proposal", False, "No proposal ID available")
            return False, {}

    def test_list_proposals(self):
        """Test listing all proposals"""
        return self.run_test("List All Proposals", "GET", "proposals", 200)

    def test_status_endpoints(self):
        """Test status check endpoints"""
        # Create status check
        data = {"client_name": "test_client"}
        success1, _ = self.run_test("Create Status Check", "POST", "status", 200, data)
        
        # Get status checks
        success2, _ = self.run_test("Get Status Checks", "GET", "status", 200)
        
        return success1 and success2

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Valentine Proposal API Tests...")
        print(f"🔗 Testing API at: {self.api_url}")
        print("=" * 60)

        # Test sequence
        self.test_root_endpoint()
        self.test_create_proposal_valid()
        self.test_create_proposal_minimal()
        self.test_create_proposal_invalid()
        self.test_get_proposal_valid()
        self.test_get_proposal_invalid()
        self.test_update_proposal_accept()
        self.test_update_proposal_reject()
        self.test_list_proposals()
        self.test_status_endpoints()

        # Print summary
        print("=" * 60)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print("❌ Some tests failed!")
            failed_tests = [r for r in self.test_results if not r['success']]
            print("\nFailed tests:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['details']}")
            return 1

def main():
    tester = ValentineProposalAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())