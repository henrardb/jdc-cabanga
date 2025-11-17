pipeline {
    agent any

    // Global variables definition
    environment {
        DOCKER_IMAGE = "brunoh6720/jdc-cabanga"
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
                    // Connection to docker Hub
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {

                        // Build image with TAG
                        def customImage = docker.build("${DOCKER_IMAGE}:${TAG}", "-f Dockerfile .")
                        echo "Image built: ${DOCKER_IMAGE}:${TAG}"

                        // Push image to Docker Hub
                        customImage.push()
                        echo "Image pushed to Docker Hub."

                        // Push TAG for reference
                        customImage.push("latest")
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