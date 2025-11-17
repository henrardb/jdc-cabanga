pipeline {
    agent {
        // Dire à Jenkins de ne PAS ajouter l'étape de checkout implicite
        // Le code source est déjà disponible dans le répertoire de travail
        // car le Jenkinsfile a été lu.
        label 'jenkins'
        customWorkspace "/var/jenkins_home/workspace/cabanga-diary"
        skipDefaultCheckout true
    }

    // Global variables definition
    environment {
        DOCKER_IMAGE = "brunoh6720/jdc-cabanga"
        // TAG = date and time of build
        TAG = sh(returnStdout: true, script: "date +%Y%m%d%H%M%S").trim()
        KUBECONFIG_FILE = "cabanga-cronjob.yaml"
    }

    stages {
        // --- 2. BUILD & PUSH DOCKER ---
        stage('Build & Push Image') {
            steps {
                script {
                    echo "Authentification, Build et Push of image..."

                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {

                    // Build image
                    def customImage = docker.build("${DOCKER_IMAGE}:${TAG}", "-f Dockerfile .")
                    echo "Image construite: ${DOCKER_IMAGE}:${TAG}"

                    // Push image and TAG latest
                    customImage.push()
                    customImage.push('latest')
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