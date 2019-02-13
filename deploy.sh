# Create GKE cluster
gcloud beta container --project "ovg-training" clusters create "ovg-training-kube" --region "europe-west2" --no-enable-basic-auth --cluster-version "1.11.6-gke.6" --machine-type "n1-standard-2" --image-type "COS" --disk-type "pd-standard" --disk-size "100" --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "1" --enable-stackdriver-kubernetes --enable-private-nodes --master-ipv4-cidr "172.16.0.0/28" --enable-ip-alias --network "projects/ovg-training/global/networks/ovg-training" --subnetwork "projects/ovg-training/regions/europe-west2/subnetworks/private" --default-max-pods-per-node "110" --enable-autoscaling --min-nodes "1" --max-nodes "5" --enable-master-authorized-networks --master-authorized-networks 104.132.25.68/32 --addons HorizontalPodAutoscaling,HttpLoadBalancing,Istio --istio-config auth=MTLS_PERMISSIVE --enable-autoupgrade --enable-autorepair --maintenance-window "03:00"

# Fetch cert to connect with kubectl
gcloud beta container clusters get-credentials ovg-training-kube --region europe-west2 --project ovg-training

# Auto inject istio sidecars
kubectl label namespace default istio-injection=enabled

# Deploy backend
kubectl apply -f ./backend/db.yaml
kubectl apply -f ./backend/deployment.yaml

# Deploy frontend
kubectl apply -f ./frontend/deployment.yaml
kubectl apply -f ./frontend/gateway.yaml
