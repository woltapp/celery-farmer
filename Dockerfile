FROM python:3.9.1-buster AS build-image
RUN useradd --user-group --create-home user
RUN pip install -U pip pipenv

RUN mkdir -p /home/user/celery-farmer
WORKDIR /home/user/celery-farmer
COPY . .
RUN chown -R user:user .

USER user

RUN pipenv install --deploy
RUN pip wheel $(pipenv lock -r) -w dist

FROM python:3.9.1-slim-buster
RUN useradd --user-group --create-home user

WORKDIR /root
COPY --from=build-image /home/user/celery-farmer/dist dist
RUN pip install \
    --no-cache-dir \
    --no-index \
    --find-links file:///root/dist/ \
    celery-farmer
RUN rm -rf dist

USER user
WORKDIR /home/user

ENTRYPOINT ["celery-farmer", "start"]
CMD []
