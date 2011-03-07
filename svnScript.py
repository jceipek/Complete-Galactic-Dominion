import os

os.popen('cp -r /home/is/.hudson/jobs/complete-galactic-dominion/workspace/* /home/is/subversionRepo/complete-galactic-dominion/')
os.popen('svn add /home/is/subversionRepo/complete-galactic-dominion/*')
gitres = os.popen('git log -1')
gitcommit = gitres.read()
gitres.close()
os.popen('svn ci /home/is/subversionRepo/complete-galactic-dominion/ -m ' + gitcommit)