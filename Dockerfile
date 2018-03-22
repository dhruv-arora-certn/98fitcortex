FROM python:3.6

RUN mkdir /app/

WORKDIR /app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY testing/ testing/

WORKDIR /app/testing/

RUN chmod a+x manage.py

RUN ln -sf request.log /dev/stdout 

ENTRYPOINT ["python","manage.py"]

CMD ["shell"]

EXPOSE 8000
