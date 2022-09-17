FROM registry.access.redhat.com/ubi8/ubi
RUN dnf -y install iputils python3
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
COPY ./application /app
EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["app.py"]
