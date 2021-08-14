import os
from abc import ABC, abstractmethod
from datetime import datetime
from random import choice

import psutil


class TestCase(ABC):
    def __init__(self, tc_id, name):
        self.tc_id = tc_id
        self.name = name

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
    UNIX_TIME = datetime(1970, 1, 1)

    def __init__(self):
        super().__init__(tc_id='tc01', name='list_files')
        self._seconds_from_unix = -1

    def __repr__(self):
        return f'{self.tc_id} {self.name}'

    def _prep(self):
        passed_time = datetime.utcnow() - self.UNIX_TIME
        self.seconds_from_unix = int(passed_time.total_seconds())
        return self.seconds_from_unix % 2 == 0

    def _run(self):
        home_directory = os.path.expanduser('~')
        for file in os.listdir(home_directory):
            print(file)

    def _clean_up(self):
        pass

    def execute(self):
        if self._prep():
            self._run()
            self._clean_up()
        else:
            print(
                f"Couldn't list files since {self.seconds_from_unix} which is the number of seconds from the "
                f"beginning of the Unix epoch is not divisible by 2"
            )


class RandomFileTestCase(TestCase):
    BYTES_TO_KB = pow(10, -9)  # 0.000_000_001
    MIN_REQUIRED_RAM = 1  # in GB
    FILE_SIZE = 10241000  # in bytes
    FILE_CONTENT = '#!?'
    FILE_CONTENT_JOINER = ''

    def __init__(self):
        super().__init__(tc_id='tc02', name='random_file')
        self._file = 'test.txt'

    def __repr__(self):
        return f'{self.tc_id} {self.name}'

    def _prep(self):
        memory_info = psutil.virtual_memory()
        ram = memory_info.total * self.BYTES_TO_KB
        return int(ram) > self.MIN_REQUIRED_RAM

    def _run(self):
        content_symbols = [choice(self.FILE_CONTENT) for _ in range(self.FILE_SIZE)]
        content = self.FILE_CONTENT_JOINER.join(content_symbols)
        with open(self._file, 'w') as file:
            file.write(content)

    def _clean_up(self):
        file_path = os.path.join(self._file)
        file_full_path = os.path.abspath(file_path)
        if os.path.isfile(file_full_path):
            os.remove(file_full_path)

    def execute(self):
        if self._prep():
            print('test.txt file is creating...')
            self._run()
            print('test.txt file is created')

            print('test.txt file is deleting...')
            self._clean_up()
            print('test.txt file is deleted successfully!')
        else:
            print('System RAM is less than 1 GB')


class TestSuite:
    def __init__(self):
        self._test_cases = []

    def add_test_case(self, test_case):
        self._test_cases.append(test_case)

    def add_test_cases(self, test_cases):
        self._test_cases.extend(test_cases)

    def run_cases(self):
        for test_case in self._test_cases:
            print(f'{test_case} case is running...')
            test_case.execute()
            print(f'Execution of {test_case} passed successfully')
            print('-' * 60)


if __name__ == '__main__':
    suite = TestSuite()
    suite.add_test_cases([
        ListFilesTestCase(),
        RandomFileTestCase(),
    ])
    suite.run_cases()
