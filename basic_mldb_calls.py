import subprocess
import sys

"""
Gets command line arguments. The type of process [check_successcode|basic|full] if the first argument
is eiither basic or full, it receives the number of cases for each thread to complete as second argument
and the number of threads as third argument. Therefore the total number of cases produced is number_of_threads*cases_per_thread

Returns nothing. The slave script is processed in the background.
"""

if sys.argv[1]=='check_success_code':
    command = 'python create_cases_mldb.py ' + sys.argv[1] +' &'
    subprocess.run(command, shell=True)
else:
    command = 'python create_cases_mldb.py ' + sys.argv[1] + ' ' + str(int(sys.argv[2])) +' &'
    for script_instance in range(int(sys.argv[3])):
        subprocess.run(command, shell=True)