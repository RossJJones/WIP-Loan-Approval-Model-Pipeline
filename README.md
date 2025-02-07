A simple WIP MLOps pipeline for deploying and monitoring a loan approval binary classifier using Metaflow. 
Planned tools: EvidentlyAI, FastAPI, Kubernetes, MLFlow

The pipeline will be split into containers for: feature engineering, model training, model deployment and a deployed model. 
3 Minio buckets will exist: data input, feature store, model artifacts. 
Everything will be versioned, and each container in the pipeline will listen for a relative version change before running their Metaflow code. 
Example: if there's a version roleback on a feature version in the feature store, this will trigger the model training to create a new model. 
