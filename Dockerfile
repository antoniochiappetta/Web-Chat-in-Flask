FROM python:3

WORKDIR /Users/antoniochiappetta/Google\ Drive/Developer/Cisco\ Academy/DTLab\ Exercises/Week\ 4/web\ chat/chat_container

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod + ./start.sh
CMD ./start.sh

EXPOSE 5000