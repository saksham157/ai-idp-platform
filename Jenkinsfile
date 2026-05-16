pipeline {

    agent {

        kubernetes {

            defaultContainer 'docker'

            yaml """

apiVersion: v1
kind: Pod

spec:

  containers:

    - name: docker

      image: docker:27.0.3

      command:
        - cat

      tty: true

      volumeMounts:

        - name: docker-sock

          mountPath: /var/run/docker.sock

  volumes:

    - name: docker-sock

      hostPath:

        path: /var/run/docker.sock

"""
        }
    }

    environment {

        IMAGE_NAME = "saksham8000/ai-idp-platform"

        IMAGE_TAG = "latest"
    }

    stages {

        stage('Checkout') {

            steps {

                checkout scm
            }
        }

        stage('Docker Build') {

            steps {

                sh 'docker version'

                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        stage('Docker Login') {

            steps {

                withCredentials([
                    usernamePassword(

                        credentialsId: 'dockerhub-creds',

                        usernameVariable: 'DOCKER_USER',

                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {

                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Push Image') {

            steps {

                sh 'docker push ${IMAGE_NAME}:${IMAGE_TAG}'
            }
        }
    }
}
