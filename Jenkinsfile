pipeline {
    agent {
        kubernetes {
            label 'kaniko'
            defaultContainer 'jnlp'
            yaml """
                apiVersion: v1
                kind: Pod
                metadata:
                    labels:
                        jenkins/label: kaniko
                spec:
                    containers:
                    - name: kaniko
                      image: gcr.io/kaniko-project/executor:latest
                      command: ["sleep"]
                      args: ["99d"]
                      volumeMounts:
                      - name: docker-config
                        mountPath: /kaniko/.docker
                        subPath: .dockerconfigjson
                    volumes:
                    - name: docker-config
                      secret:
                        secretName: ghcr-secret
            """
        }
    }

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
        TAG = "${DATE_TAG}-${COMMIT}"
    }

    stages {
        // --- CHECKOUT ---
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & push with Kaniko') {
            steps {
                container('kaniko') {
                    sh """
                        /kaniko/executor \
                            --context ${WORKSPACE} \
                            --dockerfile ${WORKSPACE}/Dockerfile \
                            --destination=${env.REGISTRY}/${env.IMAGE}:${env.TAG} \
                            --destination=${env.REGISTRY}/${env.IMAGE}:latest \
                            --digest-file=/dev/null
                    """
                }
            }
        }

        // --- KUBERNETES DEPLOYMENT ---
        stage('Deploy to K3s') {
            steps {
               withCredentials([file(credentialsId: 'kubeconfig-k3s', variable: 'KUBECONFIG')]){
                    sh """
                        export KUBECONFIG=\$KUBECONFIG
                        kubectl -n jdccabanga set image cronjob/jdccabanga \
                            jdccabanga=${env.REGISTRY}/${env.IMAGE}:${env.TAG}
                        kubectl -n jdccabanga create job --from=cronjob/jdccabanga jdccabanga-${env.DATE_TAG}
                    """
               }
            }
        }
    }
}