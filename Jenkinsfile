pipeline {

    agent any

    environment {

        IMAGE_NAME = "saksham157/ai-idp-platform"

        IMAGE_TAG = "latest"
    }

    stages {

        stage('Checkout') {

            steps {

                checkout scm
            }
        }

        stage('Build Docker Image') {

            steps {

                script {

                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Push Docker Image') {

            steps {

                script {

                    docker.withRegistry(
                        'https://index.docker.io/v1/',
                        'dockerhub-creds'
                    ) {

                        docker.image("${IMAGE_NAME}:${IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Deploy To Kubernetes') {

            steps {

                sh 'kubectl apply -f kubernetes/deployment.yaml'

                sh 'kubectl apply -f kubernetes/service.yaml'
            }
        }
    }
}