# security-cam
* A home security camera management system.
* Security camera images are stored on twitter. (Free image storage!)
* Receive image data through API POST endpoint and store images in twitter through twitter API.

Running with Docker
-------------------
* edit bin/run-docker.py
 * add twitter credentials & http basic auth creds for server clients
* bin/run-docker.py

Running with Kubernetes
-----------------------
* Start a kubernetes cluster
 * Start here: https://github.com/jelis/coreos-kubecluster 
* Create a cam server deployment
 * edit kubernetes/deployment.yaml.
 * provide values for twitter credentials and client basic auth credentials
```
kubectl create -f kubernetes/deployment.yaml
```
* Expose the deployment with a kubernetes service endpoint with HTTPS
 * create a certificate for the server with amazon certificate manager: https://console.aws.amazon.com/acm
 * edit kubernetes/service.yaml
 * enter the certificate ARN for your site in service.yaml
* Start the service with kube
```
kubectl create -f kubernetes/service.yaml
```
* The service will now be exposed by an AWS SSL enabled load balancer. Get the load balancer hostname from the AWS EC2 Console under Elastic Load Balancers.
* Using amazon route 53, create a CNAME record pointing to the load balancer hostname for the camera server domain name, for example make cams.mydomain.com point to the ELB hostname that you got from the previous step.
* DNS updates may take a while. Once done, verify that the kubernetes deployment and service setup completed successfully:
```
curl -v -X POST https://cams.mydomain.com/captures/
```
You should get an HTTP 401 Unauthorized response.

Alternativaly once the cluster is setup, you can just do:
```
fab deploy_service
fab deploy_pods
```
in order to setup the kube service and the pods.
