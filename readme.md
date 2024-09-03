gcloud builds submit --tag gcr.io/cybertrace-427312/ggmproject  --project=cybertrace-427312 

gcloud run deploy --image gcr.io/cybertrace-427312/ggmproject --platform managed  --project=cybertrace-427312 --allow-unauthenticated