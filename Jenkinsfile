pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

    // Global variables definition
    environment {
        REGISTRY = "ghcr.io"
        IMAGE = "henrardb/jdccabanga"
        // TAG = date and time of build
        DATE_TAG = sh(returnStdout: true, script: "date +%Y%m%d%H%M%S").trim()
        COMMIT = sh(returnStdout: true, script: "git rev-parse --short HEAD").trim()
        TAG = ${DATE_TAG}-${COMMIT}
    }

    //options {
    //    skipDefaultCheckout(true)
    //}
    stages {
        // --- CHECKOUT ---
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // --- PREPARE BUILDX ---
        stage('Prepare buildx') {
            steps {
                sh """
                docker buildx create --name multiarch --use --bootstrap || true
                docker buildx inspect --bootstrap
                """
            }
        }

        // --- LOGIN TO GHCR
        stage('Login to GHCR') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'ghcr-token',
                                                    usernameVariable: 'GH_USER',
                                                    passwordVariable: 'GH_PAT')]) {
                    sh """
                    echo \$GH_PAT | docker login ${env.REGISTRY} -u \$GH_USER --password-stdin
                    """
                }
            }
        }

        // --- BUILD & PUSH IMAGE ---
        stage('Build & Push Image') {
            steps {
                echo "Build et Push image..."

                sh """
                    docker buildx build \
                        --platform linux/amd64, linux/arm64 \
                        -t ${ENV.REGISTRY}/${ENV.IMAGE}:${ENV.TAG} \
                        -t ${ENV.REGISTRY}/${ENV.IMAGE}:latest \
                        --push .
                """
            }
        }

        // --- KUBERNETES DEPLOYMENT ---
        stage('Deploy to K3s') {
            steps {
               withCredentials([file(credentialsId: 'kubeconfig-k3s', variable: 'KUBECONFIG')]){
                    sh """
                        export KUBECONFIG = \$KUBECONFIG
                        kubectl -n jdccabanga set image cronjob/jdccabanga \
                            jdccabanga=${ENV.REGISTRY}/${ENV.IMAGE}:${ENV.TAG}
                        kubectl -n jdccabanga create job --from=cronjob/jdccabanga jdccabanga-${env.DATE_TAG}
                    """
               }
            }
        }
    }
}