"""
Gets information about the current build for use in the Tex and HTML files
"""

import subprocess
import sys


class BuildInfo:
    """
    Class to hold build information
    """

    def __init__(self):
        self.gitversion = self.GetGitVersion()
        self.date = self.GetDate()
        self.gitbranch = self.GetGitBranch()
        self.hostname = self.GetHostName()
        self.pythonversion = self.GetPythonVersion()
        self.linuxversion = self.GetLinuxVersion()

    def GetGitVersion(self):
        """
        Gets the git version
        """
        return subprocess.check_output(["git", "describe", "--always"]).strip().decode('utf-8')

    def GetDate(self):
        """
        Gets the date
        """
        return subprocess.check_output(["date", "+%d/%m/%Y %H:%M:%S"]).strip().decode('utf-8')

    def GetGitBranch(self):
        """
        Gets the git branch
        """
        return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip().decode('utf-8')

    def GetHostName(self):
        """
        Gets the hostname
        """
        return subprocess.check_output(["hostname"]).strip().decode('utf-8')

    def GetPythonVersion(self):
        """
        Gets the python version
        """
        return "Python {}.{}.{}".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)

    def GetLinuxVersion(self):
        """
        Gets the linux version
        """
        return subprocess.check_output(["uname", "-r", "-o", "-i"]).strip().decode('utf-8').replace('_', ' ')

    def __repr__(self):
        d = {
            'gitversion': self.gitversion,
            'date': self.date,
            'gitbranch': self.gitbranch,
            'hostname': self.hostname,
            'pythonversion': self.pythonversion,
            'linuxversion': self.linuxversion
        }
        return ";".join(["{}={}".format(k, d[k]) for k in d])

    def AsHTML(self, filename):
        """
        Returns the build info as an HTML table written to `filename`
        """
        html = """
        <h1>Build Information</h1>
        <table>
        <tr><td>Git Version</td><td>{}</td></tr>
        <tr><td>Date</td><td>{}</td></tr>
        <tr><td>Git Branch</td><td>{}</td></tr>
        <tr><td>Hostname</td><td>{}</td></tr>
        <tr><td>Python Version</td><td>{}</td></tr>
        <tr><td>Linux Version</td><td>{}</td></tr>
        </table>
        """.format(self.gitversion, self.date, self.gitbranch, self.hostname, self.pythonversion,
                   self.linuxversion)
        with open(filename, "w") as o:
            o.write(html)

    def AsLaTeX(self, filename):
        """
        Returns the build info as a LaTeX table written to `filename`
        """
        latex = r"""\section{Build Information}
        \begin{tabular}{|l|l|}
        \hline
        """

        lines = [r"{} & {} \\ \hline".format(k, v) for k, v in {
            'Git Version': self.gitversion,
            'Date': self.date,
            'Git branch': self.gitbranch,
            'Hostname': self.hostname,
            'Python version': self.pythonversion,
            'Linux version': self.linuxversion
        }.items()]

        latex += '\n'.join(lines)
        latex += '\n\\end{tabular}'
        with open(filename, "w") as o:
            o.write(latex)


if __name__ == '__main__':
    bi = BuildInfo()
    bi.AsHTML("buildinfo.html")
    bi.AsLaTeX("buildinfo.tex")
    print(bi)