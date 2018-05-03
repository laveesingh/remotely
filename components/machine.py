import shlex
import subprocess
import sys


class Machine:

    def __init__(self, *args, **kwargs):
        pass

    def run_cmd(self, cmd_str, **kwargs):
        args = shlex.split(cmd_str)
        if kwargs.get('capture', False):
            process = subprocess.Popen(args, stdout=subprocess.PIPE)
            process.wait()
            output = process.stdout.read()
            return output.decode('utf-8')
        else:
            process = subprocess.Popen(args, stdout=sys.stdout)
            process.wait()

    def install_util(self, tools_list, **kwargs):
        pkg_manager = kwargs.pkg_manager if kwargs.pkg_manager else 'apt'
        tools_str = ' '.join(tools_list)
        apt_command = 'sudo {0} install -y {1}'.format(pkg_manager, tools_str)
        self.run_cmd(apt_command)

    def apt_install(self, tools_list, **kwargs):
        self.install_util(tools_list, pkg_manager='apt')

    def pip_install(self, tools_list, **kwargs):
        self.install_util(tools_list, pkg_manager='pip')

    def npm_install(self, tools_list, **kwargs):
        self.install_util(tools_list, pkg_manager='npm')
