docker rm teamcity-agent-instance
docker run -it  \
    --link teamcity-server-instance  \
    --name teamcity-agent-instance  \
    -e SERVER_URL=http://teamcity-server-instance:8111  \
    --privileged -e DOCKER_IN_DOCKER=start  \
    -v /data/teamcity_agent/conf  \
    -v /opt/teamcity_agent/work  \
    -v /opt/teamcity_agent/system  \
    jetbrains/teamcity-agent