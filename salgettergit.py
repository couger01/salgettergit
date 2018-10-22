import subprocess
import argh
import getpass

def write_env_file(sal_directory: str, ospl_directory: str):
    """

    :return:
    """
    sal_env_lines = [
        "### Change the LSST_SDK_INSTALL and OSPL_HOME to the actual locations and uncomment\n",
        "###\n",
        "export LSST_SDK_INSTALL={0}\n".format(sal_directory),
        "export OSPL_HOME={0}/OpenSpliceDDS/V6.4.1/HDE/x86_64.linux\n".format(ospl_directory),
        "export PYTHON_BUILD_VERSION=3.6m\n",
        "export PYTHON_BUILD_LOCATION=/usr/local\n",
        "export LSST_DDS_DOMAIN=citest\n",
        "###\n",
        "\n",
        'if [ -z "$LSST_SDK_INSTALL" ]; then\n',
        '   echo "Please edit setup.env to set LSST_SDK_INSTALL and OSPL_HOME environment variables"\n'
        '   echo "to the locations where ts_sal and ts_opensplice have been installed."\n',
        "else\n",
        'if [ -z "$OSPL_HOME" ]; then\n',
        '   echo "Please edit setup.env to set OSPL_HOME environment variable"\n',
        "else\n",
        'if [ -z "$PYTHON_BUILD_VERSION" ]; then\n',
        '   echo "Please edit setup.env to set PYTHON_BUILD_VERSION and PYTHON_BUILD_LOCATION environment variable"\n',
        "else\n",
        "export SAL_HOME=$LSST_SDK_INSTALL/lsstsal\n",
        "export SAL_WORK_DIR=$LSST_SDK_INSTALL/test\n",
        "export SAL_CPPFLAGS=-m64\n",
        "source $SAL_HOME/salenv.sh\n",
        "export JAVA_HOME=/etc/alternatives/java_sdk_openjdk\n",
        "export LD_LIBRARY_PATH=${SAL_HOME}/lib\n",
        "export TCL_LIBRARY=${SAL_HOME}/lib/tcl8.5\n",
        "export TK_LIBRARY=${SAL_HOME}/lib/tk8.5\n",
        "export LD_PRELOAD=/etc/alternatives/java_sdk_openjdk/jre/lib/amd64/libjsig.so\n",
        "export PATH=$JAVA_HOME/bin:${SAL_HOME}/bin:${PATH}\n",
        "export PYTHONPATH=$PYTHONPATH:${SAL_WORK_DIR}/lib\n",
        "export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${SAL_WORK_DIR}/lib:${SAL_DIR}/lib\n",
        "export RLM_HOME=$SAL_HOME/.m2/repository/org/opensplice/gateway/rlm/9.1.3\n",
        "source $OSPL_HOME/release.com\n",
        "mkdir -p $LSST_SDK_INSTALL/lsstsal/lib\n",
        "sal_version=`grep -i version $SAL_DIR/sal_version.tcl | awk '{print $3}'\n",
        "export SAL_VERSION=$sal_version\n",
        'echo "LSST middleware toolset environment v"$sal_version" is configured"\n',
        "fi\n",
        "fi\n",
        "fi\n"
    ]
    with open("setup.env","w") as f:
        f.writelines(sal_env_lines)

def get_sal(sal_version: str, sal_directory: str):
    download_sal_archive_process = subprocess.Popen(["curl","-L","-J","-O","https://github.com/lsst-ts/ts_sal/archive/{0}.tar.gz".format(sal_version)],cwd="{0}".format(sal_directory))
    download_sal_archive_process.wait()
    unpack_sal_archive_process = subprocess.Popen(["tar","-xvzf","ts_sal-{0}.tar.gz".format(sal_version[1:])],cwd="{0}".format(sal_directory))
    unpack_sal_archive_process.wait()

def setup_sal(sal_env_directory: str, sal_directory, ospl_directory: str):
    write_env_file(sal_env_directory, ospl_directory)
    move_env_file_process = subprocess.Popen("mv setup.env {0}".format(sal_directory),shell=True)
    move_env_file_process.wait()


def main():
    parser = argh.ArghParser()
    argh.add_commands(parser,[get_sal, setup_sal])
    return parser

if __name__ == '__main__':
    argh.dispatch(parser=main())