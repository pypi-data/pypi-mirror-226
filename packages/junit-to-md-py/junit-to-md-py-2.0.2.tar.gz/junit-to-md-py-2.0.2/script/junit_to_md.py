import argparse
from lxml import etree


def main():
    parser = argparse.ArgumentParser(
        prog="junit-to-md-py",
        description="Converts JUnit XML report to markdown format",
    )
    parser.add_argument("file", help="Path to the JUnit XML report file")
    parser.add_argument(
        "--cmd-format",
        dest="cmd_format",
        help="Special formatting in case of using the output with cmd commands",
        action="store_true",
    )
    args = parser.parse_args()

    failedTestDetails = []
    allTests = []

    try:
        xmlDoc = etree.parse(args.file)
    except Exception:
        print(f"Error parsing the text from junitOutput!")
        return

    suites = xmlDoc.xpath("//testsuite")
    for suite in suites:
        tests = suite.xpath(".//testcase")
        for test in tests:
            allTests.append(test)
            failures = test.xpath(".//failure")
            for failure in failures:
                failedTestDetails.append(
                    suite.get("name")
                    + "/"
                    + test.get("name")
                    + "\n\n\\`\\`\\`\n" if args.cmd_format else "\n\n```\n"
                    + failure.text.strip().replace("\n", "").replace("\r", "")
                    + "\n\\`\\`\\`" if args.cmd_format else "\n```"
                )

    if failedTestDetails:
        returnMsg = "### Detected Vulnerabilities:\n"
        for failure in failedTestDetails:
            returnMsg += "- " + failure + "\n"
        print(returnMsg)
    else:
        print("")
