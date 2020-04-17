FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1

RUN curl https://pyenv.run | bash \
    && echo 'export PATH="/root/.pyenv/bin:$PATH"' >> /root/.bashrc \
    && echo 'eval "$(pyenv init -)"' >> /root/.bashrc \
    && echo 'eval "$(pyenv virtualenv-init -)"' >> /root/.bashrc

ENV PATH /root/.pyenv/bin:$PATH
RUN eval "$(pyenv init -)" \
    && eval "$(pyenv virtualenv-init -)" \
    && pyenv install 2.7.16 \
    && pyenv install 3.6.9 \
    && pyenv install 3.7.4

RUN pyenv virtualenv 2.7.16 metrics-2.7 \
    && pyenv virtualenv 3.6.9 metrics-3.6 \
    && pyenv virtualenv 3.7.4 metrics-3.7 \
    && pyenv global metrics-2.7 metrics-3.6 metrics-3.7

RUN pip install tox==3.14.0
