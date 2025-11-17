pipeline {
    agent any

    // Global variables definition
    environment {
        DOCKER_IMAGE = "brunoh6720/jdc-cabanga"
        DOCKER_HUB_TOKEN = credentials('docker-hub-credentials')
        // TAG = date and time of build
        TAG = sh(returnStdout: true, script: "date +%Y%m%d%H%M%S").trim()
        KUBECONFIG_FILE = "cabanga-cronjob.yaml"
    }

    stages {
        // --- 1. CLONE AND PREPARATION ---
        stage('Checkout Code') {
            steps {
                script {
                    echo "Cloning code..."
                }
            }
        }

        // --- 2. BUILD & PUSH DOCKER ---
        stage('Build & Push Image') {
            steps {
                script {
                        // Authentication, build and push with sudo. withRegistry to be investigated later.
                        // docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {

                        echo "Authentification, Build et Push of image..."

                        sh "echo ${env.DOCKER_HUB_TOKEN} | sudo docker login -u brunoh6720 --password-stdin"

                        // Image build
                        sh "sudo docker build -t ${DOCKER_IMAGE}:${TAG} -f Dockerfile ."
                        echo "Image built: ${DOCKER_IMAGE}:${TAG}"

                        // Image push
                        sh "sudo docker push ${DOCKER_IMAGE}:${TAG}"

                        // Tag push
                        sh "sudo docker tag ${DOCKER_IMAGE}:${TAG} ${DOCKER_IMAGE}:latest"
                        sh "sudo docker push ${DOCKER_IMAGE}:latest"

                        sh "sudo docker logout"
                    }
                }
            }
        }

        // --- 3. KUBERNETES DEPLOYMENT ---
        stage('Deploy to K3s') {
            steps {
                script {
                    // Replace TAG in  YAML
                    sh "sed -i 's|${DOCKER_IMAGE}:.*|${DOCKER_IMAGE}:${TAG}|g' ${KUBECONFIG_FILE}"

                    // K3S deployment
                    sh "kubectl apply -f ${KUBECONFIG_FILE}"
                    echo "Cronjob updated with TAG ${TAG}."
                }
            }
        }
    }
}