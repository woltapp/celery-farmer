FROM python:3.7.2-stretch AS build-image

RUN useradd --user-group --create-home user

RUN mkdir -p /home/user/celery-farmer
WORKDIR /home/user/celery-farmer
COPY . .
RUN chown -R user:user .

USER user
RUN python setup.py bdist_wheel

FROM python:3.7.2-slim-stretch

WORKDIR /root
COPY --from=build-image /home/user/celery-farmer/dist/*.whl .
RUN pip install --no-cache-dir *.whl
RUN rm *.whl

RUN useradd --user-group --create-home user
USER user
WORKDIR /home/user

ENTRYPOINT ["celery-farmer", "start"]
CMD []
