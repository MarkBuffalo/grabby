FROM python:3.7.4

ADD grab.py /tmp
ADD requirements.txt /tmp
ADD products.txt /tmp
ADD wake_up.wav /tmp
RUN pip3 install --upgrade pip playsound
RUN pip3 install -r /tmp/requirements.txt
CMD [ "python3", "/tmp/grab.py" ]
