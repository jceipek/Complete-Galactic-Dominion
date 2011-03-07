import os

os.popen('rm -rf /home/is/subversionRepo/complete-galactic-dominion/*')
os.popen('cp -r /home/is/.hudson/jobs/complete-galactic-dominion/workspace/* /home/is/subversionRepo/complete-galactic-dominion/')
os.popen('svn add /home/is/subversionRepo/complete-galactic-dominion/*')
gitres = os.popen('git log -1')
gitcommit = gitres.read()
gitres.close()
gitcommit = gitcommit.split('\n')
try:
    os.popen('svn ci /home/is/subversionRepo/complete-galactic-dominion/ -m ' + '"'+''.join(gitcommit[4:])+'\n'+gitcommit[1]+'"')
except:
    Exception('Failed to write to SVN')
