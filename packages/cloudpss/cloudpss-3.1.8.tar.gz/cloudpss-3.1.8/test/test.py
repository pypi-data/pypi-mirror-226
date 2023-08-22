
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..\\'))
import cloudpss
import time
import numpy as np
import pandas as pd

if __name__ == '__main__':
    try:
        os.environ['CLOUDPSS_API_URL'] = 'https://cloudpss.net/'
        print('CLOUDPSS connected')
        cloudpss.setToken(
            'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTUsInVzZXJuYW1lIjoiRGVtbyIsInNjb3BlcyI6W10sInR5cGUiOiJhcHBseSIsImV4cCI6MTcyMjY1NTkxNSwiaWF0IjoxNjkxNTUxOTE1fQ.FhkFvfgsaPvGKJcCLWg3iibWsFPpKWpwrP7tb5PSsnQybxfC4Q_V8caOkmaxW9LfFf-bAY9ch5m4u57w7HUS_A')
        print('Token done')
        project = cloudpss.Model.fetch('model/Demo/39test')
        
        
        runner = project.run()
        while not runner.status():
            time.sleep(0.01)
            logs = runner.result.getLogs()
            for log in logs:
                print(log)
        print(runner.result.getBuses())
    except Exception as e:

        print("程序出错，重启中")

