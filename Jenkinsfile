pipeline {
    agent any

    // Global variables definition
    environment {
        IMAGE = "ghcr.io/henrardb/jdccabanga"
        // TAG = date and time of build
        TAG = sh(returnStdout: true, script: "date +%Y%m%d%H%M%S").trim()
        CRONJOB_FILE = "jdccabanga-cronjob.yaml"
    }

    options {
        skipDefaultCheckout(true)
    }
    stages {
        // --- 1. CHECKOUT ---
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // --- 2. BUILD & PUSH DOCKER ---
        stage('Build & Push Image') {
            steps {
                script {
                    echo "Build et Push image..."

                    docker.withRegistry('https://ghcr.io', 'ghcr_pat') {
                        sh """
                            docker build -t ${IMAGE}:${TAG} -t ${IMAGE}:latest .
                            docker push ${IMAGE}:${TAG}
                            docker push ${IMAGE}:latest
                        """
                    }
                }
            }
        }

        // --- 3. KUBERNETES DEPLOYMENT ---
        stage('Deploy to K3s') {
            steps {
                script {
                    // Replace TAG in  YAML
                    sh """
                    sed -i 's|image: ${IMAGE}:.*|image: ${IMAGE}:${TAG}|' ${CRONJOB_FILE}
                    kubectl apply -f ${CRONJOB_FILE} -n jdccabanga
                    """

                    echo "Deployment updated with tag ${TAG}"
                }
            }
        }
    }
}