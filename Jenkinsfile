pipeline {
    agent any
    environment {
        DOCKER_CREDS = credentials('dockerhub-creds')
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
                // Use secret text credential for Azure SP JSON
                withCredentials([string(credentialsId: 'azure-sp-sdk-auth', variable: 'AZURE_SP_JSON')]) {
                    sh '''
                    echo $AZURE_SP_JSON > sp.json
                    az login --service-principal --sdk-auth --username sp.json
                    az aks get-credentials --resource-group pavani --name webapp
                    kubectl apply -f k8s/
                    '''
                }
            }
        }
    }
}
