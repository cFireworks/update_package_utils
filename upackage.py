# -*- coding: utf-8 -*-
'''
# @Descripttion: 
# @Date: 1970-01-01 08:00:00
# @Author: cfireworks
# @LastEditTime: 2020-09-30 10:22:36
'''
import sys
import os
import re
import shutil
from threading import Thread


def doParse(source_folder):
	''' 
	# @description: analyze git log to generate packing plan
	# @param {str} 
	# @return {} 
	'''
    # parse git log info
    process = os.popen('cd ' + source_folder + ' && git log')
    output = process.read()
    commitIds = re.findall(r'commit (.*)\n', output)
    commitIds.reverse()
    update_file_set = set()
    for cid in commitIds:
        # parse commit's diff info and line number
        process = os.popen('''git show ''' + cid + ''' | grep diff -n''')
        out = process.read()
        diff_list = out.split()
        file_list = [(diff.split(':')[0], diff.split(':')[1]) for diff in diff_list]
        for fn in file_list:
            update_file_set.add(fn[2:])

def doPack(source_folder, target_folder):
    ''' 执行打包
    '''
    process = os.popen('cd ' + source_folder + ' && git log')
    output = process.read()
    commitIds = re.findall(r'commit (.*)\n', output)
    update_file_set = set()
    for cid in commitIds:
        process = os.popen('''git show ''' + cid + ''' | grep diff | cut -d " " -f 3''')
        out = process.read()
        file_list = out.split()
        for fn in file_list:
            update_file_set.add(fn[2:])
    for fn in update_file_set:
        target_pth = os.path.join(target_folder, fn)
        source_pth = os.path.join(source_folder, fn)
        target_dir = os.path.split(target_pth)[0]
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        if os.path.isfile(source_pth):
            Thread(target=shutil.copy, args=[source_pth, target_pth]).start()
    process.close()

if __name__ == "__main__":
    doPack('./', '../updates')