pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'docker-credentials'
        IMAGE_NAME = 'gonemesis/si-parking-flask'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker Image...'
                script {
                    docker.build("$IMAGE_NAME:latest")
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_CREDENTIALS_ID) {
                        docker.image("$IMAGE_NAME:latest").push()
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Image pushed successfully!'
        }
        failure {
            echo 'Image push failed.'
        }
    }
}
