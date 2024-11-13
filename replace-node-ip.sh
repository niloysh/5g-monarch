# Fetch the node IP using your existing script
NODE_IP=$(./get-node-ip.sh)

# Check if NODE_IP was fetched successfully
if [[ -z "$NODE_IP" ]]; then
  echo "Error: Could not retrieve NODE_IP."
  exit 1
fi

# Replace NODE_IP in the .env file
sed -i "s/^NODE_IP=.*/NODE_IP=\"$NODE_IP\"/" .env

echo "NODE_IP updated to $NODE_IP in .env file."