FROM python:3.6.2

WORKDIR /src
ADD . /src

ADD requirements.txt /src
ENV ENVIRONMENT production
ENV PYTHONUSERBASE /venv
ENV PATH "/venv/bin:${PATH}"
RUN pip install --user -r requirements.txt --upgrade pip==21.1.1

EXPOSE 5000

# ENTRYPOINT ["./docker/entrypoint.sh"]
CMD ["python", "main.py"]    