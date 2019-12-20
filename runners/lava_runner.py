#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import unittest

from tests.cros_ec_accel import *
from tests.cros_ec_gyro import *
from tests.cros_ec_mcu import *
from tests.cros_ec_pwm import *
from tests.cros_ec_rtc import *
from tests.cros_ec_power import *
from tests.cros_ec_extcon import *


class LavaTextTestResult(unittest.TestResult):
    def __init__(self, runner):
        unittest.TestResult.__init__(self)
        self.runner = runner

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        self.runner.writeUpdate(
            "<LAVA_SIGNAL_TESTCASE TEST_CASE_ID=%s RESULT=pass>\n" % test.id()
        )

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        self.runner.writeUpdate(
            "<LAVA_SIGNAL_TESTCASE TEST_CASE_ID=%s RESULT=unknown>\n" % test.id()
        )

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        self.runner.writeUpdate(
            "<LAVA_SIGNAL_TESTCASE TEST_CASE_ID=%s RESULT=fail>\n" % test.id()
        )

    def addSkip(self, test, reason):
        unittest.TestResult.addSkip(self, test, reason)
        self.runner.writeUpdate(
            "<LAVA_SIGNAL_TESTCASE TEST_CASE_ID=%s RESULT=skip>\n" % test.id()
        )


class LavaTestRunner:
    def __init__(self, stream=sys.stderr, verbosity=0):
        self.stream = stream
        self.verbosity = verbosity

    def writeUpdate(self, message):
        self.stream.write(message)

    def run(self, test):
        result = LavaTextTestResult(self)
        test(result)
        result.testsRun
        return result


if __name__ == "__main__":
    unittest.main(
        testRunner=LavaTestRunner(),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False,
        buffer=False,
        catchbreak=False,
    )
