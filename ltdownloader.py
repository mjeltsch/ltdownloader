#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#
# tested on Ubuntu 16.04, requires pdftk
#
import subprocess, os, sys, time, requests

def execute_subprocess(comment, bash_command, working_directory='.'):
    print("\n" + comment, bash_command)
    process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=working_directory)
    output, error = process.communicate()
    process_status = process.wait()
    if output.decode('utf-8') != '':
        print("Output: " + str(output))
    if error.decode('UTF-8') != '':
        print("Error: " + str(error))

def run():
    for year in range(2007, 2014):
        for bimonth in range(1, 8):
            filelist = ''
            start = 1
            for startpage in range (start, 100):
                print("startpage: " + str(startpage))
                for endpage in range (1, 100):
                    print("endpage: " + str(endpage))
                    if startpage <= endpage and endpage-startpage < 30:
                        filename = "lt_" + str(year) + "_" + str(bimonth).zfill(2) + "_" + str(startpage) + "_" + str(endpage) + ".pdf"
                        URL = "http://labtimes.org/labtimes/issues/lt" + str(year) + "/lt" + str(bimonth).zfill(2) + "/" + filename
                        try:
                            print("Trying " + URL)
                            r = requests.get(URL)
                            if r.status_code == 200:
                                print("Saving " + filename)
                                filelist += filename + " "
                                with open(filename, "wb") as code:
                                    code.write(r.content)
                                    start = endpage
                                break
                        except Exception as ex:
                            print(str(ex))
                        time.sleep(1)
            bash_command = "pdftk " + filelist + " cat output " + str(year) + "_" + str(bimonth).zfill(2) + ".pdf"
            execute_subprocess("Trying to assemble PDF:\n", bash_command)
            time.sleep(10)
if __name__ == '__main__':
    run()
