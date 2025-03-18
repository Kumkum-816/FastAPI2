# Start MongoDB locally if not running
if ! docker ps | grep -q "mongo"; then
    echo "Starting MongoDB container..."
    docker run -d --name mongodb -p 27017:27017 mongo:latest
else
    echo "MongoDB is already running."
fi

#Build and push Docker image
IMAGE_NAME="myregistry.com/fastapi-app:v1"
echo "Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

echo "Pushing Docker image to registry..."
docker push $IMAGE_NAME

#Deploy to Kubernetes
KUBE_MANIFEST="k8s-deployment.yaml"
echo "Applying Kubernetes manifest: $KUBE_MANIFEST"
kubectl apply -f $KUBE_MANIFEST

echo "Deployment completed successfully!"
