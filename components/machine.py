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

    def configure_tools(self, tools_list, **kwargs):
        for item in tools_list:
            tool = Tool(**item)
            # install tool
            if tool.install_cmd:
                self.run_cmd(tool.install_cmd)
            else:
                self.install_util(tool.name, **kwargs)
            # setup configuration file
            self.run_cmd('{2} {0} {1}'.format(
                tool.conf_input,
                tool.conf_output,
                'ln' if tool.link_conf else 'cp'))


class Tool:

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.conf_input = kwargs.get('conf_input')
        self.conf_output = kwargs.get('conf_output', '~')
        self.link_conf = kwargs.get('link_conf')
        self.install_cmd = kwargs.get('install_cmd')
        self.pkg_manager = kwargs.get('pkg_manager')
