docker run -it --name teamcity-server-instance  \
    -v /data/teamcity_server/datadir \ 
    -v /opt/teamcity/logs  \ 
    -p 8111:8111 \              
    jetbrains/teamcity-server