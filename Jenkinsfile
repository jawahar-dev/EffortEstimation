pipeline {
    agent any

    environment {
        // Define environment variables
        DOCKER_IMAGE = "jawaharpatro/effort-app"
        DOCKER_CREDENTIALS_ID = "MY_DOCKER_ID"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the source code from the repository
                git branch: 'main', url: 'https://github.com/jawahar-dev/EffortEstimation.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    docker.build("${env.DOCKER_IMAGE}:latest")
                }
            }
        }

        // stage('Run Tests') {
        //     steps {
        //         script {
        //             // Run tests using the Docker image
        //             docker.image("${env.DOCKER_IMAGE}:latest").inside {
        //                 sh 'python -m pytest'
        //             }
        //         }
        //     }
        // }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', "${env.DOCKER_CREDENTIALS_ID}") {
                        docker.image("${env.DOCKER_IMAGE}:latest").push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Deploy the application using Docker Compose
                    sh '''
                    docker-compose down
                    docker-compose up -d
                    '''
                }
            }
        }
    }

    post {
        always {
            // Clean up Docker resources
            script {
                docker.image("${env.DOCKER_IMAGE}:latest").inside {
                    sh 'docker system prune -f'
                }
            }
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
