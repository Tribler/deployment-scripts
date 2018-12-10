"""
This script fetches the latest build executable for MacOSX from Jenkins.
It expects the following environment variable be provided:
- JENKINS_JOB_URL : Jenkins job which builds the Debian package
- BUILD_TYPE : Build type [Win64, Win32, Linux, MacOS]
- WORKSPACE : Jenkins workspace (set by jenkins itself)
"""
from __future__ import print_function

import os
import time

from deployment_utils import fetch_latest_build_artifact, print_and_exit

if __name__ == '__main__':
    start_time = time.time()

    # Step 1: fetch the latest Tribler installer from Jenkins
    build_type = os.environ.get('BUILD_TYPE', 'MacOS')
    job_url = os.environ.get('JENKINS_JOB_URL', None)
    if not job_url:
        print_and_exit('JENKINS_JOB_URL is not set')

    INSTALLER_FILE = fetch_latest_build_artifact(job_url, build_type)
    CDR_PATH = os.path.join(os.environ.get('WORKSPACE'), "Tribler.cdr")
    APP_PATH = os.path.join(os.environ.get('WORKSPACE'), "Tribler.app")

    # Step 2: Mount the dmg file
    # Convert .dmg to cdr to bypass EULA
    CONVERT_COMMAND = "hdiutil convert %s -format UDTO -o %s" % (INSTALLER_FILE, CDR_PATH)
    print(CONVERT_COMMAND)
    os.system(CONVERT_COMMAND)

    ATTACH_COMMAND = "hdiutil attach %s" % CDR_PATH
    print(ATTACH_COMMAND)
    os.system(ATTACH_COMMAND)

    # Step 3: Copy the Tribler.app to workspace
    COPY_COMMAND = "cp -R /Volumes/Tribler/Tribler.app %s" % os.environ.get('WORKSPACE')
    print(COPY_COMMAND)
    os.system(COPY_COMMAND)

    # Step 4: Unmount Tribler volume
    DETACH_COMMAND = "hdiutil detach /Volumes/Tribler"
    print(DETACH_COMMAND)
    os.system(DETACH_COMMAND)

    diff_time = time.time() - start_time
    print('Installed Tribler in MacOS in %s seconds' % diff_time)
    time.sleep(1)
