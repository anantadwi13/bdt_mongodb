cp ./hosts /etc/hosts

nohup mongos &
sleep 15
mongo --eval 'db.createUser({user: "mongo-admin", pwd: "password", roles:[{role: "root", db: "admin"}]})' admin
mkdir -p /opt/mongo
cp ./mongo-keyfile /opt/mongo
chmod 400 /opt/mongo/mongo-keyfile
chown mongodb:mongodb /opt/mongo/mongo-keyfile

kill -2 `pgrep mongo`
sleep 10

cp ./mongos.conf /etc/mongos.conf
sed -i "s/.*  bindIp: 127.0.0.1.*/  bindIp: ${IP}/" /etc/mongos.conf
sed -i "s/.*  port: 27017.*/  port: ${PORT}/" /etc/mongos.conf
sed -i "s/.*#sharding:.*/sharding:\n  configDB: ${REPLICA_SET}/" /etc/mongos.conf

nohup mongos --config /etc/mongos.conf &
sleep 2

