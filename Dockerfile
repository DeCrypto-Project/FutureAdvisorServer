FROM artifactory.outbrain.com:5005/baseimages/python-base-miniconda3-4712:latest

ARG SERVICE_NAME=PyBootcampCondaOmar-chaim
ENV SERVICE_NAME=$SERVICE_NAME

COPY environment.yml /environment.yml
RUN set -ex && \
    conda env create -f /environment.yml
RUN conda init
RUN echo "conda activate " >> ~/.bashrc
ENV BASH_ENV ~/.bashrc

EXPOSE 8000
COPY . /outbrain/Prod/Apps/myapp/
WORKDIR /outbrain/Prod/Apps/myapp/
ENTRYPOINT ["/outbrain/Prod/Apps/myapp/entrypoint.sh"]
CMD ["start-app"]
