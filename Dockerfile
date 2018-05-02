FROM python:3.5.3
RUN pip install flask jira pyzabbix requests
RUN mkdir app
ADD start.py /app/
ADD consts.py /app/
EXPOSE 5000
CMD [ "python", "/app/./start.py" ]
