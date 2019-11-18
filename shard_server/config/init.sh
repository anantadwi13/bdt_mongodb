cp ./hosts /etc/hosts

nohup mongod --bind_ip_all &
sleep 15
mongo --eval 'db.createUser({user: "mongo-admin", pwd: "password", roles:[{role: "root", db: "admin"}]})' admin
mkdir -p /opt/mongo
cp ./mongo-keyfile /opt/mongo
chmod 400 /opt/mongo/mongo-keyfile
chown mongodb:mongodb /opt/mongo/mongo-keyfile

kill -2 `pgrep mongo`
sleep 20


# Initializing Shard Server

cp ./mongod.conf /etc/mongod.conf
sed -i "s/.*  bindIp: 127.0.0.1.*/  bindIp: ${IP}/" /etc/mongod.conf
sed -i "s/.*  port: 27017.*/  port: ${PORT}/" /etc/mongod.conf
# sed -i "s/.*#replication:.*/replication:\n  replSetName: ${REPL_NAME}/" /etc/mongod.conf
sed -i "s/.*#sharding:.*/sharding:\n  clusterRole: \"${CLUSTER_ROLE}\"/" /etc/mongod.conf

nohup mongod --bind_ip_all --config /etc/mongod.conf &
sleep 30

# Registering Shard Server

# if [ ${INIT} -eq 1 ]; then 
#     mongo mongo-shard-1:27017 -u mongo-admin -p password --authenticationDatabase admin --eval 'rs.initiate( { _id: "shardReplSet", members: [ { _id: 0, host: "mongo-shard-1:27017" }, { _id: 1, host: "mongo-shard-2:27017" }, { _id: 2, host: "mongo-shard-3:27017" } ] } )'
# fi

sleep 20

mongo mongo-query-router:27017 -u mongo-admin -p password --authenticationDatabase admin --eval "sh.addShard( \"${HOSTNAME}:${PORT}\" )"
