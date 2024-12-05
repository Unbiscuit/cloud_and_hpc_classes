task 1 
  "docker compose up -d" from task 1 dir
  access localhost from your browser

task 2

  minikube start

  cd backend
  docker build -t <your-dockerhub-user>/backend:latest .
  docker push <your-dockerhub-user>/backend:latest

  cd ../frontend
  docker build -t <your-dockerhub-user>/frontend:latest .
  docker push <your-dockerhub-user>/frontend:latest

  kubectl apply -f backend/deployment.yaml
  kubectl apply -f backend/service.yaml
  kubectl apply -f frontend/deployment.yaml
  kubectl apply -f frontend/service.yaml

  minikube tunnel

  access localhost from your browser
