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

        IMAGE_TAG = "${BUILD_NUMBER}"
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

        stage('Update Deployment File') {

            steps {

                sh """

sed -i "s|image:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|g" kubernetes/deployment.yaml

cat kubernetes/deployment.yaml

"""
            }
        }

        stage('Push Updated Manifest') {

            steps {

                withCredentials([
                    usernamePassword(

                        credentialsId: 'github-creds',

                        usernameVariable: 'GIT_USER',

                        passwordVariable: 'GIT_PASS'
                    )
                ]) {

                    sh """

git config --global --add safe.directory /home/jenkins/agent/workspace/ai-idp-deployment

git config --global user.email "platform@local"

git config --global user.name "jenkins"

git add .

git commit -m "update deployment image ${IMAGE_TAG}"

git push https://${GIT_USER}:${GIT_PASS}@github.com/saksham157/ai-idp-platform.git HEAD:main

"""
                }
            }
        }
    }
}
