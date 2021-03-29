FROM python:3

WORKDIR /home/web-chat

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod + ./start.sh
CMD ./start.sh

EXPOSE 5000