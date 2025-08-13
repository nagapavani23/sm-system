pipeline {
    agent any
    environment {
        DOCKER_CREDS = credentials('dockerhub-creds')
        AZURE_CRED = credentials('azure-sp')
        REGISTRY = "${DOCKER_CREDS_USR}"
    }
    stages {
        stage('Build Backend') {
            steps {
                sh 'docker build -t $REGISTRY/student-backend:latest backend'
            }
        }
        stage('Build Frontend') {
            steps {
                sh 'docker build -t $REGISTRY/student-frontend:latest frontend'
            }
        }
        stage('Push Images') {
            steps {
                sh 'echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin'
                sh 'docker push $REGISTRY/student-backend:latest'
                sh 'docker push $REGISTRY/student-frontend:latest'
            }
        }
        stage('Deploy to AKS') {
            steps {
                sh '''
                az login --service-principal -u $AZURE_CRED_USR -p $AZURE_CRED_PSW --tenant <tenant-id>
                az aks get-credentials --resource-group pavani --name webapp
                kubectl apply -f k8s/
                '''
            }
        }
    }
}