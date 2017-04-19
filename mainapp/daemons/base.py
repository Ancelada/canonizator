import daemon
import daemon.pidfile
import os
import psutil

import django.db
from django.db import connection

class Base:

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.pids_dir = os.path.join(self.base_dir, 'daemons/pids')
        self.statuses_dir = os.path.join(self.base_dir, 'daemons/statuses')

    def create_daemon_context(self, file_name):
        context = daemon.DaemonContext(
            working_directory=self.pids_dir,
            umask=0o002,
            pidfile=daemon.pidfile.PIDLockFile('{0}/{1}.pid'.format(self.pids_dir, file_name)),
        )
        return context

    def connection(self):
        if not connection.connection is None:
            connection.connection.close()
            connection.connection = None

    ##############################################
    # функция записывает статус
    def update_working_status(self, program, status):
        status_file_link = '{0}/{1}'.format(self.statuses_dir, program.file_name)
        f = open(status_file_link, 'w')
        if status == 'working':
            f.write('working')
        else:
            f.write('waiting')
        f.close()
    ##############################################

    ###############################################
    # обновление даты модификации pid файла
    def update_pidfile(self, program):
        pid_file = '{0}/{1}.pid'.format(self.pids_dir, program.file_name)
        self.__touch(pid_file)


    def __touch(self, fname):
        open(fname, 'a').close()
        os.utime(fname, None)
    ################################################


    ################################################
    # проверка, нужно ли запускать краулер
    def can_program(self, program_module):
        
        files = os.listdir(self.pids_dir)

        programs = []

        # получаем список запущенных краулеров
        for f in files:

            pid_file = open('{0}/{1}'.format(self.pids_dir, f), 'r')  
            with pid_file:
                pid_value = int(pid_file.readlines()[0])
            pid_file.close()

            # проверка на наличие в процессах
            if pid_value in psutil.pids():
                modification_time = os.path.getmtime('{0}/{1}'.format(self.pids_dir, f))
                programs.append({
                    'pid_file_name': f,
                    'modification_time': modification_time,
                    'name': f[:-4],
                    'pid': pid_value,
                })
            else:
                os.remove('{0}/{1}'.format(self.pids, f))

            programs = sorted(programs, key=lambda program: program['modification_time'])

        files = os.listdir(self.statuses_dir)

        statuses = []
        # дополняем статусом
        for f in files:
            status_file = open('{0}/{1}'.format(self.statuses_dir, f), 'r')
            with status_file:
                status_value = (status_file.readlines()[0])
            status_file.close()
            for crawler in programs:
                if crawler['name'] == f:
                    crawler['status'] = status_value

        print (programs)
        # смотрим какая программа самая старая
        if len(programs) > 0:
            if programs[0]['name'] == program_module.file_name and programs[0]['status'] == 'waiting':
                return True
        return False