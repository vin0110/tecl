import os
import sys
import shutil
import subprocess
from subprocess import PIPE, CalledProcessError
import logging
import tempfile

from unittest import TestCase, SkipTest


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def emitTempfile(tempdir, module_name, entry_point, inputs):
    fp = tempfile.NamedTemporaryFile(dir=tempdir, suffix='.ecl', delete=False)
    logger.debug('tempfile: %s', fp.name)

    file_text = []
    # write preamble. need module name
    # in python3 write must be bytes. do conversation at end
    file_text.append('IMPORT %s;' % (module_name, ))
    file_text.append("")        # blank line

    # write inputs
    parameters = []
    for input in inputs:
        file_text.append('{} := {};'.format(input['name'], input['value']))
        parameters.append(input['name'])

    # write call
    file_text.append('result := {}.{}({});'.format(module_name, entry_point,
                                                   ', '.join(parameters)))
    file_text.append('OUTPUT(result);')
    file_text.append("")        # insert ending nl

    file_bytes = '\n'.join(file_text).encode('UTF-8')
    fp.write(file_bytes)
    fp.close()

    return fp.name


class EclTestCase(TestCase):
    def setUp(self):
        # do ecl stuff
        print('esetup')
        super(EclTestCase, self).setUp()

    def tearDown(self):
        # do ecl stuff
        print('eteardown')
        super(EclTestCase, self).tearDown()

    def invoke(self):
        tempdir = tempfile.mkdtemp()
        logger.debug('tempdir: %s', tempdir)

        try:
            temp_name = emitTempfile(tempdir,
                                     self.module,
                                     self.entry,
                                     getattr(self, 'parameters', []))
        except AttributeError as e:
            raise SkipTest(e)

        exec_name = os.path.join(tempdir, 'a.out')

        inc_list = getattr(self, 'includes', [])

        cmd_list = ['eclcc', '-o', exec_name, ]
        for inc in inc_list:
            cmd_list.append('-I')
            cmd_list.append(inc)
        cmd_list.append(temp_name)

        # compile program
        logger.debug('compiling: %s', ' '.join(cmd_list))
        compile = subprocess.run(cmd_list,
                                 stdout=PIPE, timeout=60)
        if compile.returncode != 0:
            raise SkipTest('compiling')

        # execute program
        logger.debug('executing: %s', exec_name)
        test_exec = subprocess.run([exec_name, ],
                                   stdout=PIPE, stderr=PIPE,
                                   timeout=getattr(self, 'timeout', 60))
        if test_exec.returncode != 0:
            raise self.test_case.failureException(test_exec.stderr)

        if getattr(self, 'cleanup', True):
            print('cleaning up', tempdir)
            shutil.rmtree(tempdir, ignore_errors=True)
        else:
            print('testing code saved in', tempdir)
        return test_exec.stdout

    def run(self, result=None):
        logger.debug('running test')

        # orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        testMethod()
        result.stopTest(self)
