from tabulate import tabulate
import json


class APITestReport:
    def __init__(self):
        self.results = []

    def add_result(self, test_name, url, method, status_code, response_time, response_body, error_message=None):
        result = {
            "Test Name": test_name,
            "URL": url,
            "Method": method,
            "Status Code": status_code,
            "Response Time (ms)": response_time,
            "Response Body": json.dumps(response_body)[:50] + "..." if isinstance(response_body,
                                                                                  dict) else response_body[:50] + "...",
            "Status": "PASS" if status_code < 400 else "FAIL",  # Determine Endpoint Status
            "Error Message": error_message if error_message else "N/A"
        }
        self.results.append(result)

    def generate_report(self):
        total_tests = len(self.results)
        passed_tests = len([result for result in self.results if result["Status"] == "PASS"])
        failed_tests = total_tests - passed_tests

        print("\nAPI Test Report")
        print(f"Total Tests: {total_tests}, Passed: {passed_tests}, Failed: {failed_tests}\n")

        if total_tests > 0:  # Verificar si hay resultados para informar
            # Asegúrate de que los encabezados estén en formato de lista
            headers = list(self.results[0].keys())
            # Convertir resultados en un formato adecuado para tabulate
            formatted_results = [[result[header] for header in headers] for result in self.results]
            print(tabulate(formatted_results, headers=headers, tablefmt='pretty'))
        else:
            print("No tests were executed.")


# Example
# report = APITestReport()
# report.add_result("Get User", "https://api.example.com/users/1", "GET", 200, 150, {"id": 1, "name": "John Doe"})
# report.add_result("Create User", "https://api.example.com/users", "POST", 201, 200, {"id": 2, "name": "Jane Doe"})
# report.add_result("Update User", "https://api.example.com/users/2", "PUT", 404, 180, {}, "User not found")
#
# Example Generate Report
# report.generate_report()
