pipeline {
    agent any

    environment {
    VERSION = 'v1'
    DOCKERHUB_USERNAME = 'sahanalakshmi18'
    IMAGE_NAME = 'library-management-system'
    DEPLOYMENT_NAME = 'library-v1'
    SERVICE_NAME = 'library-v1-service'
    NODE_PORT = '30001'
}

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies and Test') {
            steps {
                bat '''
                    python -m pip install -r requirements.txt
                    python -m unittest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    docker build -t %DOCKERHUB_USERNAME%/%IMAGE_NAME%:%VERSION% .
                '''
            }
        }

        stage('Login and Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    bat '''
                        powershell -NoProfile -Command "$env:DOCKER_PASS | docker login -u $env:DOCKER_USER --password-stdin"
                        docker push %DOCKERHUB_USERNAME%/%IMAGE_NAME%:%VERSION%
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    kubectl create deployment %DEPLOYMENT_NAME% --image=%DOCKERHUB_USERNAME%/%IMAGE_NAME%:%VERSION% --dry-run=client -o yaml | kubectl apply -f -
                    kubectl set image deployment/%DEPLOYMENT_NAME% %DEPLOYMENT_NAME%=%DOCKERHUB_USERNAME%/%IMAGE_NAME%:%VERSION%
                    kubectl rollout status deployment/%DEPLOYMENT_NAME% --timeout=180s
                '''
            }
        }

        stage('Create or Update Service') {
            steps {
                bat '''
                    kubectl apply -f k8s-service.yaml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                bat '''
                    kubectl get deployments
                    kubectl get services
                    kubectl get pods
                '''
            }
        }
    }

    post {
        success {
            echo 'Library Management System pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs for the error.'
        }
    }
}