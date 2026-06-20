pipeline {
    agent any
    environment {
        APP_NAME  = 'cicd-practice'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                echo "Building ${APP_NAME}:${IMAGE_TAG}"
                sh 'docker build -t ${APP_NAME}:${IMAGE_TAG} .'
                sh 'docker tag ${APP_NAME}:${IMAGE_TAG} ${APP_NAME}:latest'
                echo 'Build complete'
            }
        }
        stage('Test') {
            steps {
                echo 'Running smoke test...'
                sh 'docker run -d -p 9090:8080 --name smoke-test ${APP_NAME}:latest'
                sh 'sleep 3'
                sh 'curl -f http://localhost:9090 || exit 1'
                sh 'docker stop smoke-test && docker rm smoke-test'
                echo 'Smoke test passed'
            }
        }
        stage('Load Image to Minikube') {
            steps {
                echo 'Loading image into minikube registry...'
                sh 'minikube image load ${APP_NAME}:latest'
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes...'
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl rollout status deployment/${APP_NAME} --timeout=120s'
            }
        }
        stage('Verify') {
            steps {
                echo 'Verifying deployment...'
                sh 'kubectl get pods -l app=${APP_NAME}'
                sh 'kubectl get services'
            }
        }
    }
    post {
        success {
            echo 'DEPLOYMENT SUCCESSFUL'
            sh 'kubectl get pods -l app=${APP_NAME}'
        }
        failure {
            echo 'DEPLOYMENT FAILED - rolling back'
            sh 'kubectl rollout undo deployment/${APP_NAME} || true'
        }
        always {
            echo "Build ${BUILD_NUMBER} completed"
        }
    }
}
