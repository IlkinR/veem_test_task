import os
from abc import ABC, abstractmethod
from datetime import datetime
from random import choice

import psutil


class SecondsSinceUnixNotEven(Exception):
    """ Exception class for handling errors related to total seconds passed since unix time (January 01 1970)."""

    def __init__(self, passed_seconds):
        self.passed_seconds = passed_seconds

    def __repr__(self):
        return '{exception}: {seconds} % 2 == 0, since remainder is {remainder}'.format(
            exception=self.__class__.__name__,
            seconds=self.passed_seconds,
            remainder=self.passed_seconds % 2
        )


class SystemRAMLessThanOneGB(Exception):
    """ Exception class for handling errors related to RAM of system of the user """

    def __init__(self, system_ram):
        self.system_ram = system_ram

    def __repr__(self):
        return '{exception}: {seconds} Gb < 1 Gb '.format(
            exception=self.__class__.__name__,
            seconds=self.system_ram,
        )


class TestCase(ABC):
    """ An interface for all test cases"""

    def __init__(self, tc_id, name):
        self._tc_id = tc_id
        self._name = name

    @property
    def tc_id(self):
        return self._tc_id

    @property
    def name(self):
        return self._name

    @abstractmethod
    def _prep(self):
        raise NotImplementedError

    @abstractmethod
    def _run(self):
        raise NotImplementedError

    @abstractmethod
    def _clean_up(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class ListFilesTestCase(TestCase):
    """ Test case responsible for listing files in the user home directory if the number of seconds passed from unix
    time is even """

    UNIX_TIME = datetime(1970, 1, 1)

    def __init__(self):
        super().__init__(tc_id='tc01', name='list_files')
        self._seconds_from_unix = -1

    def __repr__(self):
        return f'{self.tc_id} {self.name}'

    def _prep(self):
        """ Checks if seconds from unix time is even. ALso assign the value for seconds_from_unix attribute """
        passed_time = datetime.utcnow() - self.UNIX_TIME
        seconds_from_unix = int(passed_time.total_seconds())
        self.seconds_from_unix = seconds_from_unix
        return seconds_from_unix % 2 == 0

    def _run(self):
        """ Print all files to terminal is home directory of the user """
        home_directory = os.path.expanduser('~')
        all_files = os.listdir(home_directory)
        for file in all_files:
            print(file)

    def _clean_up(self):
        pass

    def execute(self):
        """ Executes test case """
        if not self._prep():
            raise SecondsSinceUnixNotEven(self.seconds_from_unix)
        self._run()
        self._clean_up()


class RandomFileTestCase(TestCase):
    """ Test case responsible for creating a text.txt file with random content and immediately deleting it """

    BYTES_TO_KB = pow(10, -9)  # used to convert bytes to kb
    MIN_REQUIRED_RAM = 1  # minimum ram required for running test case
    FILE_SIZE = 10241000  # size of created file in bytes
    FILE_CONTENT = '#!?'  # symbols to fill file.
    FILE_CONTENT_JOINER = ''  # symbol to converting symbols to one big string

    def __init__(self):
        super().__init__(tc_id='tc02', name='random_file')
        self._file = 'test.txt'
        self._system_ram = -1

    def __repr__(self):
        return f'{self.tc_id} {self.name}'

    def _prep(self):
        """ Checks if system ram is greater than 1 Gb"""
        memory_info = psutil.virtual_memory()
        ram = memory_info.total * self.BYTES_TO_KB
        self._system_ram = ram
        return int(ram) > self.MIN_REQUIRED_RAM

    def _run(self):
        """ Creates files with random content """
        content_symbols = [choice(self.FILE_CONTENT) for _ in range(self.FILE_SIZE)]
        content = self.FILE_CONTENT_JOINER.join(content_symbols)
        with open(self._file, 'w') as file:
            file.write(content)

    def _clean_up(self):
        """ Deletes file from system """
        file_path = os.path.join(self._file)
        file_full_path = os.path.abspath(file_path)
        if os.path.isfile(file_full_path):
            os.remove(file_full_path)

    def execute(self):
        """ Executes test cases """
        if not self._prep():
            raise SystemRAMLessThanOneGB(self._system_ram)
        print('test.txt file is creating...')
        self._run()
        print('test.txt file is created :)')
        print('test.txt file is deleting...')
        self._clean_up()
        print('test.txt file is deleted successfully :)')


class TestSuite:
    """ Our testing system. It accepts the test cases implementing TestCase interface and runs them one by one """

    def __init__(self, test_cases=None):
        if test_cases is None:
            self._test_cases = []
        self._test_cases = test_cases

    def __getitem__(self, position):
        return self._test_cases[position]

    def __len__(self):
        return len(self._test_cases)

    def add_test_case(self, test_case):
        """ Add a test case """
        TestSuite.__TOTAL_TEST_CASES += 1
        self._test_cases.append(test_case)

    def add_test_cases(self, test_cases):
        """ Add several test cases """
        TestSuite.__TOTAL_TEST_CASES += len(test_cases)
        self._test_cases.extend(test_cases)

    def run_cases(self):
        """ Runs our testing system containing multiple test cases """
        for test_case in self._test_cases:
            try:
                print(f'{test_case} case is running...')
                test_case.execute()
                print(f'Execution of {test_case} passed successfully :)')
            except (SecondsSinceUnixNotEven, SystemRAMLessThanOneGB) as exc:
                print(f'{test_case} is failed :(')
                print(repr(exc))
            print('-' * 60)


if __name__ == '__main__':
    suite = TestSuite([ListFilesTestCase(), RandomFileTestCase()])
    print(suite.test_cases_count)
    print(len(suite))
    print(suite[0])
