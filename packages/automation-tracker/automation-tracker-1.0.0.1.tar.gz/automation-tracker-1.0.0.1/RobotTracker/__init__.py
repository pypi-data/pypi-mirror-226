try:
    from robot.libraries.BuiltIn import BuiltIn
    from robot.libraries.BuiltIn import _Misc
    import robot.api.logger as logger
    from robot.api.deco import keyword

    import requests
    import uuid

    ROBOT = False

except Exception:
    ROBOT = False


def __init__(self, baseUrl):
    self.baseURl = baseUrl


def generate_guid(self):
    global random_guid
    random_guid = str(uuid.uuid4())
    return random_guid


def TrackTestCase(self, testCaseName, testCaseStatus, projName, userName, crqRef, uniqueRunRef):
    # create body
    body = {
        "TestCaseName": testCaseName,
        "TestCaseStatus": testCaseStatus,
        "TestCaseGuid": uniqueRunRef,
        "ProjectName": projName,
        "UserName": userName,
        "CRQRef": crqRef
    }

    BuiltIn().log_to_console(f"sending Body: {body}")

    # send POST request with body
    resp = requests.post(self.baseURl + "/api/Tracking/TrackTestCaseDetails", json=body,
                         timeout=10000)
    # get response
    BuiltIn().log_to_console(f"Response Code: {resp.status_code}, Response: {resp.text}")


def manually_start_tracker_detailed(_self, proj_name, username, environment, crq_ref, squad, testType, platform,
                                    testcases_executed, testcases_passed, testcases_failed,
                                    total_testcases_executed, testcases_blocked, testcases_no_run,
                                    testcases_not_completed, critical_defects, major_defects, medium_defects,
                                    low_defects, automated_tests, manual_tests, non_functional_tests,
                                    functional_tests, tracking_testcase_reference):
    proj_name = proj_name
    username = username
    environment = environment
    crq_ref = crq_ref
    squad = squad
    testType = testType
    platform = platform
    testcases_executed = testcases_executed
    testcases_passed = testcases_passed
    testcases_failed = testcases_failed
    total_testcases_executed = total_testcases_executed
    testcases_blocked = testcases_blocked
    testcases_no_run = testcases_no_run
    testcases_not_completed = testcases_not_completed
    critical_defects = critical_defects
    major_defects = major_defects
    medium_defects = medium_defects
    low_defects = low_defects
    automated_tests = automated_tests
    manual_tests = manual_tests
    non_functional_tests = non_functional_tests
    functional_tests = functional_tests
    trackingRef = tracking_testcase_reference

    # send REQ
    url = _self.baseURl + "/api/Tracking/TrackProjectCounter?proj=" + str(proj_name) + "&username=" + str(
        username) + "&ttl_testcases_run=" + str(testcases_executed) + "&env=" + str(environment) + "&crq=" + str(
        crq_ref) + "&squad=" + str(squad) + "&executed_testcases=" + str(
        total_testcases_executed) + "&passed_testcases=" + str(testcases_passed) + "&failed_testcases=" + str(
        testcases_failed) + "&blocked_testcases=" + str(testcases_blocked) + "&norun_testcases=" + str(
        testcases_no_run) + "&notcompleted_testcases=" + str(testcases_not_completed) + "&critical_defects=" + str(
        critical_defects) + "&major_defects=" + str(major_defects) + "&medium_defects=" + str(
        medium_defects) + "&low_defects=" + str(low_defects) + "&automated_tests=" + str(
        automated_tests) + "&manual_tests=" + str(manual_tests) + "&functional_tests=" + str(
        functional_tests) + "&non_functional_tests=" + str(non_functional_tests) + "&test_type=" + str(
        testType) + "&platform=" + str(platform) + "&tracking_testcase_ref=" + str(trackingRef)

    resp = requests.get(url, timeout=10000)

    BuiltIn().log_to_console(f"Response Code: {resp.status_code}, Response: {resp.text}")
    BuiltIn().log_to_console(f"Response Data: {resp.text}")

    if resp.status_code == 200:
        BuiltIn().log_to_console(f"Tracker closed successfully")

    else:
        BuiltIn().log_to_console(f"Tracker closed unsuccessfully")

    # return data
    return resp.status_code
