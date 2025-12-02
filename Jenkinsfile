pipeline {
    agent {
        kubernetes {
            label 'buildkit'
            defaultContainer 'buildkit'
            yaml """
                apiVersion: v1
                kind: Pod
                metadata:
                  labels:
                    jenkins/label: buildkit
                spec:
                  containers:
                    - name: buildkit
                      image: moby/buildkit:latest
                      securityContext:
                        privileged: true
                      command:
                        - buildkitd
                      args:
                        - --addr
                        - unix:///run/buildkit/buildkitd.sock
                      volumeMounts:
                        - name: docker-config
                          mountPath: /root/.docker/config.json
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

        stage('Prepare Git') {
            steps {
                sh "git config --global --add safe.directory '${WORKSPACE}'"
            }
        }

        stage('Build & Push with BuildKit') {
            steps {
                container('buildkit') {
                    sh """
                        buildctl build \
                          --frontend=dockerfile.v0 \
                          --local context=. \
                          --local dockerfile=. \
                          --output type=image,name=${env.REGISTRY}/${env.IMAGE}:${env.TAG},push=true \
                          --output type=image,name=${env.REGISTRY}/${env.IMAGE}:latest,push=true
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