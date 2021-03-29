docker rm dtlab-chat-running
docker run -it  \
    --name dtlab-chat-running  \
    -p 5000:5000  \
    dtlab-chat
