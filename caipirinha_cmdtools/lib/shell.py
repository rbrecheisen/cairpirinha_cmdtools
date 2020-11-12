import os
import cmd2
import numpy as np


class Result(object):

    def __init__(self, data, name):
        self.data = data
        self.name = name
        self.description = None


class ResultManager(object):

    def __init__(self):
        self.results = {}
        self.current_result = None
        self.result_idx = -1

    def next_result_idx(self):
        self.result_idx += 1
        return self.result_idx

    def add_result_data(self, data):
        name = 'result_{}'.format(self.next_result_idx())
        result = Result(data, name)
        self.results[name] = result
        self.current_result = self.results[name]

    def remove_result_data(self, name):
        self.current_result = self.results['result_0']
        del self.results[name]

    def get_current_result_data(self):
        return self.current_result.data

    def set_current_result(self, name):
        self.current_result = self.results[name]

    def set_result_description(self, name, description):
        self.results[name].description = description

    def undo(self):
        name = self.current_result.name
        index = int(name.split('_')[1])
        index = np.minimum(0, index-1)
        name = 'result_{}'.format(index)
        self.current_result = self.results[name]

    def redo(self):
        name = self.current_result.name
        index = int(name.split('_')[1])
        index = np.maximum(index+1, len(self.results.keys()))
        name = 'result_{}'.format(index)
        self.current_result = self.results[name]

    def show_results(self):
        current = ''
        for result in self.results.values():
            if result.name == self.current_result.name:
                current = '[current]'
            print('{}: description = {} {}'.format(result.name, result.description, current))


class BasicShell(cmd2.Cmd):

    def __init__(self):
        super(BasicShell, self).__init__()
        self.result_manager = ResultManager()
        self.current_dir = os.path.abspath(os.path.curdir)
        self.intro = 'Put your intro inside a global variable INTRO'
        self.prompt = '(shell) '

    def add_result(self, data):
        """
        Usage: add_result <data>
        Add <data> as a new result set to the result manager.
        """
        self.result_manager.add_result_data(data)

    def remove_result(self, name):
        """
        Usage: remove_result <result name>
        Remove result <name> from list of result sets.
        """
        self.result_manager.remove_result_data(name)

    def do_cd(self, line):
        """
        Usage: cd <dir path>
        Change the current directory to <dir path>.
        """
        if line == '.' or line == '':
            self.do_pwd(None)
            return
        if line == '..':
            self.current_dir = os.path.split(self.current_dir)[0]
            self.do_pwd(None)
            return
        if not os.path.isdir(line):
            line = os.path.join(self.current_dir, line)
            if not os.path.isdir(line):
                self.poutput('Directory {} is not a valid directory'.format(line))
                return
        self.current_dir = line
        self.do_pwd(None)

    def do_ls(self, _):
        """
        Usage: ls
        Lists the contents of the current directory. Same as shell command "!ls -lap".
        """
        self.do_shell('cd {}; ls -lap'.format(self.current_dir))

    def do_pwd(self, _):
        """
        Usage: pwd
        Show the current directory.
        """
        self.poutput(self.current_dir)

    def do_shell(self, line):
        """
        Usage: !<command>
        Execute shell command <command>. For example, !echo $HOME will display the user's HOME directory.
        """
        if line is None or line is '':
            self.poutput('Please specify a shell command preceded by! For example, !echo $HOME')
        else:
            self.poutput('Running shell command: {}'.format(line))
            output = os.popen(line).read()
            self.poutput(output)

    def do_show_results(self, _):
        """
        Usage: show_results
        Shows all result sets currently available.
        """
        self.result_manager.show_results()

    def do_set_result_desc(self, line):
        """
        Usage: set_result_desc <name=description>
        Set description of result set <name> to <description>.
        """
        items = [x.strip() for x in line.split('=')]
        name, description = items[0], items[1]
        self.result_manager.set_result_description(name, description)

    def do_undo(self, _):
        """
        Usage: undo
        Sets current result set to previous result set.
        """
        self.result_manager.undo()

    def do_redo(self, _):
        """
        Usage: redo
        Sets current result set to next result set.
        """
        self.result_manager.redo()
